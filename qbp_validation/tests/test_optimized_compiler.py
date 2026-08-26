from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.optimized_compiler import (
    clean_flag_leakage_block,
    clean_flag_system_block,
    direct_addressed_depth_layer,
    direct_real_frame,
    flagged_addressed_depth_layer,
    flagged_real_frame,
    forward_ucr_cnot_upper_bound,
    frame_ucr_core_cnot_upper_bound,
    inverse_suffix_ucr_cnot_upper_bound,
    optimized_compiler_row,
    suffix_predicate_control_widths,
    suffix_predicate_quadratic_proxy,
    ucr_ry_cnot_upper_bound,
)


class OptimizedCompilerTests(unittest.TestCase):
    def test_flagged_depth_layers_match_direct_layers(self) -> None:
        rng = np.random.default_rng(260827)
        for n in range(1, 6):
            for depth in range(n):
                angles = rng.uniform(-1.1, 1.1, size=1 << depth)
                direct = direct_addressed_depth_layer(n, depth, angles)
                flagged = flagged_addressed_depth_layer(n, depth, angles)
                np.testing.assert_allclose(
                    clean_flag_system_block(flagged, n), direct, atol=1e-12, rtol=0.0
                )
                np.testing.assert_allclose(
                    clean_flag_leakage_block(flagged, n), 0.0, atol=1e-12, rtol=0.0
                )

    def test_complete_flagged_frame_matches_direct_frame(self) -> None:
        rng = np.random.default_rng(260828)
        for n in range(1, 5):
            theta = rng.uniform(-0.9, 0.9, size=(1 << n) - 1)
            direct = direct_real_frame(n, theta)
            flagged = flagged_real_frame(n, theta)
            np.testing.assert_allclose(
                clean_flag_system_block(flagged, n), direct, atol=1e-12, rtol=0.0
            )
            np.testing.assert_allclose(
                clean_flag_leakage_block(flagged, n), 0.0, atol=1e-12, rtol=0.0
            )
            np.testing.assert_allclose(
                clean_flag_system_block(flagged.conj().T, n),
                direct.conj().T,
                atol=1e-12,
                rtol=0.0,
            )
            np.testing.assert_allclose(
                clean_flag_leakage_block(flagged.conj().T, n),
                0.0,
                atol=1e-12,
                rtol=0.0,
            )

    def test_uniformly_controlled_rotation_core_counts(self) -> None:
        self.assertEqual([ucr_ry_cnot_upper_bound(k) for k in range(6)], [0, 2, 4, 8, 16, 32])
        self.assertEqual(
            [forward_ucr_cnot_upper_bound(n) for n in range(1, 7)],
            [0, 2, 6, 14, 30, 62],
        )
        self.assertEqual(
            [frame_ucr_core_cnot_upper_bound(n) for n in range(1, 7)],
            [0, 4, 10, 22, 46, 94],
        )
        self.assertEqual(
            [inverse_suffix_ucr_cnot_upper_bound(4, depth) for depth in range(4)],
            [14, 12, 8, 0],
        )

    def test_suffix_predicates_are_exposed_separately(self) -> None:
        self.assertEqual(suffix_predicate_control_widths(4), (3, 3, 2, 2, 1, 1))
        self.assertEqual(suffix_predicate_quadratic_proxy(4), 28)
        row = optimized_compiler_row(4)
        self.assertEqual(row.dimension, 16)
        self.assertEqual(row.forward_ucr_cnot_upper_bound, 14)
        self.assertEqual(row.frame_ucr_core_cnot_upper_bound, 22)
        self.assertEqual(row.suffix_predicate_calls, 6)
        self.assertEqual(row.maximum_predicate_controls, 3)
        self.assertEqual(row.reusable_clean_flags, 1)


if __name__ == "__main__":
    unittest.main()
