"""Qibo circuit builders for deterministic exact-logical validation.

The builders emit actual :class:`qibo.models.Circuit` objects.  Analytic state
and coordinate-derivative formulas live exclusively in :mod:`reference`.
"""
from __future__ import annotations

from typing import Mapping, Sequence

import numpy as np
from qibo import gates, models, set_backend

from .conventions import (
    PolyTree,
    bit_at,
    depth_gate_specs,
    frame_gate_specs,
    infer_n_from_theta_mag,
    poly_anchor,
    poly_preorder,
    validate_poly_tree,
)
from .native_schedule import (
    native_complex_schedule,
    native_real_schedule,
    qibo_index_from_target_mask,
    qibo_indices_from_mask,
)

set_backend("numpy")

SDG = np.asarray([[1.0, 0.0], [0.0, -1.0j]], dtype=complex)


def _controlled_ry_with_pattern(
    circuit: models.Circuit,
    target: int,
    controls: Sequence[int],
    control_values: Sequence[int],
    angle: float,
) -> None:
    if len(controls) != len(control_values):
        raise ValueError("Control qubits and values have different lengths.")
    if any(value not in (0, 1) for value in control_values):
        raise ValueError("Control values must be zero or one.")
    open_controls = [q for q, value in zip(controls, control_values) if value == 0]
    for qubit in open_controls:
        circuit.add(gates.X(qubit))
    gate = gates.RY(target, 2.0 * float(angle))
    if controls:
        gate = gate.controlled_by(*controls)
    circuit.add(gate)
    for qubit in reversed(open_controls):
        circuit.add(gates.X(qubit))


def _controlled_unitary_with_pattern(
    circuit: models.Circuit,
    target: int,
    controls: Sequence[int],
    control_values: Sequence[int],
    matrix: np.ndarray,
) -> None:
    """Append a one-qubit unitary with mixed positive and negative controls."""

    if len(controls) != len(control_values):
        raise ValueError("Control qubits and values have different lengths.")
    if any(value not in (0, 1) for value in control_values):
        raise ValueError("Control values must be zero or one.")
    open_controls = [q for q, value in zip(controls, control_values) if value == 0]
    for qubit in open_controls:
        circuit.add(gates.X(qubit))
    gate = gates.Unitary(np.asarray(matrix, dtype=complex), target)
    if controls:
        gate = gate.controlled_by(*controls)
    circuit.add(gate)
    for qubit in reversed(open_controls):
        circuit.add(gates.X(qubit))


def _rc_matrix(theta_a: float, theta_b: float, theta_c: float) -> np.ndarray:
    """Return the first paper's promoted final-layer gate ``R_C``."""

    c = float(np.cos(theta_a))
    s = float(np.sin(theta_a))
    return np.asarray(
        [
            [np.exp(1j * theta_b) * c, -np.exp(-1j * theta_c) * s],
            [np.exp(1j * theta_c) * s, np.exp(-1j * theta_b) * c],
        ],
        dtype=complex,
    )


def add_real_frame(
    circuit: models.Circuit,
    theta_mag: np.ndarray,
    system_qubits: Sequence[int],
    *,
    inverse: bool = False,
) -> None:
    """Append the fully addressed frame ``W_R`` or its inverse."""

    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta_mag)
    if len(system_qubits) != n:
        raise ValueError("System-qubit list length does not match theta_mag.")
    specs = list(frame_gate_specs(n))
    if inverse:
        specs.reverse()
    for spec in specs:
        target = system_qubits[spec.target]
        controls = [q for index, q in enumerate(system_qubits) if index != spec.target]
        values = [
            bit_at(spec.anchor, index, n)
            for index in range(n)
            if index != spec.target
        ]
        angle = -theta_mag[spec.node - 1] if inverse else theta_mag[spec.node - 1]
        _controlled_ry_with_pattern(circuit, target, controls, values, angle)


def add_depth_layer(
    circuit: models.Circuit,
    theta_mag: np.ndarray,
    system_qubits: Sequence[int],
    depth: int,
    *,
    inverse: bool = False,
) -> None:
    """Append one breadth-first checkpoint layer ``U_depth``."""

    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta_mag)
    if len(system_qubits) != n:
        raise ValueError("System-qubit list length does not match theta_mag.")
    for spec in depth_gate_specs(n, depth):
        controls = list(system_qubits[:depth])
        values = [
            (spec.position >> (depth - 1 - position)) & 1
            for position in range(depth)
        ]
        angle = -theta_mag[spec.node - 1] if inverse else theta_mag[spec.node - 1]
        _controlled_ry_with_pattern(
            circuit, system_qubits[depth], controls, values, angle
        )


