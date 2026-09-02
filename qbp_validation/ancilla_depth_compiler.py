"""Structural checks for ancilla--depth robustness of the global Hopf frame.

This module is deliberately Qibo-free. It does not reproduce the elementary
circuits of Sun--Tian--Yang--Yuan--Zhang. Instead it exposes the exact Hopf
identities needed to lift that compiler architecture from state preparation to
the complete differential frame, and it records the resulting asymptotic depth
terms.

The finite matrix builders check two load-bearing facts:

* the first ``t`` addressed Hopf-frame layers are a ``t``-qubit Hopf frame
  conditioned on the untouched lower suffix being all zero; and
* the ``t``-qubit Hopf frame is a depth-``t`` network of disjoint two-mode
  Givens rotations on the single-excitation unary code.

The resource rows are term ledgers, not finite gate counts. Unit coefficients
are attached only to keep every contribution visible. Their asymptotic use
relies on the cited uniformly controlled gate, multi-controlled X, and
unary-to-binary synthesis theorems.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Iterable

import numpy as np

from .optimized_compiler import (
    direct_addressed_depth_layer,
    direct_real_frame,
    hopf_ry,
)


@dataclass(frozen=True)
class AncillaDepthRow:
    """One machine-readable ancilla--depth term ledger.

    ``state_ancillas`` is the clean workspace assigned to the reference state
    compiler. The frame construction reserves one additional reusable clean
    suffix flag. The displayed depth values are asymptotic term proxies with
    unit coefficients, not exact elementary-gate depths.
    """

    n: int
    dimension: int
    state_ancillas: int
    frame_ancillas: int
    unary_prefix_qubits: int
    unary_prefix_ancilla_upper_bound: int
    maximum_unary_control_copies: int
    tail_layers: int
    prefix_depth_proxy: int
    tail_predicate_depth_proxy: int
    ucg_linear_depth_proxy: int
    ucg_exponential_depth_proxy: int
    total_frame_depth_proxy: int
    theorem_geometric_term: int
    theorem_sequential_term: int
    logical_hopf_rotations: int
    recordwise_decode_operations_per_shot: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


def _validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")


def _validate_n_t(n: int, t: int) -> None:
    _validate_n(n)
    if not 0 <= t <= n:
        raise ValueError("t must lie in 0, ..., n.")


def _theta_for_n(theta_mag: object, n: int) -> np.ndarray:
    _validate_n(n)
    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    if values.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    return values


def prefix_angle_count(t: int) -> int:
    """Return the number of Hopf angles in the first ``t`` tree depths."""

    if t < 0:
        raise ValueError("t must be nonnegative.")
    return (1 << t) - 1


def direct_prefix_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return the product of addressed depths ``0, ..., t-1`` on ``n`` qubits."""

    _validate_n_t(n, t)
    values = _theta_for_n(theta_mag, n)
    unitary = np.eye(1 << n, dtype=complex)
    offset = 0
    for depth in range(t):
        width = 1 << depth
        layer = direct_addressed_depth_layer(
            n, depth, values[offset : offset + width]
        )
        unitary = layer @ unitary
        offset += width
    return unitary


def conditioned_prefix_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return ``W_t`` conditioned on the external lower suffix being zero.

    With ``P0 = |0**(n-t)><0**(n-t)|``, this is

    ``W_t kron P0 + I kron (I - P0)``.
    """

    _validate_n_t(n, t)
    values = _theta_for_n(theta_mag, n)
    if t == 0:
        return np.eye(1 << n, dtype=complex)

    prefix = direct_real_frame(t, values[: prefix_angle_count(t)])
    suffix_dimension = 1 << (n - t)
    suffix_zero = np.zeros((suffix_dimension, suffix_dimension), dtype=complex)
    suffix_zero[0, 0] = 1.0
    return np.kron(prefix, suffix_zero) + np.kron(
        np.eye(1 << t, dtype=complex),
        np.eye(suffix_dimension, dtype=complex) - suffix_zero,
    )


def tail_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return the product of addressed depths ``t, ..., n-1``."""

    _validate_n_t(n, t)
    values = _theta_for_n(theta_mag, n)
    unitary = np.eye(1 << n, dtype=complex)
    offset = prefix_angle_count(t)
    for depth in range(t, n):
        width = 1 << depth
        layer = direct_addressed_depth_layer(
            n, depth, values[offset : offset + width]
        )
        unitary = layer @ unitary
        offset += width
    return unitary


def hybrid_frame(n: int, t: int, theta_mag: object) -> np.ndarray:
    """Return the exact prefix-conditioned-plus-tail factorization of ``W_R``."""

    return tail_frame(n, t, theta_mag) @ conditioned_prefix_frame(
        n, t, theta_mag
    )


def prefix_bridge_residual(n: int, t: int, theta_mag: object) -> float:
    """Return the max-norm residual in the conditioned-prefix identity."""

    residual = direct_prefix_frame(n, t, theta_mag) - conditioned_prefix_frame(
        n, t, theta_mag
    )
    return float(np.max(np.abs(residual)))


