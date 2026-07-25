"""Qibo circuit builders for deterministic exact-logical Hopf-QBP validation.

The builders emit actual :class:`qibo.models.Circuit` objects. Analytic states,
frames, derivatives, and interface matrices live exclusively in :mod:`reference`.
"""
from __future__ import annotations

from typing import Sequence

import numpy as np
from qibo import gates, models, set_backend

from .conventions import bit_at, depth_gate_specs, frame_gate_specs, infer_n_from_theta_mag
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
    """Append the fully addressed real frame ``W_R`` or its inverse."""

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
    """Append the exact diagonal leaf-phase unitary ``D_ph`` or its inverse."""

    theta_ph = np.asarray(theta_ph, dtype=float).reshape(-1)
    if theta_ph.size != 1 << len(system_qubits):
        raise ValueError("theta_ph length does not match the system register.")
    sign = -1.0 if inverse else 1.0
    matrix = np.diag(np.exp(1j * sign * theta_ph))
    circuit.add(gates.Unitary(matrix, *system_qubits))


def add_complex_frame_separated(
    circuit: models.Circuit,
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    system_qubits: Sequence[int],
    *,
    inverse: bool = False,
) -> None:
    """Append ``W_C = D_ph W_R`` or ``W_C^dagger`` using separated blocks."""

    if inverse:
        add_phase_layer(circuit, theta_ph, system_qubits, inverse=True)
        add_real_frame(circuit, theta_mag, system_qubits, inverse=True)
    else:
        add_real_frame(circuit, theta_mag, system_qubits)
        add_phase_layer(circuit, theta_ph, system_qubits)


def _four_qubit_rc_arguments(theta_ph: np.ndarray) -> dict[int, tuple[float, float]]:
    """Circuit-side construction of the Appendix-A addressed ``R_C`` phases."""

    phase = np.asarray(theta_ph, dtype=float).reshape(-1)
    if phase.size != 16:
        raise ValueError("The addressed R_C compiler is four-qubit only.")
    centered = phase - float(np.mean(phase))
    sums = np.zeros(32, dtype=float)
    sums[16:32] = centered
    for node in range(15, 0, -1):
        sums[node] = sums[2 * node] + sums[2 * node + 1]
    return {
        node: (-float(sums[2 * node + 1]), -float(sums[2 * node]))
        for node in range(1, 16)
    }


def add_complex_frame_rc_4q(
    circuit: models.Circuit,
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    system_qubits: Sequence[int],
    *,
    inverse: bool = False,
) -> None:
    """Append the Appendix-A addressed ``R_C`` compiler of ``W_C``.

    As a complete matrix this implementation is ``exp(-i mean(theta_ph)) W_C``.
    Its inverse therefore implements ``W_C^dagger`` up to the conjugate common
    phase, which is applied to both interference branches.
    """

    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    theta_ph = np.asarray(theta_ph, dtype=float).reshape(-1)
    if theta_mag.size != 15 or theta_ph.size != 16 or len(system_qubits) != 4:
        raise ValueError("The addressed R_C compiler is four-qubit only.")
    arguments = _four_qubit_rc_arguments(theta_ph)
    specs = list(frame_gate_specs(4))
    if inverse:
        specs.reverse()
    for spec in specs:
        target = system_qubits[spec.target]
        controls = [q for index, q in enumerate(system_qubits) if index != spec.target]
        values = [
            bit_at(spec.anchor, index, 4)
            for index in range(4)
            if index != spec.target
        ]
        alpha, beta = arguments[spec.node]
        matrix = _rc_matrix(theta_mag[spec.node - 1], alpha, beta)
        if inverse:
            matrix = matrix.conj().T
        _controlled_unitary_with_pattern(circuit, target, controls, values, matrix)


