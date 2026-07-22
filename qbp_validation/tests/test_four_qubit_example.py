from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import observables, regular_theta_mag
from qbp_validation.circuits import probabilities, real_checkpoint_measurement_circuit
from qbp_validation.conventions import marker_map
from qbp_validation.decoders import decode_checkpoint_gradient
from qbp_validation.native_schedule import native_real_cnot_charge
from qbp_validation.reference import real_gradient, real_tree_data


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
        theta_mag = regular_theta_mag(4)
        data = real_tree_data(theta_mag)
        expected = np.zeros(16, dtype=float)
        expected[0b0100] = -np.sin(theta_mag[4]) * np.cos(theta_mag[9])
        expected[0b0101] = -np.sin(theta_mag[4]) * np.sin(theta_mag[9])
        expected[0b0110] = np.cos(theta_mag[4]) * np.cos(theta_mag[10])
        expected[0b0111] = np.cos(theta_mag[4]) * np.sin(theta_mag[10])
        np.testing.assert_allclose(
            data.complements[5], expected, atol=2e-12, rtol=0.0
        )
        self.assertAlmostEqual(
            data.sqrt_metric[4],
            np.cos(theta_mag[0]) * np.sin(theta_mag[1]),
            places=12,
        )

    def test_all_four_checkpoint_settings(self) -> None:
        theta_mag = regular_theta_mag(4)
        observable = observables(4)[-1]
        exact = real_gradient(theta_mag, observable)
        for depth in range(4):
            decoded = decode_checkpoint_gradient(
                probabilities(
                    real_checkpoint_measurement_circuit(
                        theta_mag, observable, depth
                    )
                ),
                4,
                depth,
            )
            start = (1 << depth) - 1
            stop = (1 << (depth + 1)) - 1
            np.testing.assert_allclose(
                decoded, exact[start:stop], atol=3e-12, rtol=0.0
            )

    def test_native_real_charge_is_one_hundred(self) -> None:
        self.assertEqual(native_real_cnot_charge(4), 100)


if __name__ == "__main__":
    unittest.main()
