"""Independent NumPy reference formulas for the Hopf-QBP manuscript.

No function in this module imports Qibo or calls a circuit builder. The test
suite uses these recursive formulas as the analytic side of circuit comparisons.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .conventions import (
    checkpoint_interface_projector,
    depth_gate_specs,
    frame_gate_specs,
    infer_n_from_theta_mag,
    marker_label,
    split_theta,
)


@dataclass(frozen=True)
class RealTreeData:
    """Recursive data for the balanced real Hopf tree."""

    n: int
    state: np.ndarray
    subtree: tuple[np.ndarray | None, ...]
    complements: tuple[np.ndarray | None, ...]
    sqrt_metric: np.ndarray
    metric: np.ndarray
    derivatives: tuple[np.ndarray, ...]


def basis_vector(dimension: int, label: int, *, dtype: type = complex) -> np.ndarray:
    vec = np.zeros(dimension, dtype=dtype)
    vec[label] = 1
    return vec


def ry_matrix(theta: float) -> np.ndarray:
    return np.asarray(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]],
        dtype=complex,
    )


def rc_matrix(theta_a: float, theta_b: float, theta_c: float) -> np.ndarray:
    """Return the first paper's three-parameter ``R_C`` gate."""

    c = float(np.cos(theta_a))
    s = float(np.sin(theta_a))
    return np.asarray(
        [
            [np.exp(1j * theta_b) * c, -np.exp(-1j * theta_c) * s],
            [np.exp(1j * theta_c) * s, np.exp(-1j * theta_b) * c],
        ],
        dtype=complex,
    )


def real_tree_data(theta_mag: object) -> RealTreeData:
    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta_mag)
    N = 1 << n

    subtree: list[np.ndarray | None] = [None] * (2 * N)
    complements: list[np.ndarray | None] = [None] * N
    for ell in range(N):
        subtree[N + ell] = basis_vector(N, ell, dtype=float)

    for node in range(N - 1, 0, -1):
        left = subtree[2 * node]
        right = subtree[2 * node + 1]
        assert left is not None and right is not None
        c = float(np.cos(theta_mag[node - 1]))
        s = float(np.sin(theta_mag[node - 1]))
        subtree[node] = c * left + s * right
        complements[node] = -s * left + c * right

    incoming_by_node = np.zeros(N, dtype=float)
    incoming_by_node[1] = 1.0
    for node in range(1, N):
        left = 2 * node
        right = left + 1
        if left < N:
            incoming_by_node[left] = incoming_by_node[node] * np.cos(theta_mag[node - 1])
        if right < N:
            incoming_by_node[right] = incoming_by_node[node] * np.sin(theta_mag[node - 1])

    sqrt_metric = incoming_by_node[1:].copy()
    derivatives: list[np.ndarray] = []
    for node in range(1, N):
        comp = complements[node]
        assert comp is not None
        derivatives.append(sqrt_metric[node - 1] * comp)

    root = subtree[1]
    assert root is not None
    return RealTreeData(
        n=n,
        state=np.asarray(root, dtype=float),
        subtree=tuple(subtree),
        complements=tuple(complements),
        sqrt_metric=sqrt_metric,
        metric=sqrt_metric**2,
        derivatives=tuple(derivatives),
    )


def real_state(theta_mag: object) -> np.ndarray:
    return real_tree_data(theta_mag).state


def real_frame_matrix(theta_mag: object) -> np.ndarray:
    data = real_tree_data(theta_mag)
    N = 1 << data.n
    frame = np.zeros((N, N), dtype=float)
    frame[:, 0] = data.state
    for node in range(1, N):
        comp = data.complements[node]
        assert comp is not None
        frame[:, marker_label(node, data.n)] = comp
    return frame


def phase_layer_matrix(theta_ph: object, *, inverse: bool = False) -> np.ndarray:
    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phase.size == 0 or phase.size & (phase.size - 1):
        raise ValueError("theta_ph length must be a positive power of two.")
    sign = -1.0 if inverse else 1.0
    return np.diag(np.exp(1j * sign * phase))


def complex_state(theta_mag: object, theta_ph: object) -> np.ndarray:
    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    theta_ph = np.asarray(theta_ph, dtype=float).reshape(-1)
    data = real_tree_data(theta_mag)
    N = 1 << data.n
    if theta_ph.size != N:
        raise ValueError("The complex Hopf chart requires one phase per leaf.")
    return np.exp(1j * theta_ph) * data.state


