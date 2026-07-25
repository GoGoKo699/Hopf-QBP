from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.decoders import (
    checkpoint_record,
    decode_checkpoint_gradient,
    fwht,
    global_moments_direct,
    global_moments_fwht,
    phase_record,
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
            np.testing.assert_allclose(fwht(values), dense @ values, atol=1e-12, rtol=0.0)

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

    def test_fixed_norm_records(self) -> None:
        for N in (2, 4, 8, 16):
            for ancilla in (0, 1):
                for leaf in range(N):
                    self.assertAlmostEqual(np.linalg.norm(phase_record(ancilla, leaf, N)), 2.0)
        for width in (1, 2, 4, 8):
            for ancilla in (0, 1):
                for target in (0, 1):
                    for prefix in range(width):
                        self.assertAlmostEqual(
                            np.linalg.norm(checkpoint_record(ancilla, target, prefix, width)),
                            2.0,
                        )

    def test_checkpoint_decoder_discards_suffix(self) -> None:
        n = 3
        depth = 1
        probabilities = np.zeros(1 << (n + 1), dtype=float)
        # Ancilla 0, system labels 010 and 011 share prefix 0 and target 1.
        probabilities[0b0010] = 0.2
        probabilities[0b0011] = 0.3
        # Ancilla 1, system label 110 has prefix 1 and target 1.
        probabilities[(1 << n) | 0b110] = 0.5
        decoded = decode_checkpoint_gradient(probabilities, n, depth)
        np.testing.assert_allclose(decoded, [1.0, -1.0], atol=1e-12, rtol=0.0)


if __name__ == "__main__":
    unittest.main()
