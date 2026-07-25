from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import complex_theta_mag, observables, regular_theta_mag, theta_ph
from qbp_validation.circuits import b2c_4q_circuit, probabilities, real_checkpoint_native_forward_circuit
from qbp_validation.conventions import (
    checkpoint_interface_projector,
    marker_map,
)
from qbp_validation.decoders import decode_checkpoint_gradient
from qbp_validation.reference import (
    complex_frame_matrix,
    depth_suffix_matrix,
    four_qubit_b2c_matrix,
    four_qubit_rc_phase_arguments,
    phase_layer_matrix,
    real_gradient,
    real_tree_data,
)


class FourQubitExampleTests(unittest.TestCase):
    def test_all_appendix_marker_labels(self) -> None:
        expected = {
            1: 0b1000,
            2: 0b0100,
            3: 0b1100,
            4: 0b0010,
            5: 0b0110,
            6: 0b1010,
            7: 0b1110,
            8: 0b0001,
            9: 0b0011,
            10: 0b0101,
            11: 0b0111,
            12: 0b1001,
            13: 0b1011,
            14: 0b1101,
            15: 0b1111,
        }
        self.assertEqual(marker_map(4), expected)

    def test_explicit_node_five_column_and_metric(self) -> None:
        theta = regular_theta_mag(4)
        data = real_tree_data(theta)
        expected = np.zeros(16, dtype=float)
        expected[0b0100] = -np.sin(theta[4]) * np.cos(theta[9])
        expected[0b0101] = -np.sin(theta[4]) * np.sin(theta[9])
        expected[0b0110] = np.cos(theta[4]) * np.cos(theta[10])
        expected[0b0111] = np.cos(theta[4]) * np.sin(theta[10])
        np.testing.assert_allclose(data.complements[5], expected, atol=2e-12, rtol=0.0)
        self.assertAlmostEqual(
            data.sqrt_metric[4], np.cos(theta[0]) * np.sin(theta[1]), places=12
        )

    def test_all_four_native_forward_checkpoint_settings(self) -> None:
        theta = regular_theta_mag(4)
        observable = observables(4)[-1]
        exact = real_gradient(theta, observable)
        for depth in range(4):
            decoded = decode_checkpoint_gradient(
                probabilities(
                    real_checkpoint_native_forward_circuit(theta, observable, depth)
                ),
                4,
                depth,
            )
            start = (1 << depth) - 1
            stop = (1 << (depth + 1)) - 1
            np.testing.assert_allclose(decoded, exact[start:stop], atol=3e-12, rtol=0.0)

    def test_b2c_eight_sectors_and_interface(self) -> None:
        mag = complex_theta_mag(4)
        phase = theta_ph(4)
        qibo = np.asarray(b2c_4q_circuit(mag, phase).unitary())
        reference = four_qubit_b2c_matrix(mag, phase)
        np.testing.assert_allclose(qibo, reference, atol=3e-12, rtol=0.0)
        projector = checkpoint_interface_projector(4, 2)
        separated = phase_layer_matrix(phase) @ depth_suffix_matrix(mag, 2)
        np.testing.assert_allclose(qibo @ projector, separated @ projector, atol=3e-12, rtol=0.0)
        self.assertGreater(float(np.max(np.abs(qibo - separated))), 1e-3)

    def test_addressed_rc_phase_argument_table(self) -> None:
        phase = theta_ph(4)
        centered = phase - np.mean(phase)
        arguments = four_qubit_rc_phase_arguments(phase)
        self.assertAlmostEqual(arguments[1][0], -float(np.sum(centered[8:16])))
        self.assertAlmostEqual(arguments[1][1], -float(np.sum(centered[0:8])))
        self.assertAlmostEqual(arguments[5][0], -float(np.sum(centered[6:8])))
        self.assertAlmostEqual(arguments[5][1], -float(np.sum(centered[4:6])))
        self.assertAlmostEqual(arguments[15][0], -float(centered[15]))
        self.assertAlmostEqual(arguments[15][1], -float(centered[14]))

    def test_complex_frame_is_unitary(self) -> None:
        mag = complex_theta_mag(4)
        phase = theta_ph(4)
        frame = complex_frame_matrix(mag, phase)
        np.testing.assert_allclose(frame.conj().T @ frame, np.eye(16), atol=3e-12, rtol=0.0)


if __name__ == "__main__":
    unittest.main()
