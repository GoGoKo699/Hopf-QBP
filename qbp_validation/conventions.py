"""Indexing, register, tree, and assigned-ledger conventions for Hopf-QBP.

This module deliberately contains no Qibo imports.  It is the shared source of
truth for the manuscript's breadth-first tree indexing, big-endian basis labels,
marker map, manuscript/Qibo wire translation, and exact assigned CNOT ledger.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterator, Mapping, TypeAlias

import numpy as np


@dataclass(frozen=True)
class FrameGateSpec:
    """One addressed-frame gate in ``W_R``.

    ``target`` is an index into the supplied Qibo system-register tuple, with
    index 0 the most-significant computational-basis qubit.
    """

    node: int
    depth: int
    position: int
    anchor: int
    marker: int
    target: int


@dataclass(frozen=True)
class DepthGateSpec:
    """One gate in a breadth-first checkpoint-preparation layer."""

    node: int
    depth: int
    position: int
    target: int


@dataclass(frozen=True)
class PolyLeaf:
    """A leaf encoded by one computational-basis label."""

    label: int


@dataclass(frozen=True)
class PolyBranch:
    """An ordered full-binary-tree internal node.

    ``key`` identifies the angle in an external mapping.  Keeping topology
    separate from numerical angles lets circuit and analytic paths consume the
    same immutable case without sharing state-vector code.
    """

    key: str
    left: "PolyTree"
    right: "PolyTree"


PolyTree: TypeAlias = PolyLeaf | PolyBranch


def infer_n_from_theta_mag(theta_mag: object) -> int:
    """Infer ``n`` from a magnitude block of length ``2**n - 1``."""

    length = len(theta_mag)  # type: ignore[arg-type]
    n_float = math.log2(length + 1)
    n = int(round(n_float))
    if n < 1 or (1 << n) - 1 != length:
        raise ValueError("theta_mag must have length 2**n - 1 with n >= 1.")
    return n


def split_theta(theta: object) -> tuple[np.ndarray, np.ndarray]:
    """Split the first-paper complex Hopf vector into magnitude and phase blocks.

    The full complex coordinate vector has length ``2**(n+1) - 1`` and ordering

    ``theta = (theta_1, ..., theta_{N-1}, theta_N, ..., theta_{2N-1})``.

    The returned arrays are ``theta_mag`` of length ``N-1`` and ``theta_ph`` of
    length ``N``.  The phase associated with leaf ``ell`` is
    ``theta_ph[ell] = theta_{N+ell}`` in one-based manuscript notation.
    """

    values = np.asarray(theta, dtype=float).reshape(-1)
    if values.size < 3:
        raise ValueError("A complex Hopf vector requires at least three parameters.")
    total_plus_one = values.size + 1
    if total_plus_one & (total_plus_one - 1):
        raise ValueError("Complex theta must have length 2**(n+1) - 1.")
    n = int(round(math.log2(total_plus_one))) - 1
    if n < 1 or 2 * (1 << n) - 1 != values.size:
        raise ValueError("Complex theta must have length 2**(n+1) - 1 with n >= 1.")
    N = 1 << n
    return values[: N - 1].copy(), values[N - 1 :].copy()


def join_theta(theta_mag: object, theta_ph: object) -> np.ndarray:
    """Join magnitude and phase blocks into the first-paper complex ordering."""

    mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    ph = np.asarray(theta_ph, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(mag)
    if ph.size != 1 << n:
        raise ValueError("theta_ph must contain one phase for every encoded leaf.")
    return np.concatenate((mag, ph))


def node_depth_position(node: int) -> tuple[int, int]:
    """Return ``(d, r)`` for the breadth-first node ``j = 2**d + r``."""

    if node < 1:
        raise ValueError("Internal-node indices start at 1.")
    depth = node.bit_length() - 1
    return depth, node - (1 << depth)


def anchor_label(node: int, n: int) -> int:
    """Return the leftmost basis label in the subtree rooted at ``node``."""

    depth, position = node_depth_position(node)
    if depth >= n:
        raise ValueError("Node is not internal for the requested qubit count.")
    return position << (n - depth)


def marker_label(node: int, n: int) -> int:
    """Return the nonzero computational-basis marker ``lambda(node)``."""

    depth, position = node_depth_position(node)
    if depth >= n:
        raise ValueError("Node is not internal for the requested qubit count.")
    return (2 * position + 1) << (n - depth - 1)


def frame_gate_specs(n: int) -> tuple[FrameGateSpec, ...]:
    """Return all addressed-frame gates in forward depth order."""

    if n < 1:
        raise ValueError("n must be positive.")
    specs: list[FrameGateSpec] = []
    for depth in range(n):
        for position in range(1 << depth):
            node = (1 << depth) + position
            specs.append(
                FrameGateSpec(
                    node=node,
                    depth=depth,
                    position=position,
                    anchor=anchor_label(node, n),
                    marker=marker_label(node, n),
                    target=depth,
                )
            )
    return tuple(specs)


def depth_gate_specs(n: int, depth: int | None = None) -> tuple[DepthGateSpec, ...]:
    """Return one or all breadth-first checkpoint-preparation layers."""

    if n < 1:
        raise ValueError("n must be positive.")
    depths = range(n) if depth is None else (depth,)
    specs: list[DepthGateSpec] = []
    for d in depths:
        if not 0 <= d < n:
            raise ValueError("Depth must lie in 0, ..., n-1.")
        for position in range(1 << d):
            specs.append(
                DepthGateSpec(
                    node=(1 << d) + position,
                    depth=d,
                    position=position,
                    target=d,
                )
            )
    return tuple(specs)


def bit_at(label: int, qibo_system_index: int, n: int) -> int:
    """Return one big-endian basis bit.

    Qibo system index 0 is the most-significant basis bit and corresponds to
    manuscript wire ``q_n``.  Qibo system index ``n-1`` corresponds to
    manuscript wire ``q_1``.
    """

    if not 0 <= qibo_system_index < n:
        raise ValueError("Qubit index out of range.")
    return (label >> (n - 1 - qibo_system_index)) & 1


def manuscript_wire_from_qibo_index(index: int, n: int) -> int:
    """Map Qibo system index ``i`` to the manuscript wire number ``q_{n-i}``."""

    if not 0 <= index < n:
        raise ValueError("Qibo system index out of range.")
    return n - index


def qibo_index_from_manuscript_wire(wire: int, n: int) -> int:
    """Map manuscript wire number ``q_k`` to Qibo system index ``n-k``."""

    if not 1 <= wire <= n:
        raise ValueError("Manuscript wire must lie in 1, ..., n.")
    return n - wire


def parity(label: int, outcome: int) -> int:
    """Return the mod-two inner product of two basis labels."""

    return (label & outcome).bit_count() & 1


def marker_map(n: int) -> dict[int, int]:
    """Return ``node -> lambda(node)`` for every internal Hopf node."""

    return {spec.node: spec.marker for spec in frame_gate_specs(n)}


def controlled_ry_cnot_charge(num_controls: int) -> int:
    """Assigned no-clean-ancilla CNOT charge for a controlled ``R_y``."""

    if num_controls < 0:
        raise ValueError("Number of controls must be nonnegative.")
    if num_controls == 0:
        return 0
    if num_controls <= 4:
        return (1 << (num_controls + 1)) - 2
    return 16 * (num_controls + 1) - 40


def controlled_rc_cnot_charge(num_controls: int) -> int:
    """Assigned no-clean-ancilla CNOT charge for a controlled ``R_C``."""

    if num_controls < 0:
        raise ValueError("Number of controls must be nonnegative.")
    if num_controls == 0:
        return 0
    if num_controls <= 4:
        return (1 << (num_controls + 1)) - 2
    gate_width = num_controls + 1
    return 20 * gate_width - 38 if gate_width % 2 else 20 * gate_width - 42


def controlled_su2_cnot_charge(num_controls: int) -> int:
    """Alias for the controlled special-unitary ``R_C`` ledger charge."""

    return controlled_rc_cnot_charge(num_controls)


def frame_cnot_charge(n: int) -> int:
    """Assigned charge of the fully addressed frame ``W_R``."""

    if n < 1:
        raise ValueError("n must be positive.")
    return ((1 << n) - 1) * controlled_ry_cnot_charge(n - 1)


def depth_layer_cnot_charge(depth: int) -> int:
    """Assigned charge of checkpoint preparation layer ``U_depth``."""

    if depth < 0:
        raise ValueError("Depth must be nonnegative.")
    return (1 << depth) * controlled_ry_cnot_charge(depth)


def depth_preparation_cnot_charge(n: int) -> int:
    """Assigned charge of ``U_chk``."""

    if n < 1:
        raise ValueError("n must be positive.")
    return sum(depth_layer_cnot_charge(d) for d in range(n))


def inverse_suffix_cnot_charge(n: int, depth: int) -> int:
    """Assigned charge of the inverse checkpoint suffix ``B_d^dagger``."""

    if not 0 <= depth < n:
        raise ValueError("Depth must lie in 0, ..., n-1.")
    return sum(depth_layer_cnot_charge(d) for d in range(depth + 1, n))


def checkpoint_cnot_charge_without_observable(n: int, depth: int) -> int:
    """Assigned real-checkpoint charge excluding the controlled observable."""

    if not 0 <= depth < n:
        raise ValueError("Depth must lie in 0, ..., n-1.")
    return depth_preparation_cnot_charge(n) + inverse_suffix_cnot_charge(n, depth)


def poly_preorder(tree: PolyTree) -> Iterator[PolyBranch]:
    if isinstance(tree, PolyLeaf):
        return
    yield tree
    yield from poly_preorder(tree.left)
    yield from poly_preorder(tree.right)


def poly_leaves(tree: PolyTree) -> tuple[int, ...]:
    if isinstance(tree, PolyLeaf):
        return (tree.label,)
    return poly_leaves(tree.left) + poly_leaves(tree.right)


def poly_anchor(tree: PolyTree) -> int:
    if isinstance(tree, PolyLeaf):
        return tree.label
    return poly_anchor(tree.left)


def poly_marker(node: PolyBranch) -> int:
    return poly_anchor(node.right)


def poly_relative_markers(tree: PolyTree) -> dict[str, int]:
    root_anchor = poly_anchor(tree)
    return {node.key: root_anchor ^ poly_marker(node) for node in poly_preorder(tree)}


def validate_poly_tree(tree: PolyTree, n: int, angles: Mapping[str, float]) -> None:
    labels = poly_leaves(tree)
    if len(labels) != len(set(labels)):
        raise ValueError("Polyspherical leaf labels must be distinct.")
    if any(label < 0 or label >= (1 << n) for label in labels):
        raise ValueError("Polyspherical leaf label outside the encoded space.")
    keys = [node.key for node in poly_preorder(tree)]
    if len(keys) != len(set(keys)):
        raise ValueError("Polyspherical internal-node keys must be unique.")
    missing = set(keys).difference(angles)
    if missing:
        raise ValueError(f"Missing angles for internal nodes: {sorted(missing)}")