def add_depth_preparation(
    circuit: models.Circuit,
    theta_mag: np.ndarray,
    system_qubits: Sequence[int],
) -> None:
    """Append ``U_chk = U_{n-1} ... U_0`` in state-update order."""

    n = infer_n_from_theta_mag(theta_mag)
    for depth in range(n):
        add_depth_layer(circuit, theta_mag, system_qubits, depth)


def add_inverse_depth_suffix(
    circuit: models.Circuit,
    theta_mag: np.ndarray,
    system_qubits: Sequence[int],
    selected_depth: int,
) -> None:
    """Append ``B_d^dagger`` for a checkpoint at depth ``d``."""

    n = infer_n_from_theta_mag(theta_mag)
    for depth in range(n - 1, selected_depth, -1):
        add_depth_layer(circuit, theta_mag, system_qubits, depth, inverse=True)


def add_native_real_preparation(
    circuit: models.Circuit,
    theta_mag: np.ndarray,
    system_qubits: Sequence[int],
) -> None:
    """Append the first paper's native ``HopfReal`` preparation schedule."""

    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta_mag)
    if len(system_qubits) != n:
        raise ValueError("System-qubit list length does not match theta_mag.")

    for spec in native_real_schedule(n):
        target_index = qibo_index_from_target_mask(spec.target_mask, n)
        target = system_qubits[target_index]
        control_mask = spec.ctrl_mask | spec.anti_mask
        control_indices = qibo_indices_from_mask(control_mask, n)
        controls = [system_qubits[index] for index in control_indices]
        values = [
            0 if spec.anti_mask & (1 << (n - 1 - index)) else 1
            for index in control_indices
        ]
        assert isinstance(spec.theta_index, int)
        _controlled_ry_with_pattern(
            circuit,
            target,
            controls,
            values,
            theta_mag[spec.theta_index - 1],
        )


def add_native_complex_preparation(
    circuit: models.Circuit,
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    system_qubits: Sequence[int],
) -> None:
    """Append the first paper's native ``HopfComplex`` schedule."""

    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    theta_ph = np.asarray(theta_ph, dtype=float).reshape(-1)
    n = infer_n_from_theta_mag(theta_mag)
    N = 1 << n
    if len(system_qubits) != n:
        raise ValueError("System-qubit list length does not match theta_mag.")
    if theta_ph.size != N:
        raise ValueError("theta_ph must contain one phase for every leaf.")

    for spec in native_complex_schedule(n):
        target_index = qibo_index_from_target_mask(spec.target_mask, n)
        target = system_qubits[target_index]
        control_mask = spec.ctrl_mask | spec.anti_mask
        control_indices = qibo_indices_from_mask(control_mask, n)
        controls = [system_qubits[index] for index in control_indices]
        values = [
            0 if spec.anti_mask & (1 << (n - 1 - index)) else 1
            for index in control_indices
        ]
        if isinstance(spec.theta_index, int):
            _controlled_ry_with_pattern(
                circuit, target, controls, values, theta_mag[spec.theta_index - 1]
            )
        else:
            magnitude_index, left_phase_index, right_phase_index = spec.theta_index
            _controlled_unitary_with_pattern(
                circuit,
                target,
                controls,
                values,
                _rc_matrix(
                    theta_mag[magnitude_index - 1],
                    theta_ph[left_phase_index - N],
                    theta_ph[right_phase_index - N],
                ),
            )


def add_phase_layer(
    circuit: models.Circuit,
    theta_ph: np.ndarray,
    system_qubits: Sequence[int],
    *,
    inverse: bool = False,
) -> None:
    """Append the exact diagonal leaf-phase layer ``D_ph`` or its inverse."""

    theta_ph = np.asarray(theta_ph, dtype=float).reshape(-1)
    if theta_ph.size != 1 << len(system_qubits):
        raise ValueError("theta_ph length does not match the system register.")
    sign = -1.0 if inverse else 1.0
    matrix = np.diag(np.exp(1j * sign * theta_ph))
    circuit.add(gates.Unitary(matrix, *system_qubits))


