from __future__ import annotations

import unittest

import numpy as np
from qibo import models

from qbp_validation.cases import complex_theta_mag, observables, regular_theta_mag, theta_ph
from qbp_validation.circuits import (
    add_depth_preparation,
    add_phase_layer,
    b2c_4q_circuit,
    complex_checkpoint_integrated_depth2_4q_circuit,
    complex_checkpoint_separated_circuit,
    complex_frame_rc_4q_circuit,
    complex_frame_separated_circuit,
    depth_preparation_circuit,
    frame_circuit,
    native_complex_circuit,
    native_real_circuit,
    probabilities,
)
from qbp_validation.conventions import checkpoint_interface_projector
from qbp_validation.decoders import decode_checkpoint_gradient
from qbp_validation.reference import (
    complex_magnitude_gradient,
    complex_state,
    depth_suffix_matrix,
    phase_layer_matrix,
    real_state,
)


class OperatorContractTests(unittest.TestCase):
    def test_real_native_depth_and_frame_share_only_state_column(self) -> None:
        theta = regular_theta_mag(4)
        reference_state = real_state(theta)
        native = np.asarray(native_real_circuit(theta).unitary())
        checkpoint = np.asarray(depth_preparation_circuit(theta).unitary())
        addressed = np.asarray(frame_circuit(theta).unitary())
        for unitary in (native, checkpoint, addressed):
            np.testing.assert_allclose(unitary[:, 0], reference_state, atol=3e-12, rtol=0.0)
        self.assertGreater(float(np.max(np.abs(addressed - checkpoint))), 1e-3)
        self.assertGreater(float(np.max(np.abs(native - checkpoint))), 1e-3)

    def test_complex_exact_forward_columns_and_integrated_global_phase(self) -> None:
        mag = complex_theta_mag(4)
        phase = theta_ph(4)
        reference_state = complex_state(mag, phase)

        native = np.asarray(native_complex_circuit(mag, phase).unitary())
        separated = np.asarray(complex_frame_separated_circuit(mag, phase).unitary())
        depth_then_phase = models.Circuit(4)
        system = tuple(range(4))
        add_depth_preparation(depth_then_phase, mag, system)
        add_phase_layer(depth_then_phase, phase, system)
        depth_then_phase_u = np.asarray(depth_then_phase.unitary())

        for unitary in (native, separated, depth_then_phase_u):
            np.testing.assert_allclose(unitary[:, 0], reference_state, atol=3e-12, rtol=0.0)
        self.assertGreater(float(np.max(np.abs(native - separated))), 1e-3)

        integrated = np.asarray(complex_frame_rc_4q_circuit(mag, phase).unitary())
        overlap = np.vdot(reference_state, integrated[:, 0])
        self.assertGreater(abs(overlap), 1.0 - 1e-12)

    def test_b2c_interface_equality_without_full_unitary_equality(self) -> None:
        mag = complex_theta_mag(4)
        phase = theta_ph(4)
        b2c = np.asarray(b2c_4q_circuit(mag, phase).unitary())
        separated = phase_layer_matrix(phase) @ depth_suffix_matrix(mag, 2)
        projector = checkpoint_interface_projector(4, 2)
        np.testing.assert_allclose(
            b2c @ projector, separated @ projector, atol=3e-12, rtol=0.0
        )
        self.assertGreater(float(np.max(np.abs(b2c - separated))), 1e-3)

    def test_checkpoint_interface_preserves_means_not_complete_distributions(self) -> None:
        mag = complex_theta_mag(4)
        phase = theta_ph(4)
        observable = observables(4)[-1]
        separated = probabilities(
            complex_checkpoint_separated_circuit(mag, phase, observable, 2)
        )
        integrated = probabilities(
            complex_checkpoint_integrated_depth2_4q_circuit(mag, phase, observable)
        )
        total_variation = 0.5 * float(np.sum(np.abs(separated - integrated)))
        self.assertGreater(total_variation, 1e-6)

        separated_gradient = decode_checkpoint_gradient(separated, 4, 2)
        integrated_gradient = decode_checkpoint_gradient(integrated, 4, 2)
        exact = complex_magnitude_gradient(mag, phase, observable)[3:7]
        np.testing.assert_allclose(separated_gradient, exact, atol=3e-12, rtol=0.0)
        np.testing.assert_allclose(integrated_gradient, exact, atol=3e-12, rtol=0.0)
        np.testing.assert_allclose(
            separated_gradient, integrated_gradient, atol=3e-12, rtol=0.0
        )


if __name__ == "__main__":
    unittest.main()
