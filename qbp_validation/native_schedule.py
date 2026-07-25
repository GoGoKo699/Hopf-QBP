"""Native HopfReal/HopfComplex gate schedules from the first paper.

The functions reproduce the first paper's deterministic ``Ctrl``, ``Anti``,
``Targ``, and ``Index`` lists without importing Qibo. They cross-check the
inherited native preparations and their assigned CNOT charges; the QBP circuits
use native, depth, and frame completions under the contracts stated in the
manuscript.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Literal, TypeAlias

import numpy as np

from .conventions import controlled_rc_cnot_charge, controlled_ry_cnot_charge


NativeIndex: TypeAlias = int | tuple[int, int, int]


@dataclass(frozen=True)
class NativeGateSpec:
    """One gate in the first paper's native Hopf schedule."""

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


def find_pairs(
    a_values: tuple[int, ...] | list[int],
    b_values: tuple[int, ...] | list[int],
) -> tuple[list[int], list[int]]:
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


def native_schedule(
    n: int, case: Literal["real", "complex"] = "real"
) -> tuple[NativeGateSpec, ...]:
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
            indices.extend(
                theta_real_index(n, a, b) for a, b in zip(paired_a, paired_b)
            )
        else:
            indices.extend(
                theta_complex_index(n, a, b) for a, b in zip(paired_a, paired_b)
            )

    if not (len(ctrl) == len(anti) == len(target) == len(indices) == N - 1):
        raise RuntimeError("Native schedule construction produced inconsistent lists.")

    return tuple(
        NativeGateSpec(c, a, t, index)
        for c, a, t, index in zip(ctrl, anti, target, indices)
    )


def native_real_schedule(n: int) -> tuple[NativeGateSpec, ...]:
    return native_schedule(n, "real")


def native_complex_schedule(n: int) -> tuple[NativeGateSpec, ...]:
    return native_schedule(n, "complex")


def qibo_index_from_target_mask(target_mask: int, n: int) -> int:
    if target_mask <= 0 or target_mask & (target_mask - 1):
        raise ValueError("target_mask must be a positive power of two.")
    bit_position = target_mask.bit_length() - 1
    if bit_position >= n:
        raise ValueError("target_mask lies outside the n-qubit register.")
    return n - 1 - bit_position


def qibo_indices_from_mask(mask: int, n: int) -> tuple[int, ...]:
    if mask < 0 or mask >= (1 << n):
        raise ValueError("Mask lies outside the n-qubit register.")
    return tuple(n - 1 - bit for bit in range(n) if mask & (1 << bit))


def native_real_cnot_charge(n: int) -> int:
    return sum(
        controlled_ry_cnot_charge(gate.num_controls)
        for gate in native_real_schedule(n)
    )


def native_complex_cnot_charge(n: int) -> int:
    total = 0
    for gate in native_complex_schedule(n):
        if gate.is_rc:
            total += controlled_rc_cnot_charge(gate.num_controls)
        else:
            total += controlled_ry_cnot_charge(gate.num_controls)
    return total


def _rc_matrix(theta_a: float, theta_b: float, theta_c: float) -> np.ndarray:
    c = float(np.cos(theta_a))
    s = float(np.sin(theta_a))
    return np.asarray(
        [
            [np.exp(1j * theta_b) * c, -np.exp(-1j * theta_c) * s],
            [np.exp(1j * theta_c) * s, np.exp(-1j * theta_b) * c],
        ],
        dtype=complex,
    )


def _apply_patterned_gate(
    state: np.ndarray,
    n: int,
    target_mask: int,
    ctrl_mask: int,
    anti_mask: int,
    matrix: np.ndarray,
) -> np.ndarray:
    """Apply one native one-qubit gate directly to a statevector."""

    out = np.asarray(state, dtype=complex).copy()
    target_bit = target_mask.bit_length() - 1
    target_value = 1 << target_bit
    for base in range(1 << n):
        if base & target_value:
            continue
        if (base & ctrl_mask) != ctrl_mask or (base & anti_mask) != 0:
            continue
        partner = base | target_value
        pair = matrix @ np.asarray([out[base], out[partner]], dtype=complex)
        out[base], out[partner] = pair[0], pair[1]
    return out


def native_real_statevector(theta_mag: object) -> np.ndarray:
    """Qibo-independent state column of the native ``HopfReal`` schedule."""

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = int(round(np.log2(theta.size + 1)))
    if theta.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    state = np.zeros(1 << n, dtype=complex)
    state[0] = 1.0
    for gate in native_real_schedule(n):
        assert isinstance(gate.theta_index, int)
        angle = theta[gate.theta_index - 1]
        matrix = np.asarray(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
            dtype=complex,
        )
        state = _apply_patterned_gate(
            state,
            n,
            gate.target_mask,
            gate.ctrl_mask,
            gate.anti_mask,
            matrix,
        )
    return state


def native_complex_statevector(theta_mag: object, theta_ph: object) -> np.ndarray:
    """Qibo-independent state column of the native ``HopfComplex`` schedule."""

    mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    ph = np.asarray(theta_ph, dtype=float).reshape(-1)
    n = int(round(np.log2(mag.size + 1)))
    N = 1 << n
    if mag.size != N - 1 or ph.size != N:
        raise ValueError("Inconsistent complex Hopf parameter blocks.")
    state = np.zeros(N, dtype=complex)
    state[0] = 1.0
    for gate in native_complex_schedule(n):
        if isinstance(gate.theta_index, int):
            angle = mag[gate.theta_index - 1]
            matrix = np.asarray(
                [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
                dtype=complex,
            )
        else:
            magnitude, left_phase, right_phase = gate.theta_index
            matrix = _rc_matrix(
                mag[magnitude - 1], ph[left_phase - N], ph[right_phase - N]
            )
        state = _apply_patterned_gate(
            state,
            n,
            gate.target_mask,
            gate.ctrl_mask,
            gate.anti_mask,
            matrix,
        )
    return state