def hybrid_frame_residual(n: int, t: int, theta_mag: object) -> float:
    """Return the max-norm residual between the hybrid factorization and ``W_R``."""

    residual = hybrid_frame(n, t, theta_mag) - direct_real_frame(n, theta_mag)
    return float(np.max(np.abs(residual)))


def unary_layer_pairs(t: int, depth: int) -> tuple[tuple[int, int], ...]:
    """Return the disjoint mode pairs for one unary Hopf tree depth."""

    if t < 1:
        raise ValueError("t must be positive for a unary Hopf layer.")
    if not 0 <= depth < t:
        raise ValueError("depth must lie in 0, ..., t-1.")
    suffix_width = t - depth - 1
    return tuple(
        (
            position << (t - depth),
            (position << (t - depth)) | (1 << suffix_width),
        )
        for position in range(1 << depth)
    )


def unary_code_isometry(
    t: int, *, maximum_hilbert_dimension: int = 4096
) -> np.ndarray:
    """Embed ``t`` binary qubits into the one-excitation code of ``2**t`` modes.

    This dense helper is for small exact tests only. Its ambient dimension is
    ``2**(2**t)``, so a guard prevents accidental large allocations.
    """

    if t < 1:
        raise ValueError("t must be positive for the unary-code matrix check.")
    modes = 1 << t
    hilbert_dimension = 1 << modes
    if hilbert_dimension > maximum_hilbert_dimension:
        raise ValueError(
            "Dense unary-code checks are limited by maximum_hilbert_dimension."
        )
    isometry = np.zeros((hilbert_dimension, modes), dtype=complex)
    for label in range(modes):
        isometry[1 << label, label] = 1.0
    return isometry


def unary_two_mode_givens(
    modes: int,
    first: int,
    second: int,
    theta: float,
    *,
    maximum_hilbert_dimension: int = 4096,
) -> np.ndarray:
    """Return a number-preserving two-mode Givens gate on a small unary register."""

    if modes < 2:
        raise ValueError("modes must be at least two.")
    if not 0 <= first < modes or not 0 <= second < modes or first == second:
        raise ValueError("first and second must be distinct valid mode indices.")
    hilbert_dimension = 1 << modes
    if hilbert_dimension > maximum_hilbert_dimension:
        raise ValueError(
            "Dense unary-code checks are limited by maximum_hilbert_dimension."
        )

    gate = np.eye(hilbert_dimension, dtype=complex)
    pair_mask = (1 << first) | (1 << second)
    block = hopf_ry(float(theta))
    for label in range(hilbert_dimension):
        if ((label >> first) & 1) and not ((label >> second) & 1):
            partner = label ^ pair_mask
            gate[np.ix_([label, partner], [label, partner])] = block
    return gate


def unary_hopf_network(
    t: int,
    theta_prefix: object,
    *,
    maximum_hilbert_dimension: int = 4096,
) -> np.ndarray:
    """Return the dense unary Givens network for a small ``t``-qubit Hopf frame."""

    if t < 1:
        raise ValueError("t must be positive for the unary-code matrix check.")
    values = np.asarray(theta_prefix, dtype=float).reshape(-1)
    if values.size != prefix_angle_count(t):
        raise ValueError("theta_prefix must have length 2**t - 1.")
    modes = 1 << t
    hilbert_dimension = 1 << modes
    if hilbert_dimension > maximum_hilbert_dimension:
        raise ValueError(
            "Dense unary-code checks are limited by maximum_hilbert_dimension."
        )

    unitary = np.eye(hilbert_dimension, dtype=complex)
    for depth in range(t):
        for first, second in unary_layer_pairs(t, depth):
            node = (1 << depth) + (first >> (t - depth))
            gate = unary_two_mode_givens(
                modes,
                first,
                second,
                values[node - 1],
                maximum_hilbert_dimension=maximum_hilbert_dimension,
            )
            unitary = gate @ unitary
    return unitary


def unary_code_action(t: int, theta_prefix: object) -> np.ndarray:
    """Return the effective binary action of the small unary Givens network."""

    isometry = unary_code_isometry(t)
    network = unary_hopf_network(t, theta_prefix)
    return isometry.conj().T @ network @ isometry


def unary_code_leakage(t: int, theta_prefix: object) -> float:
    """Return leakage from the one-excitation code under the unary Hopf network."""

    isometry = unary_code_isometry(t)
    network = unary_hopf_network(t, theta_prefix)
    projector = isometry @ isometry.conj().T
    leakage = (
        np.eye(network.shape[0], dtype=complex) - projector
    ) @ network @ isometry
    return float(np.max(np.abs(leakage)))


def maximum_unary_control_copies(t: int) -> int:
    """Return the maximum number of parallel controls used by a unary layer."""

    if t < 0:
        raise ValueError("t must be nonnegative.")
    return 0 if t == 0 else 1 << (t - 1)