def add_b2c_4q(
    circuit: models.Circuit,
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    system_qubits: Sequence[int],
    *,
    inverse: bool = False,
) -> None:
    """Append the Appendix-A complex depth-2 suffix ``B_{2,C}`` or its inverse."""

    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    theta_ph = np.asarray(theta_ph, dtype=float).reshape(-1)
    if theta_mag.size != 15 or theta_ph.size != 16 or len(system_qubits) != 4:
        raise ValueError("B_{2,C} is defined here for the four-qubit example.")
    target = system_qubits[3]  # manuscript q_1
    controls = list(system_qubits[:3])
    prefixes = list(range(8))
    if inverse:
        prefixes.reverse()
    for prefix in prefixes:
        values = [(prefix >> (2 - position)) & 1 for position in range(3)]
        matrix = _rc_matrix(
            theta_mag[7 + prefix], theta_ph[2 * prefix], theta_ph[2 * prefix + 1]
        )
        if inverse:
            matrix = matrix.conj().T
        _controlled_unitary_with_pattern(circuit, target, controls, values, matrix)


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
    # State-update order is S^dagger then H, hence net matrix H S^dagger.
    circuit.add(gates.Unitary(SDG, qubit))
    circuit.add(gates.H(qubit))


def frame_circuit(theta_mag: np.ndarray, *, inverse: bool = False) -> models.Circuit:
    n = infer_n_from_theta_mag(theta_mag)
    circuit = models.Circuit(n)
    add_real_frame(circuit, theta_mag, tuple(range(n)), inverse=inverse)
    return circuit


def complex_frame_separated_circuit(
    theta_mag: np.ndarray, theta_ph: np.ndarray, *, inverse: bool = False
) -> models.Circuit:
    n = infer_n_from_theta_mag(theta_mag)
    circuit = models.Circuit(n)
    add_complex_frame_separated(
        circuit, theta_mag, theta_ph, tuple(range(n)), inverse=inverse
    )
    return circuit


def complex_frame_rc_4q_circuit(
    theta_mag: np.ndarray, theta_ph: np.ndarray, *, inverse: bool = False
) -> models.Circuit:
    circuit = models.Circuit(4)
    add_complex_frame_rc_4q(
        circuit, theta_mag, theta_ph, tuple(range(4)), inverse=inverse
    )
    return circuit


def b2c_4q_circuit(
    theta_mag: np.ndarray, theta_ph: np.ndarray, *, inverse: bool = False
) -> models.Circuit:
    circuit = models.Circuit(4)
    add_b2c_4q(circuit, theta_mag, theta_ph, tuple(range(4)), inverse=inverse)
    return circuit


def depth_preparation_circuit(theta_mag: np.ndarray) -> models.Circuit:
    n = infer_n_from_theta_mag(theta_mag)
    circuit = models.Circuit(n)
    add_depth_preparation(circuit, theta_mag, tuple(range(n)))
    return circuit


def native_real_circuit(theta_mag: np.ndarray) -> models.Circuit:
    n = infer_n_from_theta_mag(theta_mag)
    circuit = models.Circuit(n)
    add_native_real_preparation(circuit, theta_mag, tuple(range(n)))
    return circuit


def native_complex_circuit(
    theta_mag: np.ndarray, theta_ph: np.ndarray
) -> models.Circuit:
    n = infer_n_from_theta_mag(theta_mag)
    circuit = models.Circuit(n)
    add_native_complex_preparation(circuit, theta_mag, theta_ph, tuple(range(n)))
    return circuit


native_real_preparation_circuit = native_real_circuit


def real_global_measurement_circuit(
    theta_mag: np.ndarray, observable: np.ndarray
) -> models.Circuit:
    """Global real circuit using ``W_R`` on both sides."""

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


def real_global_native_forward_circuit(
    theta_mag: np.ndarray, observable: np.ndarray
) -> models.Circuit:
    """Global real circuit with native ``HopfReal`` forward preparation."""

    n = infer_n_from_theta_mag(theta_mag)
    ancilla = 0
    system = tuple(range(1, n + 1))
    circuit = models.Circuit(n + 1)
    circuit.add(gates.H(ancilla))
    add_native_real_preparation(circuit, theta_mag, system)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_real_frame(circuit, theta_mag, system, inverse=True)
    add_x_basis_rotation(circuit, (ancilla, *system))
    return circuit