def complex_state_from_theta(theta: object) -> np.ndarray:
    theta_mag, theta_ph = split_theta(theta)
    return complex_state(theta_mag, theta_ph)


def complex_frame_matrix(theta_mag: object, theta_ph: object) -> np.ndarray:
    """Return the exact full complex frame ``W_C = D_ph W_R``."""

    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    theta_ph = np.asarray(theta_ph, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta_mag)
    if theta_ph.size != 1 << n:
        raise ValueError("The complex Hopf chart requires one phase per leaf.")
    return phase_layer_matrix(theta_ph) @ real_frame_matrix(theta_mag)


def complex_magnitude_derivatives(
    theta_mag: object, theta_ph: object
) -> tuple[np.ndarray, ...]:
    data = real_tree_data(theta_mag)
    phase = np.exp(1j * np.asarray(theta_ph, dtype=float).reshape(-1))
    if phase.size != (1 << data.n):
        raise ValueError("The complex Hopf chart requires one phase per leaf.")
    return tuple(phase * deriv for deriv in data.derivatives)


def complex_phase_derivatives(
    theta_mag: object, theta_ph: object
) -> tuple[np.ndarray, ...]:
    psi = complex_state(theta_mag, theta_ph)
    N = psi.size
    out: list[np.ndarray] = []
    for ell in range(N):
        deriv = np.zeros(N, dtype=complex)
        deriv[ell] = 1j * psi[ell]
        out.append(deriv)
    return tuple(out)


def expectation(state: np.ndarray, observable: np.ndarray) -> float:
    return float(np.real(np.vdot(state, observable @ state)))


def coordinate_gradient(
    state: np.ndarray, derivatives: tuple[np.ndarray, ...], observable: np.ndarray
) -> np.ndarray:
    Opsi = observable @ state
    return np.asarray(
        [2.0 * np.real(np.vdot(deriv, Opsi)) for deriv in derivatives],
        dtype=float,
    )


def real_gradient(theta_mag: object, observable: np.ndarray) -> np.ndarray:
    data = real_tree_data(theta_mag)
    return coordinate_gradient(data.state.astype(complex), data.derivatives, observable)


def complex_magnitude_gradient(
    theta_mag: object, theta_ph: object, observable: np.ndarray
) -> np.ndarray:
    psi = complex_state(theta_mag, theta_ph)
    return coordinate_gradient(
        psi, complex_magnitude_derivatives(theta_mag, theta_ph), observable
    )


def complex_phase_gradient(
    theta_mag: object, theta_ph: object, observable: np.ndarray
) -> np.ndarray:
    psi = complex_state(theta_mag, theta_ph)
    return coordinate_gradient(psi, complex_phase_derivatives(theta_mag, theta_ph), observable)


def complex_full_gradient(
    theta_mag: object, theta_ph: object, observable: np.ndarray
) -> np.ndarray:
    return np.concatenate(
        [
            complex_magnitude_gradient(theta_mag, theta_ph, observable),
            complex_phase_gradient(theta_mag, theta_ph, observable),
        ]
    )


def is_hermitian_unitary(observable: np.ndarray, atol: float = 1e-12) -> bool:
    observable = np.asarray(observable, dtype=complex)
    if observable.ndim != 2 or observable.shape[0] != observable.shape[1]:
        return False
    eye = np.eye(observable.shape[0], dtype=complex)
    return bool(
        np.allclose(observable, observable.conj().T, atol=atol, rtol=0.0)
        and np.allclose(observable @ observable, eye, atol=atol, rtol=0.0)
    )


def two_level_matrix(
    dimension: int, first: int, second: int, block: np.ndarray
) -> np.ndarray:
    """Embed a 2-by-2 block on an ordered computational-basis pair."""

    if block.shape != (2, 2):
        raise ValueError("block must be 2 by 2.")
    out = np.eye(dimension, dtype=complex)
    out[first, first] = block[0, 0]
    out[first, second] = block[0, 1]
    out[second, first] = block[1, 0]
    out[second, second] = block[1, 1]
    return out


def depth_layer_matrix(theta_mag: object, depth: int) -> np.ndarray:
    """Return the exact breadth-first layer ``U_d``."""

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta)
    if not 0 <= depth < n:
        raise ValueError("Depth must lie in 0, ..., n-1.")
    N = 1 << n
    out = np.eye(N, dtype=complex)
    suffix_width = n - depth - 1
    for spec in depth_gate_specs(n, depth):
        angle = theta[spec.node - 1]
        block = ry_matrix(angle)
        for suffix in range(1 << suffix_width):
            first = (spec.position << (suffix_width + 1)) | suffix
            second = first | (1 << suffix_width)
            out[np.ix_([first, second], [first, second])] = block
    return out


