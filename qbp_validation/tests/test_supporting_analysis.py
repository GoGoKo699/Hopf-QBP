from __future__ import annotations

import math
import unittest

import numpy as np

from qbp_validation.supporting_analysis import (
    checkpoint_sign_readout_attenuation,
    complete_magnitude_l2_shot_bound,
    complete_magnitude_record_norm,
    descent_direction_is_guaranteed,
    direction_error_upper_bound,
    fixed_norm_vector_shot_bound,
    global_marker_readout_attenuation,
    independent_bitflip_channel,
    phase_sign_readout_attenuation,
    project_common_phase_gradient,
    reflection_sampling_probabilities,
    reflection_sum_expected_record,
    reflection_sum_record_norm_bound,
)


class SupportingAnalysisTests(unittest.TestCase):
    def test_complete_magnitude_record_norm_and_shot_bound(self) -> None:
        for n in range(1, 8):
            self.assertAlmostEqual(complete_magnitude_record_norm(n), 2.0 * math.sqrt(n))
        eta = 0.05
        epsilon = 0.2
        expected = math.ceil(
            4.0 * 5.0 * (1.0 + math.sqrt(2.0 * math.log(1.0 / eta))) ** 2
            / epsilon**2
        )
        self.assertEqual(complete_magnitude_l2_shot_bound(5, epsilon, eta), expected)
        self.assertEqual(
            fixed_norm_vector_shot_bound(2.0, epsilon, eta),
            math.ceil(
                4.0 * (1.0 + math.sqrt(2.0 * math.log(1.0 / eta))) ** 2
                / epsilon**2
            ),
        )

    def test_directional_guarantees_require_nonzero_gradient(self) -> None:
        self.assertTrue(descent_direction_is_guaranteed(2.0, 0.5))
        self.assertFalse(descent_direction_is_guaranteed(2.0, 2.0))
        self.assertFalse(descent_direction_is_guaranteed(0.0, 0.0))
        self.assertAlmostEqual(direction_error_upper_bound(2.0, 0.5), 0.5)
        with self.assertRaises(ValueError):
            direction_error_upper_bound(0.0, 0.0)
        with self.assertRaises(ValueError):
            direction_error_upper_bound(1.0, 1.0)

    def test_common_phase_projection_is_unbiased_and_nonexpansive(self) -> None:
        true_gradient = np.asarray([0.7, -0.4, 0.2, -0.5])
        estimate = true_gradient + np.asarray([0.2, -0.1, 0.3, 0.4])
        projected = project_common_phase_gradient(estimate)
        self.assertAlmostEqual(float(np.sum(projected)), 0.0, places=14)
        self.assertLessEqual(
            float(np.linalg.norm(projected - true_gradient)),
            float(np.linalg.norm(estimate - true_gradient)) + 1e-14,
        )

    def test_reflection_term_sampling_is_unbiased(self) -> None:
        coefficients = np.asarray([1.5, -0.5, 2.0])
        term_records = np.asarray(
            [
                [0.2, -0.4, 0.1],
                [0.8, 0.3, -0.2],
                [-0.5, 0.6, 0.9],
            ]
        )
        probabilities = reflection_sampling_probabilities(coefficients)
        np.testing.assert_allclose(probabilities, [0.375, 0.125, 0.5])
        expected = reflection_sum_expected_record(coefficients, term_records)
        np.testing.assert_allclose(expected, coefficients @ term_records, atol=1e-14)
        self.assertEqual(reflection_sum_record_norm_bound(4.0), 8.0)

    def test_readout_transfer_functions(self) -> None:
        marker = 0b1010
        system_errors = [0.01, 0.02, 0.03, 0.04]
        expected = (1.0 - 2.0 * 0.05) * (1.0 - 2.0 * 0.01) * (1.0 - 2.0 * 0.03)
        self.assertAlmostEqual(
            global_marker_readout_attenuation(marker, 4, 0.05, system_errors),
            expected,
        )
        self.assertAlmostEqual(
            checkpoint_sign_readout_attenuation(0.05, 0.02),
            (1.0 - 0.10) * (1.0 - 0.04),
        )
        self.assertAlmostEqual(phase_sign_readout_attenuation(0.05), 0.9)

        channel = independent_bitflip_channel([0.1, 0.2])
        np.testing.assert_allclose(np.sum(channel, axis=0), 1.0, atol=1e-14)
        np.testing.assert_allclose(np.sum(channel, axis=1), 1.0, atol=1e-14)


if __name__ == "__main__":
    unittest.main()