def complex_magnitude_separated_circuit(
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    observable: np.ndarray,
) -> models.Circuit:
    """Designated separated complex-magnitude global circuit.

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


complex_magnitude_measurement_circuit = complex_magnitude_separated_circuit


def complex_magnitude_integrated_4q_circuit(
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    observable: np.ndarray,
) -> models.Circuit:
    """Four-qubit native-forward circuit with the addressed ``W_C^dagger`` decoder."""

    if infer_n_from_theta_mag(theta_mag) != 4:
        raise ValueError("The integrated addressed W_C circuit is four-qubit only.")
    ancilla = 0
    system = tuple(range(1, 5))
    circuit = models.Circuit(5)
    circuit.add(gates.H(ancilla))
    add_native_complex_preparation(circuit, theta_mag, theta_ph, system)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_complex_frame_rc_4q(circuit, theta_mag, theta_ph, system, inverse=True)
    add_x_basis_rotation(circuit, (ancilla, *system))
    return circuit


def complex_phase_measurement_circuit(
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    observable: np.ndarray,
) -> models.Circuit:
    """Direct phase family with the designated ``D_ph U_chk`` forward circuit."""

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


def complex_phase_native_forward_circuit(
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    observable: np.ndarray,
) -> models.Circuit:
    """Direct phase family with native ``HopfComplex`` forward preparation."""

    n = infer_n_from_theta_mag(theta_mag)
    ancilla = 0
    system = tuple(range(1, n + 1))
    circuit = models.Circuit(n + 1)
    circuit.add(gates.H(ancilla))
    add_native_complex_preparation(circuit, theta_mag, theta_ph, system)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_y_basis_rotation(circuit, ancilla)
    return circuit


def real_checkpoint_measurement_circuit(
    theta_mag: np.ndarray,
    observable: np.ndarray,
    depth: int,
) -> models.Circuit:
    """Designated real checkpoint with ``U_chk`` forward preparation."""

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


def real_checkpoint_native_forward_circuit(
    theta_mag: np.ndarray,
    observable: np.ndarray,
    depth: int,
) -> models.Circuit:
    """Real checkpoint using native ``HopfReal`` forward preparation."""

    n = infer_n_from_theta_mag(theta_mag)
    if not 0 <= depth < n:
        raise ValueError("Depth must lie in 0, ..., n-1.")
    ancilla = 0
    system = tuple(range(1, n + 1))
    circuit = models.Circuit(n + 1)
    circuit.add(gates.H(ancilla))
    add_native_real_preparation(circuit, theta_mag, system)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_inverse_depth_suffix(circuit, theta_mag, system, depth)
    add_y_basis_rotation(circuit, ancilla)
    add_y_basis_rotation(circuit, system[depth])
    return circuit


def complex_checkpoint_separated_circuit(
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    observable: np.ndarray,
    depth: int,
) -> models.Circuit:
    """Designated separated complex checkpoint at arbitrary depth."""

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


complex_checkpoint_measurement_circuit = complex_checkpoint_separated_circuit


def complex_checkpoint_integrated_depth2_4q_circuit(
    theta_mag: np.ndarray,
    theta_ph: np.ndarray,
    observable: np.ndarray,
) -> models.Circuit:
    """Four-qubit native-forward checkpoint using ``B_{2,C}^dagger``."""

    if infer_n_from_theta_mag(theta_mag) != 4:
        raise ValueError("The integrated B_{2,C} circuit is four-qubit only.")
    ancilla = 0
    system = tuple(range(1, 5))
    circuit = models.Circuit(5)
    circuit.add(gates.H(ancilla))
    add_native_complex_preparation(circuit, theta_mag, theta_ph, system)
    add_controlled_observable(circuit, observable, ancilla, system)
    add_b2c_4q(circuit, theta_mag, theta_ph, system, inverse=True)
    add_y_basis_rotation(circuit, ancilla)
    add_y_basis_rotation(circuit, system[2])  # manuscript target q_2
    return circuit


def statevector(circuit: models.Circuit) -> np.ndarray:
    result = circuit()
    return np.asarray(result.state(), dtype=complex).reshape(-1)


def probabilities(circuit: models.Circuit) -> np.ndarray:
    state = statevector(circuit)
    probs = np.abs(state) ** 2
    probs /= probs.sum()
    return probs