def unary_prefix_ancilla_upper_bound(t: int) -> int:
    """Return the clean-workspace bound ``3*2**t - t`` for the unary prefix.

    The first ``t`` binary system qubits occupy ``t`` of the ``2**t`` unary
    register wires. The remaining unary wires cost ``2**t - t`` ancillas, and
    the Sun et al. unary-to-binary transform uses ``2**(t+1)`` additional clean
    ancillas. Those transform ancillas are clean again before the controlled
    Givens layers and can be reused for the suffix flag and coherent fanout.
    """

    if t < 0:
        raise ValueError("t must be nonnegative.")
    return 0 if t == 0 else 3 * (1 << t) - t


def hybrid_prefix_qubits(n: int, state_ancillas: int) -> int:
    """Return the conservative Sun-style choice ``floor(log2(m/3))``.

    The result is clamped to ``0, ..., n``. It guarantees
    ``3*2**t - t <= state_ancillas`` without using the small ``-t`` saving to
    enlarge the prefix by one additional qubit.
    """

    _validate_n(n)
    if state_ancillas < 0:
        raise ValueError("state_ancillas must be nonnegative.")
    if state_ancillas < 3:
        return 0
    quotient = state_ancillas // 3
    return min(n, quotient.bit_length() - 1)


def frame_layer_ucg_qubits(n: int, depth: int) -> int:
    """Return the UCG width, including target, in one flagged frame layer."""

    _validate_n(n)
    if not 0 <= depth < n:
        raise ValueError("depth must lie in 0, ..., n-1.")
    # Nonfinal layers use ``depth`` prefix controls plus one clean suffix flag.
    # The final layer has no lower suffix and therefore needs no flag.
    return depth + 2 if depth < n - 1 else n


def ucg_depth_proxy(total_qubits: int, work_ancillas: int) -> tuple[int, int]:
    """Return the terms in ``O(k + 2**k/(k+m))`` from Sun et al. Lemma 12."""

    if total_qubits < 1:
        raise ValueError("total_qubits must be positive.")
    if work_ancillas < 0:
        raise ValueError("work_ancillas must be nonnegative.")
    linear = total_qubits
    exponential = math.ceil(
        (1 << total_qubits) / (total_qubits + work_ancillas)
    )
    return linear, exponential


def unary_prefix_depth_proxy(n: int, t: int) -> int:
    """Expose the clean unary-prefix depth contributions with unit coefficients."""

    _validate_n_t(n, t)
    if t == 0:
        return 0
    # Two encoding transforms and t Givens layers. When an external suffix is
    # present, add predicate compute/uncompute and flag fanout/unfanout.
    if t == n:
        return 3 * t
    return 2 * t + t + 2 * (n - t) + 2 * t


def ancilla_depth_row(n: int, state_ancillas: int) -> AncillaDepthRow:
    """Return one asymptotic term ledger for the clean global-frame compiler."""

    _validate_n(n)
    if state_ancillas < 0:
        raise ValueError("state_ancillas must be nonnegative.")

    N = 1 << n
    t = hybrid_prefix_qubits(n, state_ancillas)
    prefix_depth = unary_prefix_depth_proxy(n, t)
    tail_predicate_depth = 0
    ucg_linear = 0
    ucg_exponential = 0
    for depth in range(t, n):
        suffix_width = n - depth - 1
        tail_predicate_depth += 2 * suffix_width
        linear, exponential = ucg_depth_proxy(
            frame_layer_ucg_qubits(n, depth), state_ancillas
        )
        ucg_linear += linear
        ucg_exponential += exponential

    total = (
        prefix_depth
        + tail_predicate_depth
        + ucg_linear
        + ucg_exponential
    )
    theorem_geometric = math.ceil(N / (n + state_ancillas))
    theorem_sequential = n * (n - t + 1)
    return AncillaDepthRow(
        n=n,
        dimension=N,
        state_ancillas=state_ancillas,
        frame_ancillas=state_ancillas + 1,
        unary_prefix_qubits=t,
        unary_prefix_ancilla_upper_bound=unary_prefix_ancilla_upper_bound(t),
        maximum_unary_control_copies=maximum_unary_control_copies(t),
        tail_layers=n - t,
        prefix_depth_proxy=prefix_depth,
        tail_predicate_depth_proxy=tail_predicate_depth,
        ucg_linear_depth_proxy=ucg_linear,
        ucg_exponential_depth_proxy=ucg_exponential,
        total_frame_depth_proxy=total,
        theorem_geometric_term=theorem_geometric,
        theorem_sequential_term=theorem_sequential,
        logical_hopf_rotations=N - 1,
        recordwise_decode_operations_per_shot=N,
    )


def ancilla_depth_rows(
    n: int, state_ancillas: Iterable[int]
) -> tuple[AncillaDepthRow, ...]:
    """Return validated rows for an iterable of ancillary budgets."""

    return tuple(ancilla_depth_row(n, int(value)) for value in state_ancillas)