def depth_preparation_matrix(theta_mag: object) -> np.ndarray:
    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta)
    N = 1 << n
    out = np.eye(N, dtype=complex)
    for depth in range(n):
        out = depth_layer_matrix(theta, depth) @ out
    return out


def depth_prefix_matrix(theta_mag: object, depth: int) -> np.ndarray:
    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta)
    if not 0 <= depth < n:
        raise ValueError("Depth must lie in 0, ..., n-1.")
    N = 1 << n
    out = np.eye(N, dtype=complex)
    for current in range(depth + 1):
        out = depth_layer_matrix(theta, current) @ out
    return out


def depth_suffix_matrix(theta_mag: object, depth: int) -> np.ndarray:
    """Return ``B_d = U_{n-1} ... U_{d+1}``."""

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta)
    if not 0 <= depth < n:
        raise ValueError("Depth must lie in 0, ..., n-1.")
    N = 1 << n
    out = np.eye(N, dtype=complex)
    for current in range(depth + 1, n):
        out = depth_layer_matrix(theta, current) @ out
    return out


def centered_leaf_phases(theta_ph: object) -> tuple[float, np.ndarray]:
    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phase.size == 0 or phase.size & (phase.size - 1):
        raise ValueError("theta_ph length must be a positive power of two.")
    mean = float(np.mean(phase))
    return mean, phase - mean


def four_qubit_rc_phase_arguments(theta_ph: object) -> dict[int, tuple[float, float]]:
    """Return Appendix-A ``(alpha_j, beta_j)`` for the addressed ``W_C`` compiler."""

    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phase.size != 16:
        raise ValueError("The explicit addressed R_C compiler is four-qubit only.")
    _, centered = centered_leaf_phases(phase)
    sums = np.zeros(32, dtype=float)
    sums[16:32] = centered
    for node in range(15, 0, -1):
        sums[node] = sums[2 * node] + sums[2 * node + 1]
    return {
        node: (-float(sums[2 * node + 1]), -float(sums[2 * node]))
        for node in range(1, 16)
    }


def addressed_rc_frame_matrix_4q(theta_mag: object, theta_ph: object) -> np.ndarray:
    """Return the Appendix-A addressed ``R_C`` implementation of ``W_C``.

    The result equals ``exp(-i * mean(theta_ph)) * W_C`` as a complete matrix.
    """

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if theta.size != 15 or phase.size != 16:
        raise ValueError("The explicit addressed R_C compiler is four-qubit only.")
    arguments = four_qubit_rc_phase_arguments(phase)
    out = np.eye(16, dtype=complex)
    for spec in frame_gate_specs(4):
        alpha, beta = arguments[spec.node]
        gate = two_level_matrix(
            16,
            spec.anchor,
            spec.marker,
            rc_matrix(theta[spec.node - 1], alpha, beta),
        )
        out = gate @ out
    return out


def four_qubit_b2c_matrix(theta_mag: object, theta_ph: object) -> np.ndarray:
    """Return the Appendix-A complex depth-2 suffix ``B_{2,C}``."""

    theta = np.asarray(theta_mag, dtype=float).reshape(-1)
    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if theta.size != 15 or phase.size != 16:
        raise ValueError("B_{2,C} is defined here for the four-qubit example.")
    out = np.eye(16, dtype=complex)
    for prefix in range(8):
        first = 2 * prefix
        second = first + 1
        block = rc_matrix(theta[7 + prefix], phase[2 * prefix], phase[2 * prefix + 1])
        out[np.ix_([first, second], [first, second])] = block
    return out


def four_qubit_b2c_interface_residual(theta_mag: object, theta_ph: object) -> float:
    """Return ``||B_{2,C}P_2 - D_ph B_2 P_2||_max``."""

    b2c = four_qubit_b2c_matrix(theta_mag, theta_ph)
    b2 = depth_suffix_matrix(theta_mag, 2)
    projector = checkpoint_interface_projector(4, 2)
    separated = phase_layer_matrix(theta_ph) @ b2
    return float(np.max(np.abs(b2c @ projector - separated @ projector)))
