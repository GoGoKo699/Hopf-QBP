from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.conventions import parity
from qbp_validation.decoders import (
    checkpoint_record,
    decode_balanced_magnitude_gradient,
    decode_balanced_magnitude_samples_recordwise,
    decode_checkpoint_gradient,
    fwht,
    global_moments_direct,
    global_moments_fwht,
    global_moments_recordwise,
    phase_record,
    walsh_character_from_outcome,
)


class DecoderTests(unittest.TestCase):
    def test_fwht_matches_dense_hadamard(self) -> None:
        rng = np.random.default_rng(123)
        for n in range(1, 7):
            values = rng.normal(size=1 << n)
            dense = np.asarray([[1.0]])
            h = np.asarray([[1.0, 1.0], [1.0, -1.0]])
            for _ in range(n):
                dense = np.kron(dense, h)
            np.testing.assert_allclose(
                fwht(values), dense @ values, atol=1e-12, rtol=0.0
            )

    def test_direct_and_fwht_global_moments(self) -> None:
        rng = np.random.default_rng(456)
        probabilities = rng.uniform(size=32)
        probabilities /= probabilities.sum()
        np.testing.assert_allclose(
            global_moments_direct(probabilities),
            global_moments_fwht(probabilities),
            atol=1e-12,
            rtol=0.0,
        )

    def test_walsh_character_matches_direct_parity(self) -> None:
        for n in range(1, 7):
            N = 1 << n
            for outcome in range(N):
                expected = np.asarray(
                    [
                        -1.0 if parity(label, outcome) else 1.0
                        for label in range(N)
                    ]
                )
                np.testing.assert_array_equal(
                    walsh_character_from_outcome(outcome, n), expected
                )

    def test_recordwise_decoder_matches_empirical_fwht(self) -> None:
        rng = np.random.default_rng(260905)
        for n in range(1, 7):
            N = 1 << n
            shots = 3 * n + 1
            ancilla = rng.integers(0, 2, size=shots)
            labels = rng.integers(0, N, size=shots)
            probabilities = np.zeros(2 * N, dtype=float)
            for bit, label in zip(ancilla, labels, strict=True):
                probabilities[int(bit) * N + int(label)] += 1.0 / shots
            np.testing.assert_allclose(
                global_moments_recordwise(ancilla, labels, n),
                global_moments_fwht(probabilities),
                atol=1e-12,
                rtol=0.0,
            )
            sqrt_metric = rng.uniform(0.0, 1.0, size=N - 1)
            np.testing.assert_allclose(
                decode_balanced_magnitude_samples_recordwise(
                    ancilla, labels, sqrt_metric, n
                ),
                decode_balanced_magnitude_gradient(
                    probabilities, sqrt_metric, n
                ),
                atol=1e-12,
                rtol=0.0,
            )

    def test_recordwise_decoder_rejects_invalid_outcomes(self) -> None:
        with self.assertRaises(ValueError):
            global_moments_recordwise([], [], 2)
        with self.assertRaises(ValueError):
            global_moments_recordwise([0, 1], [0], 2)
        with self.assertRaises(ValueError):
            global_moments_recordwise([0, 2], [0, 1], 2)
        with self.assertRaises(ValueError):
            global_moments_recordwise([0, 1], [0, 4], 2)
        with self.assertRaises(ValueError):
            global_moments_recordwise([0.0, 0.5], [0, 1], 2)
        with self.assertRaises(ValueError):
            global_moments_recordwise([0, 1], [0, np.nan], 2)
        with self.assertRaises(ValueError):
            walsh_character_from_outcome(np.nan, 2)

    def test_fixed_norm_records(self) -> None:
        for N in (2, 4, 8, 16):
            for ancilla in (0, 1):
                for leaf in range(N):
                    self.assertAlmostEqual(
                        np.linalg.norm(phase_record(ancilla, leaf, N)), 2.0
                    )
        for width in (1, 2, 4, 8):
            for ancilla in (0, 1):
                for target in (0, 1):
                    for prefix in range(width):
                        self.assertAlmostEqual(
                            np.linalg.norm(
                                checkpoint_record(
                                    ancilla, target, prefix, width
                                )
                            ),
                            2.0,
                        )

    def test_checkpoint_decoder_discards_suffix(self) -> None:
        n = 3
        depth = 1
        probabilities = np.zeros(1 << (n + 1), dtype=float)
        probabilities[0b0010] = 0.2
        probabilities[0b0011] = 0.3
        probabilities[(1 << n) | 0b110] = 0.5
        decoded = decode_checkpoint_gradient(probabilities, n, depth)
        np.testing.assert_allclose(
            decoded, [1.0, -1.0], atol=1e-12, rtol=0.0
        )


if __name__ == "__main__":
    unittest.main()
