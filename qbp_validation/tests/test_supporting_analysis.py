from __future__ import annotations

import math
import unittest

import numpy as np

from qbp_validation.supporting_analysis import (
    ambient_phase_metric,
    checkpoint_sign_readout_attenuation,
    complete_frame_record_norm,
    complete_magnitude_l2_shot_bound,
    complete_magnitude_record_norm,
    complete_magnitude_relative_l2_shot_bound,
    descent_direction_is_guaranteed,
    direction_error_upper_bound,
    fixed_norm_vector_shot_bound,
    global_marker_readout_attenuation,
    independent_bitflip_channel,
    natural_gradient_coordinate_record_bound,
    natural_gradient_record_second_moment,
    ordinary_magnitude_record_second_moment,
    phase_sign_readout_attenuation,
    project_common_phase_gradient,
    projective_phase_metric,
    reflection_sampling_probabilities,
    reflection_sum_expected_record,
    reflection_sum_record_norm_bound,
    regularized_natural_gradient_coordinate_record_bound,
    regularized_natural_gradient_record_second_moment,
    regularized_natural_gradient_second_moment_bound,
    swap_reflection,
)


class SupportingAnalysisTests(unittest.TestCase):
    def test_complete_magnitude_record_norm_and_shot_bound(self) -> None:
        for n in range(1, 8):
            self.assertAlmostEqual(
                complete_magnitude_record_norm(n),
                2.0 * math.sqrt(n),
            )
        eta = 0.05
        epsilon = 0.2
        expected = math.ceil(
            4.0
            * 5.0
            * (1.0 + math.sqrt(2.0 * math.log(1.0 / eta))) ** 2
            / epsilon**2
        )
        self.assertEqual(
            complete_magnitude_l2_shot_bound(5, epsilon, eta),
            expected,
        )
        self.assertEqual(
            fixed_norm_vector_shot_bound(2.0, epsilon, eta),
            math.ceil(
                4.0
                * (1.0 + math.sqrt(2.0 * math.log(1.0 / eta))) ** 2
                / epsilon**2
            ),
        )

    def test_relative_shot_bound_and_directional_guarantees(self) -> None:
        n = 5
        eta = 0.05
        rho = 0.1
        gradient_norm = 2.5
        self.assertEqual(
            complete_magnitude_relative_l2_shot_bound(
                n,
                rho,
                gradient_norm,
                eta,
            ),
            complete_magnitude_l2_shot_bound(
                n,
                rho * gradient_norm,
                eta,
            ),
        )
        self.assertTrue(descent_direction_is_guaranteed(2.0, 0.5))
        self.assertFalse(descent_direction_is_guaranteed(2.0, 2.0))
        self.assertFalse(descent_direction_is_guaranteed(0.0, 0.0))
        self.assertAlmostEqual(direction_error_upper_bound(2.0, 0.5), 0.5)
        with self.assertRaises(ValueError):
            complete_magnitude_relative_l2_shot_bound(n, 1.0, gradient_norm, eta)
        with self.assertRaises(ValueError):
            complete_magnitude_relative_l2_shot_bound(n, rho, 0.0, eta)
        with self.assertRaises(ValueError):
            direction_error_upper_bound(0.0, 0.0)
        with self.assertRaises(ValueError):
            direction_error_upper_bound(1.0, 1.0)

    def test_coordinate_frame_separation_with_hopf_split(self) -> None:
        root = 1.0e-3
        left = 0.37
        right = 0.81
        state = np.asarray(
            [
                math.cos(root) * math.cos(left),
                math.cos(root) * math.sin(left),
                math.sin(root) * math.cos(right),
                math.sin(root) * math.sin(right),
            ],
            dtype=complex,
        )
        directions = np.asarray(
            [
                [
                    -math.sin(root) * math.cos(left),
                    -math.sin(root) * math.sin(left),
                    math.cos(root) * math.cos(right),
                    math.cos(root) * math.sin(right),
                ],
                [-math.sin(left), math.cos(left), 0.0, 0.0],
                [0.0, 0.0, -math.sin(right), math.cos(right)],
            ],
            dtype=complex,
        )
        sqrt_metric = np.asarray([1.0, math.cos(root), math.sin(root)])
        selected = 2
        observable = swap_reflection(state, directions[selected])

        np.testing.assert_allclose(observable, observable.conj().T, atol=1e-13)
        np.testing.assert_allclose(
            observable @ observable,
            np.eye(4),
            atol=1e-13,
        )
        np.testing.assert_allclose(
            observable @ state,
            directions[selected],
            atol=1e-13,
        )

        frame_coefficients = 2.0 * np.real(
            directions.conj() @ (observable @ state)
        )
        coordinate_gradient = sqrt_metric * frame_coefficients
        epsilon = 3.0 * sqrt_metric[selected]

        self.assertLess(np.max(np.abs(coordinate_gradient)), epsilon)
        self.assertAlmostEqual(frame_coefficients[selected], 2.0)
        np.testing.assert_allclose(
            np.delete(frame_coefficients, selected),
            0.0,
            atol=1e-13,
        )
        self.assertAlmostEqual(float(np.linalg.norm(frame_coefficients)), 2.0)

    def test_magnitude_norm_hierarchy(self) -> None:
        self.assertAlmostEqual(complete_frame_record_norm(0), 0.0)
        self.assertAlmostEqual(complete_frame_record_norm(7), 2.0 * math.sqrt(7))
        self.assertAlmostEqual(natural_gradient_coordinate_record_bound(0.25), 4.0)
        self.assertAlmostEqual(
            regularized_natural_gradient_coordinate_record_bound(0.25),
            2.0,
        )
        with self.assertRaises(ValueError):
            complete_frame_record_norm(-1)
        with self.assertRaises(ValueError):
            natural_gradient_coordinate_record_bound(0.0)
        with self.assertRaises(ValueError):
            regularized_natural_gradient_coordinate_record_bound(0.0)

    def test_metric_conditioning_and_regularization(self) -> None:
        self.assertEqual(ordinary_magnitude_record_second_moment(0.0), 0.0)
        self.assertAlmostEqual(ordinary_magnitude_record_second_moment(0.25), 1.0)
        self.assertAlmostEqual(natural_gradient_record_second_moment(0.25), 16.0)

        tau = 0.2
        bound = regularized_natural_gradient_second_moment_bound(tau)
        self.assertEqual(bound, 5.0)
        for metric in np.linspace(0.0, 1.0, 101):
            moment = regularized_natural_gradient_record_second_moment(metric, tau)
            self.assertLessEqual(moment, bound + 1e-14)
        self.assertAlmostEqual(
            regularized_natural_gradient_record_second_moment(tau, tau),
            bound,
        )

        with self.assertRaises(ValueError):
            ordinary_magnitude_record_second_moment(-1.0)
        with self.assertRaises(ValueError):
            natural_gradient_record_second_moment(0.0)
        with self.assertRaises(ValueError):
            regularized_natural_gradient_record_second_moment(0.5, 0.0)

    def test_phase_metric_conventions_and_support_rank(self) -> None:
        probabilities = np.asarray([0.5, 0.3, 0.2, 0.0])
        ambient = ambient_phase_metric(probabilities)
        projective = projective_phase_metric(probabilities)

        np.testing.assert_allclose(ambient, np.diag(probabilities))
        np.testing.assert_allclose(
            projective,
            np.diag(probabilities) - np.outer(probabilities, probabilities),
        )
        np.testing.assert_allclose(projective @ np.ones(4), 0.0, atol=1e-14)
        self.assertGreaterEqual(float(np.min(np.linalg.eigvalsh(projective))), -1e-14)
        self.assertEqual(np.linalg.matrix_rank(ambient, tol=1e-12), 3)
        self.assertEqual(np.linalg.matrix_rank(projective, tol=1e-12), 2)
        self.assertAlmostEqual(float(np.ones(4) @ ambient @ np.ones(4)), 1.0)

        with self.assertRaises(ValueError):
            ambient_phase_metric([0.2, 0.2])
        with self.assertRaises(ValueError):
            projective_phase_metric([0.8, -0.1, 0.3])

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
        expected = (
            (1.0 - 2.0 * 0.05)
            * (1.0 - 2.0 * 0.01)
            * (1.0 - 2.0 * 0.03)
        )
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
