"""Native HopfReal/HopfComplex gate schedules from the first paper.

The functions in this module reproduce the first paper's deterministic
``Ctrl``, ``Anti``, ``Targ``, and ``Index`` lists without importing Qibo.  They
are used only to cross-check the inherited native preparation and its assigned
CNOT charge; the new QBP circuits use ``U_chk`` and ``W_R`` as distinct
full-unitary completions.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Literal, TypeAlias

from .conventions import controlled_rc_cnot_charge, controlled_ry_cnot_charge


NativeIndex: TypeAlias = int | tuple[int, int, int]


@dataclass(frozen=True)
class NativeGateSpec:
    """One gate in the first paper's native Hopf schedule.

    Masks use the first paper's integer-bit convention: bit position 0 is the
    least-significant computational-basis bit, and target masks are powers of
    two.  ``theta_index`` is one-based manuscript indexing.  A three-tuple
    denotes a promoted final-layer ``R_C`` gate.
    """

    ctrl_mask: int
    anti_mask: int
    target_mask: int
    theta_index: NativeIndex

    @property
    def num_controls(self) -> int:
        return (self.ctrl_mask | self.anti_mask).bit_count()

    @property
    def is_rc(self) -> bool:
        return isinstance(self.theta_index, tuple)


def hamming_weight_lists(n: int) -> tuple[tuple[int, ...], ...]:
    """Return ascending n-bit integers grouped by Hamming weight."""

    if n < 1:
        raise ValueError("n must be positive.")
    N = 1 << n
    groups: list[list[int]] = [[] for _ in range(n + 1)]
    pop = [0] * N
    for value in range(1, N):
        pop[value] = pop[value >> 1] + (value & 1)
    for value in range(N):
        groups[pop[value]].append(value)
    return tuple(tuple(group) for group in groups)


def find_pairs(a_values: tuple[int, ...] | list[int], b_values: tuple[int, ...] | list[int]) -> tuple[list[int], list[int]]:
    """Apply the first paper's deterministic greedy pairing rule."""

    a_list = list(a_values)
    b_list = list(b_values)
    pointer = len(a_list) - 1
    buckets: dict[int, list[int]] = {}
    for b in reversed(b_list):
        while pointer >= 0 and a_list[pointer] >= b:
            pointer -= 1
        if pointer < 0:
            break
        a = a_list[pointer]
        buckets.setdefault(a, []).append(b)

    out_a: list[int] = []
    out_b: list[int] = []
    for a in a_list:
        for b in buckets.get(a, []):
            out_a.append(a)
            out_b.append(b)
    return out_a, out_b


def anti_control_masks(a_values: list[int]) -> list[int]:
    """Return the first paper's ``Anti`` masks for one Hamming-weight block."""

    frequencies = Counter(a_values)
    masks: list[int] = []
    for a in sorted(frequencies):
        count = frequencies[a]
        for index in range(count, 0, -1):
            masks.append((1 << count) - (1 << index))
    return masks


def theta_real_index(n: int, old: int, new: int) -> int:
    distance = new - old
    if distance <= 0:
        raise ValueError("Native schedule pairs require new > old.")
    return ((1 << n) + old) // (2 * distance)


def theta_complex_index(n: int, old: int, new: int) -> NativeIndex:
    distance = new - old
    magnitude = theta_real_index(n, old, new)
    if distance == 1:
        return (magnitude, (1 << n) + old, (1 << n) + new)
    return magnitude


def native_schedule(n: int, case: Literal["real", "complex"] = "real") -> tuple[NativeGateSpec, ...]:
    """Return the first paper's native ``HopfReal`` or ``HopfComplex`` schedule."""

    if n < 1:
        raise ValueError("n must be positive.")
    if case not in ("real", "complex"):
        raise ValueError("case must be 'real' or 'complex'.")

    N = 1 << n
    groups = hamming_weight_lists(n)

    ctrl = [0] * n
    anti = [0] + [N - (1 << (n - index)) for index in range(1, n)]
    target = [1 << (n - 1 - index) for index in range(n)]
    if case == "real":
        indices: list[NativeIndex] = [1 << index for index in range(n)]
    else:
        indices = [1 << index for index in range(n - 1)]
        indices.append(((1 << (n - 1)), (1 << n), (1 << n) + 1))

    for weight in range(1, n):
        paired_a, paired_b = find_pairs(groups[weight], groups[weight + 1])
        ctrl.extend(paired_a)
        anti.extend(anti_control_masks(paired_a))
        target.extend([b - a for a, b in zip(paired_a, paired_b)])
        if case == "real":
            indices.extend(theta_real_index(n, a, b) for a, b in zip(paired_a, paired_b))
        else:
            indices.extend(theta_complex_index(n, a, b) for a, b in zip(paired_a, paired_b))

    if not (len(ctrl) == len(anti) == len(target) == len(indices) == N - 1):
        raise RuntimeError("Native schedule construction produced inconsistent list lengths.")

    return tuple(
        NativeGateSpec(c, a, t, index)
        for c, a, t, index in zip(ctrl, anti, target, indices)
    )


def native_real_schedule(n: int) -> tuple[NativeGateSpec, ...]:
    return native_schedule(n, "real")


def native_complex_schedule(n: int) -> tuple[NativeGateSpec, ...]:
    return native_schedule(n, "complex")


def qibo_index_from_target_mask(target_mask: int, n: int) -> int:
    """Map a power-of-two target mask to Qibo's big-endian system index."""

    if target_mask <= 0 or target_mask & (target_mask - 1):
        raise ValueError("target_mask must be a positive power of two.")
    bit_position = target_mask.bit_length() - 1
    if bit_position >= n:
        raise ValueError("target_mask lies outside the n-qubit register.")
    return n - 1 - bit_position


def qibo_indices_from_mask(mask: int, n: int) -> tuple[int, ...]:
    """Return Qibo system indices selected by an integer control mask."""

    if mask < 0 or mask >= (1 << n):
        raise ValueError("Mask lies outside the n-qubit register.")
    return tuple(n - 1 - bit for bit in range(n) if mask & (1 << bit))


def native_real_cnot_charge(n: int) -> int:
    return sum(controlled_ry_cnot_charge(gate.num_controls) for gate in native_real_schedule(n))


def native_complex_cnot_charge(n: int) -> int:
    total = 0
    for gate in native_complex_schedule(n):
        if gate.is_rc:
            total += controlled_rc_cnot_charge(gate.num_controls)
        else:
            total += controlled_ry_cnot_charge(gate.num_controls)
    return total