def add_controlled_observable(
    circuit: models.Circuit,
    observable: np.ndarray,
    ancilla: int,
    system_qubits: Sequence[int],
) -> None:
    observable = np.asarray(observable, dtype=complex)
    N = 1 << len(system_qubits)
    if observable.shape != (N, N):
        raise ValueError("Observable dimension does not match system register.")
    circuit.add(gates.Unitary(observable, *system_qubits).controlled_by(ancilla))


def add_x_basis_rotation(circuit: models.Circuit, qubits: Sequence[int]) -> None:
    for qubit in qubits:
        circuit.add(gates.H(qubit))


def add_y_basis_rotation(circuit: models.Circuit, qubit: int) -> None:
    # State-update order is S^dagger followed by H, hence the net matrix H S^dagger.
    circuit.add(gates.Unitary(SDG, qubit))
    circuit.add(gates.H(qubit))


def frame_circuit(theta_mag: np.ndarray, *, inverse: bool = False) -> models.Circuit:
    n = infer_n_from_theta_mag(theta_mag)
    circuit = models.Circuit(n)
    add_real_frame(circuit, theta_mag, tuple(range(n)), inverse=inverse)
    return circuit


def depth_preparation_circuit(theta_mag: np.ndarray) -> models.Circuit:
    n = infer_n_from_theta_mag(theta_mag)
    circuit = models.Circuit(n)
    add_depth_preparation(circuit, theta_mag, tuple(range(n)))
    return circuit


def native_real_circuit(theta_mag: np.ndarray) -> models.Circuit:
    """Return the inherited native ``HopfReal`` circuit."""

    n = infer_n_from_theta_mag(theta_mag)
    circuit = models.Circuit(n)
    add_native_real_preparation(circuit, theta_mag, tuple(range(n)))
    return circuit


def native_complex_circuit(
    theta_mag: np.ndarray, theta_ph: np.ndarray
) -> models.Circuit:
    """Return the inherited native ``HopfComplex`` circuit."""

    n = infer_n_from_theta_mag(theta_mag)
    circuit = models.Circuit(n)
    add_native_complex_preparation(circuit, theta_mag, theta_ph, tuple(range(n)))
    return circuit


native_real_preparation_circuit = native_real_circuit


def real_global_measurement_circuit(
    theta_mag: np.ndarray, observable: np.ndarray
) -> models.Circuit:
    n = infer_n_from_theta_mag(theta_mag)
    ancilla = 0
    system = tuple(range(1, n + 1))
    circuit = models.Circuit(n + 1)
    circuit.add(gates.H(ancilla))
    add_real_frame(circuit, theta_mag, system)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_real_frame(circuit, theta_mag, system, inverse=True)
    add_x_basis_rotation(circuit, (ancilla, *system))
    return circuit


def complex_magnitude_measurement_circuit(
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    observable: np.ndarray,
) -> models.Circuit:
    """Build the asymmetric complex-magnitude global circuit.

    The forward branch uses ``U_chk`` while the decoder uses ``W_R^dagger``:

    ``U_chk -> D_ph -> ctrl(O) -> D_ph^dagger -> W_R^dagger``.
    """

    n = infer_n_from_theta_mag(theta_mag)
    ancilla = 0
    system = tuple(range(1, n + 1))
    circuit = models.Circuit(n + 1)
    circuit.add(gates.H(ancilla))
    add_depth_preparation(circuit, theta_mag, system)
    add_phase_layer(circuit, theta_ph, system)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_phase_layer(circuit, theta_ph, system, inverse=True)
    add_real_frame(circuit, theta_mag, system, inverse=True)
    add_x_basis_rotation(circuit, (ancilla, *system))
    return circuit


def complex_phase_measurement_circuit(
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    observable: np.ndarray,
) -> models.Circuit:
    """Build the direct phase family with ``U_chk`` on the forward branch."""

    n = infer_n_from_theta_mag(theta_mag)
    ancilla = 0
    system = tuple(range(1, n + 1))
    circuit = models.Circuit(n + 1)
    circuit.add(gates.H(ancilla))
    add_depth_preparation(circuit, theta_mag, system)
    add_phase_layer(circuit, theta_ph, system)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_y_basis_rotation(circuit, ancilla)
    return circuit


