"""Independent NumPy reference formulas for the Hopf-QBP manuscript.

No function in this module imports Qibo or calls a circuit builder.  The test
suite uses these recursive formulas as the analytic side of every circuit-level
comparison.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np

from .conventions import (
    PolyLeaf,
    PolyTree,
    infer_n_from_theta_mag,
    marker_label,
    poly_anchor,
    poly_leaves,
    poly_marker,
    poly_preorder,
    split_theta,
    validate_poly_tree,
)


@dataclass(frozen=True)
class RealTreeData:
    """Recursive data for the balanced real Hopf tree.

    ``sqrt_metric[node-1]`` is the incoming subtree amplitude
    ``sqrt(g^R_{j,j})`` for node ``j``.  ``metric`` is its square.
    """

    n: int
    state: np.ndarray
    subtree: tuple[np.ndarray | None, ...]
    complements: tuple[np.ndarray | None, ...]
    sqrt_metric: np.ndarray
    metric: np.ndarray
    derivatives: tuple[np.ndarray, ...]


@dataclass(frozen=True)
class PolyTreeData:
    state: np.ndarray
    complements: dict[str, np.ndarray]
    sqrt_metric: dict[str, float]
    derivatives: dict[str, np.ndarray]
    anchors: dict[str, int]
    markers: dict[str, int]


def basis_vector(dimension: int, label: int, *, dtype: type = complex) -> np.ndarray:
    vec = np.zeros(dimension, dtype=dtype)
    vec[label] = 1
    return vec


def real_tree_data(theta_mag: np.ndarray | list[float] | tuple[float, ...]) -> RealTreeData:
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


def real_state(theta_mag: np.ndarray | list[float] | tuple[float, ...]) -> np.ndarray:
    return real_tree_data(theta_mag).state


def real_frame_matrix(theta_mag: np.ndarray | list[float] | tuple[float, ...]) -> np.ndarray:
    data = real_tree_data(theta_mag)
    N = 1 << data.n
    frame = np.zeros((N, N), dtype=float)
    frame[:, 0] = data.state
    for node in range(1, N):
        comp = data.complements[node]
        assert comp is not None
        frame[:, marker_label(node, data.n)] = comp
    return frame


def complex_state(theta_mag: np.ndarray, theta_ph: np.ndarray) -> np.ndarray:
    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    theta_ph = np.asarray(theta_ph, dtype=float).reshape(-1)
    data = real_tree_data(theta_mag)
    N = 1 << data.n
    if theta_ph.size != N:
        raise ValueError("The complex Hopf chart requires one phase per leaf.")
    return np.exp(1j * theta_ph) * data.state


def complex_state_from_theta(theta: np.ndarray) -> np.ndarray:
    theta_mag, theta_ph = split_theta(theta)
    return complex_state(theta_mag, theta_ph)


def complex_magnitude_derivatives(
    theta_mag: np.ndarray, theta_ph: np.ndarray
) -> tuple[np.ndarray, ...]:
    data = real_tree_data(theta_mag)
    phase = np.exp(1j * np.asarray(theta_ph, dtype=float).reshape(-1))
    if phase.size != (1 << data.n):
        raise ValueError("The complex Hopf chart requires one phase per leaf.")
    return tuple(phase * deriv for deriv in data.derivatives)


def complex_phase_derivatives(
    theta_mag: np.ndarray, theta_ph: np.ndarray
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
        [2.0 * np.real(np.vdot(deriv, Opsi)) for deriv in derivatives], dtype=float
    )


def real_gradient(theta_mag: np.ndarray, observable: np.ndarray) -> np.ndarray:
    data = real_tree_data(theta_mag)
    return coordinate_gradient(data.state.astype(complex), data.derivatives, observable)


def complex_magnitude_gradient(
    theta_mag: np.ndarray, theta_ph: np.ndarray, observable: np.ndarray
) -> np.ndarray:
    psi = complex_state(theta_mag, theta_ph)
    return coordinate_gradient(
        psi, complex_magnitude_derivatives(theta_mag, theta_ph), observable
    )


def complex_phase_gradient(
    theta_mag: np.ndarray, theta_ph: np.ndarray, observable: np.ndarray
) -> np.ndarray:
    psi = complex_state(theta_mag, theta_ph)
    return coordinate_gradient(psi, complex_phase_derivatives(theta_mag, theta_ph), observable)


def complex_full_gradient(
    theta_mag: np.ndarray, theta_ph: np.ndarray, observable: np.ndarray
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


def _poly_reference_node(
    tree: PolyTree,
    angles: Mapping[str, float],
    dimension: int,
    incoming: float,
    data: dict[str, object],
) -> np.ndarray:
    if isinstance(tree, PolyLeaf):
        return basis_vector(dimension, tree.label, dtype=float)

    angle = float(angles[tree.key])
    left = _poly_reference_node(tree.left, angles, dimension, incoming * np.cos(angle), data)
    right = _poly_reference_node(tree.right, angles, dimension, incoming * np.sin(angle), data)
    c = float(np.cos(angle))
    s = float(np.sin(angle))
    state = c * left + s * right
    comp = -s * left + c * right

    sqrt_metric_map = data["sqrt_metric"]
    complements = data["complements"]
    derivatives = data["derivatives"]
    anchors = data["anchors"]
    markers = data["markers"]
    assert isinstance(sqrt_metric_map, dict)
    assert isinstance(complements, dict)
    assert isinstance(derivatives, dict)
    assert isinstance(anchors, dict)
    assert isinstance(markers, dict)
    sqrt_metric_map[tree.key] = float(incoming)
    complements[tree.key] = comp
    derivatives[tree.key] = float(incoming) * comp
    anchors[tree.key] = poly_anchor(tree)
    markers[tree.key] = poly_marker(tree)
    return state


def polyspherical_tree_data(
    tree: PolyTree, angles: Mapping[str, float], n: int
) -> PolyTreeData:
    validate_poly_tree(tree, n, angles)
    dimension = 1 << n
    data: dict[str, object] = {
        "sqrt_metric": {},
        "complements": {},
        "derivatives": {},
        "anchors": {},
        "markers": {},
    }
    state = _poly_reference_node(tree, angles, dimension, 1.0, data)
    return PolyTreeData(
        state=state,
        complements=data["complements"],  # type: ignore[arg-type]
        sqrt_metric=data["sqrt_metric"],  # type: ignore[arg-type]
        derivatives=data["derivatives"],  # type: ignore[arg-type]
        anchors=data["anchors"],  # type: ignore[arg-type]
        markers=data["markers"],  # type: ignore[arg-type]
    )


def polyspherical_frame_matrix(
    tree: PolyTree, angles: Mapping[str, float], n: int
) -> np.ndarray:
    data = polyspherical_tree_data(tree, angles, n)
    dimension = 1 << n
    root_anchor = poly_anchor(tree)
    frame = np.eye(dimension, dtype=float)
    encoded_labels = set(poly_leaves(tree))
    for label in encoded_labels:
        frame[:, label] = 0.0
    frame[:, root_anchor] = data.state
    for node in poly_preorder(tree):
        frame[:, poly_marker(node)] = data.complements[node.key]
    return frame


def polyspherical_shifted_frame_matrix(
    tree: PolyTree, angles: Mapping[str, float], n: int
) -> np.ndarray:
    frame = polyspherical_frame_matrix(tree, angles, n)
    dimension = 1 << n
    anchor = poly_anchor(tree)
    translation = np.zeros((dimension, dimension), dtype=float)
    for label in range(dimension):
        translation[label ^ anchor, label] = 1.0
    return frame @ translation


def polyspherical_gradient(
    tree: PolyTree, angles: Mapping[str, float], n: int, observable: np.ndarray
) -> dict[str, float]:
    data = polyspherical_tree_data(tree, angles, n)
    Opsi = observable @ data.state
    return {
        node.key: float(2.0 * np.real(np.vdot(data.derivatives[node.key], Opsi)))
        for node in poly_preorder(tree)
    }
