"""Qibo-free optimized compiler references for Hopf-QBP.

The manuscript's assigned ledger decomposes each multi-controlled rotation
independently.  This module records a complementary, asymptotically optimized
factorization based on uniformly controlled rotations (multiplexors).

The forward depth layer is already a uniformly controlled ``R_y``.  For an
addressed-frame layer, one reusable clean flag stores the predicate that the
lower suffix is all zero.  A uniformly controlled ``R_y`` selected by the
prefix and flag then applies all rotations at that depth, after which the flag
is uncomputed.

The matrix builders below validate the logical factorization on the clean-flag
input subspace.  They do not emit a routed hardware circuit.  The CNOT counts
refer only to the standard uniformly-controlled-rotation cores; the reversible
suffix predicates are reported separately because their exact finite count
depends on the chosen multi-controlled-X synthesis.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class OptimizedCompilerRow:
    """One row of the optimized asymptotic resource companion."""

    n: int
    dimension: int
    forward_ucr_cnot_upper_bound: int
    frame_ucr_core_cnot_upper_bound: int
    suffix_predicate_calls: int
    maximum_predicate_controls: int
    reusable_clean_flags: int

    def as_dict(self) -> dict[str, int]:
        return {key: int(value) for key, value in asdict(self).items()}


def _validate_n_depth(n: int, depth: int) -> None:
    if n < 1:
        raise ValueError("n must be positive.")
    if not 0 <= depth < n:
        raise ValueError("depth must lie in 0, ..., n-1.")


def _angles_for_depth(angles: object, depth: int) -> np.ndarray:
    values = np.asarray(angles, dtype=float).reshape(-1)
    if values.size != 1 << depth:
        raise ValueError("angles must contain exactly 2**depth entries.")
    return values


def hopf_ry(theta: float) -> np.ndarray:
    """Return ``R_y(theta) = exp(-i theta Y)`` in the Hopf convention."""

    c = float(math.cos(float(theta)))
    s = float(math.sin(float(theta)))
    return np.asarray([[c, -s], [s, c]], dtype=complex)


def direct_addressed_depth_layer(
    n: int,
    depth: int,
    angles: object,
) -> np.ndarray:
    """Return one addressed-frame depth layer on the system register.

    Prefix ``r`` selects angle ``angles[r]``.  The rotation acts only when the
    lower ``n-depth-1`` suffix qubits are all zero.
    """

    _validate_n_depth(n, depth)
    values = _angles_for_depth(angles, depth)
    dimension = 1 << n
    suffix_width = n - depth - 1
    unitary = np.eye(dimension, dtype=complex)

    for prefix, theta in enumerate(values):
        anchor = prefix << (n - depth)
        marker = anchor | (1 << suffix_width)
        unitary[np.ix_([anchor, marker], [anchor, marker])] = hopf_ry(float(theta))

    return unitary


def suffix_zero_flag_permutation(n: int, depth: int) -> np.ndarray:
    """Compute ``flag ^= [lower suffix == 0]`` with the flag as the last bit.

    This is a reference permutation, not a particular multi-controlled-X
    decomposition.  It is self-inverse and acts on ``n`` system qubits plus one
    flag qubit.
    """

    _validate_n_depth(n, depth)
    system_dimension = 1 << n
    total_dimension = 2 * system_dimension
    suffix_width = n - depth - 1
    suffix_mask = (1 << suffix_width) - 1
    permutation = np.zeros((total_dimension, total_dimension), dtype=complex)

    for system_label in range(system_dimension):
        is_zero_suffix = int(
            suffix_width == 0 or (system_label & suffix_mask) == 0
        )
        for flag in (0, 1):
            source = 2 * system_label + flag
            target = 2 * system_label + (flag ^ is_zero_suffix)
            permutation[target, source] = 1.0

    return permutation


def flagged_multiplexor_depth_layer(
    n: int,
    depth: int,
    angles: object,
) -> np.ndarray:
    """Return the prefix-and-flag uniformly controlled rotation as a matrix.

    The flag is the least-significant register bit.  When the flag is zero all
    selected angles are zero; when it is one, prefix ``r`` selects
    ``angles[r]``.
    """

    _validate_n_depth(n, depth)
    values = _angles_for_depth(angles, depth)
    system_dimension = 1 << n
    total_dimension = 2 * system_dimension
    suffix_width = n - depth - 1
    multiplexor = np.eye(total_dimension, dtype=complex)

    for prefix, theta in enumerate(values):
        for suffix in range(1 << suffix_width):
            target_zero = (prefix << (n - depth)) | suffix
            target_one = target_zero | (1 << suffix_width)
            indices = [2 * target_zero + 1, 2 * target_one + 1]
            multiplexor[np.ix_(indices, indices)] = hopf_ry(float(theta))

    return multiplexor


def flagged_addressed_depth_layer(
    n: int,
    depth: int,
    angles: object,
) -> np.ndarray:
    """Return the optimized flagged factorization for one addressed layer.

    The final depth has no lower suffix, so its ordinary prefix multiplexor is
    tensored with the identity on the unused flag.
    """

    _validate_n_depth(n, depth)
    values = _angles_for_depth(angles, depth)
    if depth == n - 1:
        return np.kron(
            direct_addressed_depth_layer(n, depth, values),
            np.eye(2, dtype=complex),
        )
    predicate = suffix_zero_flag_permutation(n, depth)
    multiplexor = flagged_multiplexor_depth_layer(n, depth, values)
    return predicate @ multiplexor @ predicate


def clean_flag_system_block(unitary: object, n: int) -> np.ndarray:
    """Extract the system operator from clean-flag input and output columns."""

    if n < 1:
        raise ValueError("n must be positive.")
    matrix = np.asarray(unitary, dtype=complex)
    expected = 1 << (n + 1)
    if matrix.shape != (expected, expected):
        raise ValueError("unitary shape does not match n system qubits plus one flag.")
    return matrix[0::2, 0::2]


def clean_flag_leakage_block(unitary: object, n: int) -> np.ndarray:
    """Extract amplitudes leaking from flag ``|0>`` input to flag ``|1>``."""

    if n < 1:
        raise ValueError("n must be positive.")
    matrix = np.asarray(unitary, dtype=complex)
    expected = 1 << (n + 1)
    if matrix.shape != (expected, expected):
        raise ValueError("unitary shape does not match n system qubits plus one flag.")
    return matrix[1::2, 0::2]


def direct_real_frame(n: int, theta_mag: object) -> np.ndarray:
    """Compose all direct addressed depth layers in forward depth order."""

    if n < 1:
        raise ValueError("n must be positive.")
    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    if values.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    unitary = np.eye(1 << n, dtype=complex)
    offset = 0
    for depth in range(n):
        width = 1 << depth
        layer = direct_addressed_depth_layer(
            n, depth, values[offset : offset + width]
        )
        unitary = layer @ unitary
        offset += width
    return unitary


def flagged_real_frame(n: int, theta_mag: object) -> np.ndarray:
    """Compose the flagged factorization of the full addressed real frame."""

    if n < 1:
        raise ValueError("n must be positive.")
    values = np.asarray(theta_mag, dtype=float).reshape(-1)
    if values.size != (1 << n) - 1:
        raise ValueError("theta_mag must have length 2**n - 1.")
    unitary = np.eye(1 << (n + 1), dtype=complex)
    offset = 0
    for depth in range(n):
        width = 1 << depth
        layer = flagged_addressed_depth_layer(
            n, depth, values[offset : offset + width]
        )
        unitary = layer @ unitary
        offset += width
    return unitary


def ucr_ry_cnot_upper_bound(num_controls: int) -> int:
    """Standard exact CNOT upper bound for a uniformly controlled ``R_y``.

    A nontrivial multiplexor with ``k`` controls uses ``2**k`` CNOTs in the
    standard Gray-code construction.  The zero-control case is one local
    rotation and uses no CNOT.
    """

    if num_controls < 0:
        raise ValueError("num_controls must be nonnegative.")
    return 0 if num_controls == 0 else 1 << num_controls


def forward_ucr_cnot_upper_bound(n: int) -> int:
    """CNOT upper bound for ``U_chk`` using one multiplexor per depth."""

    if n < 1:
        raise ValueError("n must be positive.")
    return sum(ucr_ry_cnot_upper_bound(depth) for depth in range(n))


def inverse_suffix_ucr_cnot_upper_bound(n: int, selected_depth: int) -> int:
    """CNOT upper bound for ``B_d^dagger`` using optimized depth layers."""

    _validate_n_depth(n, selected_depth)
    return sum(
        ucr_ry_cnot_upper_bound(depth)
        for depth in range(selected_depth + 1, n)
    )


def frame_ucr_core_cnot_upper_bound(n: int) -> int:
    """CNOT bound for the addressed-frame multiplexor cores.

    The reversible compute/uncompute cost of the suffix-zero predicates is not
    included.  For depths below the final one, the prefix and flag supply
    ``depth + 1`` controls.  The final depth has no suffix predicate and uses
    ``n - 1`` prefix controls.
    """

    if n < 1:
        raise ValueError("n must be positive.")
    if n == 1:
        return 0
    flagged_depths = sum(
        ucr_ry_cnot_upper_bound(depth + 1) for depth in range(n - 1)
    )
    final_depth = ucr_ry_cnot_upper_bound(n - 1)
    return flagged_depths + final_depth


def suffix_predicate_control_widths(n: int) -> tuple[int, ...]:
    """Control widths of all predicate computations and uncomputations."""

    if n < 1:
        raise ValueError("n must be positive.")
    widths: list[int] = []
    for depth in range(n - 1):
        width = n - depth - 1
        widths.extend((width, width))
    return tuple(widths)


def suffix_predicate_quadratic_proxy(n: int) -> int:
    """Return ``sum m**2`` over predicate calls, not an exact gate count.

    Exact ancilla-free multi-controlled-X decompositions have quadratic cost in
    their control width.  This proxy exposes the resulting ``O(n**3)`` total
    without attaching a compiler-specific constant.
    """

    return sum(width * width for width in suffix_predicate_control_widths(n))


def optimized_compiler_row(n: int) -> OptimizedCompilerRow:
    """Return one machine-readable optimized compiler summary row."""

    if n < 1:
        raise ValueError("n must be positive.")
    widths = suffix_predicate_control_widths(n)
    return OptimizedCompilerRow(
        n=n,
        dimension=1 << n,
        forward_ucr_cnot_upper_bound=forward_ucr_cnot_upper_bound(n),
        frame_ucr_core_cnot_upper_bound=frame_ucr_core_cnot_upper_bound(n),
        suffix_predicate_calls=len(widths),
        maximum_predicate_controls=max(widths, default=0),
        reusable_clean_flags=1 if n > 1 else 0,
    )


def optimized_compiler_rows(ns: Iterable[int]) -> tuple[OptimizedCompilerRow, ...]:
    """Return validated rows for an iterable of qubit counts."""

    return tuple(optimized_compiler_row(int(n)) for n in ns)