def real_checkpoint_measurement_circuit(
    theta_mag: np.ndarray,
    observable: np.ndarray,
    depth: int,
) -> models.Circuit:
    n = infer_n_from_theta_mag(theta_mag)
    if not 0 <= depth < n:
        raise ValueError("Depth must lie in 0, ..., n-1.")
    ancilla = 0
    system = tuple(range(1, n + 1))
    circuit = models.Circuit(n + 1)
    circuit.add(gates.H(ancilla))
    add_depth_preparation(circuit, theta_mag, system)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_inverse_depth_suffix(circuit, theta_mag, system, depth)
    add_y_basis_rotation(circuit, ancilla)
    add_y_basis_rotation(circuit, system[depth])
    return circuit


def complex_checkpoint_measurement_circuit(
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    observable: np.ndarray,
    depth: int,
) -> models.Circuit:
    n = infer_n_from_theta_mag(theta_mag)
    if not 0 <= depth < n:
        raise ValueError("Depth must lie in 0, ..., n-1.")
    ancilla = 0
    system = tuple(range(1, n + 1))
    circuit = models.Circuit(n + 1)
    circuit.add(gates.H(ancilla))
    add_depth_preparation(circuit, theta_mag, system)
    add_phase_layer(circuit, theta_ph, system)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_phase_layer(circuit, theta_ph, system, inverse=True)
    add_inverse_depth_suffix(circuit, theta_mag, system, depth)
    add_y_basis_rotation(circuit, ancilla)
    add_y_basis_rotation(circuit, system[depth])
    return circuit


def _two_level_rotation(
    dimension: int, first: int, second: int, angle: float
) -> np.ndarray:
    matrix = np.eye(dimension, dtype=complex)
    c = float(np.cos(angle))
    s = float(np.sin(angle))
    matrix[first, first] = c
    matrix[second, first] = s
    matrix[first, second] = -s
    matrix[second, second] = c
    return matrix


def _add_poly_translation(
    circuit: models.Circuit, system_qubits: Sequence[int], label: int
) -> None:
    n = len(system_qubits)
    for index, qubit in enumerate(system_qubits):
        if bit_at(label, index, n):
            circuit.add(gates.X(qubit))


def add_polyspherical_frame(
    circuit: models.Circuit,
    tree: PolyTree,
    angles: Mapping[str, float],
    system_qubits: Sequence[int],
    *,
    shifted: bool = True,
    inverse: bool = False,
) -> None:
    n = len(system_qubits)
    validate_poly_tree(tree, n, angles)
    nodes = list(poly_preorder(tree))
    dimension = 1 << n
    if not inverse:
        if shifted:
            _add_poly_translation(circuit, system_qubits, poly_anchor(tree))
        for node in nodes:
            matrix = _two_level_rotation(
                dimension,
                poly_anchor(node.left),
                poly_anchor(node.right),
                float(angles[node.key]),
            )
            circuit.add(gates.Unitary(matrix, *system_qubits))
    else:
        for node in reversed(nodes):
            matrix = _two_level_rotation(
                dimension,
                poly_anchor(node.left),
                poly_anchor(node.right),
                -float(angles[node.key]),
            )
            circuit.add(gates.Unitary(matrix, *system_qubits))
        if shifted:
            _add_poly_translation(circuit, system_qubits, poly_anchor(tree))


def polyspherical_frame_circuit(
    tree: PolyTree,
    angles: Mapping[str, float],
    n: int,
    *,
    shifted: bool = True,
) -> models.Circuit:
    circuit = models.Circuit(n)
    add_polyspherical_frame(circuit, tree, angles, tuple(range(n)), shifted=shifted)
    return circuit


def polyspherical_global_measurement_circuit(
    tree: PolyTree,
    angles: Mapping[str, float],
    n: int,
    observable: np.ndarray,
) -> models.Circuit:
    ancilla = 0
    system = tuple(range(1, n + 1))
    circuit = models.Circuit(n + 1)
    circuit.add(gates.H(ancilla))
    add_polyspherical_frame(circuit, tree, angles, system, shifted=True)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_polyspherical_frame(circuit, tree, angles, system, shifted=True, inverse=True)
    add_x_basis_rotation(circuit, (ancilla, *system))
    return circuit


def statevector(circuit: models.Circuit) -> np.ndarray:
    result = circuit()
    return np.asarray(result.state(), dtype=complex).reshape(-1)


def probabilities(circuit: models.Circuit) -> np.ndarray:
    state = statevector(circuit)
    probs = np.abs(state) ** 2
    probs /= probs.sum()
    return probs
