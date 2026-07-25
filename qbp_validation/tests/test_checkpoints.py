from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import complex_theta_mag, observables, regular_theta_mag, theta_ph
from qbp_validation.circuits import (
    complex_checkpoint_integrated_depth2_4q_circuit,
    complex_checkpoint_separated_circuit,
    probabilities,
    real_checkpoint_measurement_circuit,
    real_checkpoint_native_forward_circuit,
)
from qbp_validation.decoders import checkpoint_record, decode_checkpoint_gradient
from qbp_validation.reference import complex_magnitude_gradient, real_gradient


class CheckpointTests(unittest.TestCase):
    def test_real_checkpoint_all_depths(self) -> None:
        for n in range(1, 5):
            theta = regular_theta_mag(n)
            for obs_index, observable in enumerate(observables(n)):
                exact = real_gradient(theta, observable)
                for depth in range(n):
                    with self.subTest(n=n, observable=obs_index, depth=depth):
                        probs = probabilities(
                            real_checkpoint_measurement_circuit(theta, observable, depth)
                        )
                        decoded = decode_checkpoint_gradient(probs, n, depth)
                        start = (1 << depth) - 1
                        stop = (1 << (depth + 1)) - 1
                        np.testing.assert_allclose(
                            decoded, exact[start:stop], atol=3e-12, rtol=0.0
                        )

    def test_native_real_forward_all_depths(self) -> None:
        n = 4
        theta = regular_theta_mag(n)
        observable = observables(n)[-1]
        exact = real_gradient(theta, observable)
        for depth in range(n):
            decoded = decode_checkpoint_gradient(
                probabilities(
                    real_checkpoint_native_forward_circuit(theta, observable, depth)
                ),
                n,
                depth,
            )
            start = (1 << depth) - 1
            stop = (1 << (depth + 1)) - 1
            np.testing.assert_allclose(decoded, exact[start:stop], atol=3e-12, rtol=0.0)

    def test_complex_separated_checkpoint_all_depths(self) -> None:
        for n in range(1, 5):
            mag = complex_theta_mag(n)
            phase = theta_ph(n)
            for obs_index, observable in enumerate(observables(n)):
                exact = complex_magnitude_gradient(mag, phase, observable)
                for depth in range(n):
                    with self.subTest(n=n, observable=obs_index, depth=depth):
                        probs = probabilities(
                            complex_checkpoint_separated_circuit(
                                mag, phase, observable, depth
                            )
                        )
                        decoded = decode_checkpoint_gradient(probs, n, depth)
                        start = (1 << depth) - 1
                        stop = (1 << (depth + 1)) - 1
                        np.testing.assert_allclose(
                            decoded, exact[start:stop], atol=3e-12, rtol=0.0
                        )

    def test_integrated_complex_depth2_checkpoint(self) -> None:
        n = 4
        mag = complex_theta_mag(n)
        phase = theta_ph(n)
        observable = observables(n)[-1]
        exact = complex_magnitude_gradient(mag, phase, observable)[3:7]
        decoded = decode_checkpoint_gradient(
            probabilities(
                complex_checkpoint_integrated_depth2_4q_circuit(
                    mag, phase, observable
                )
            ),
            n,
            2,
        )
        np.testing.assert_allclose(decoded, exact, atol=3e-12, rtol=0.0)

    def test_checkpoint_records_have_fixed_norm_two(self) -> None:
        for width in (1, 2, 4, 8):
            for ancilla in (0, 1):
                for target in (0, 1):
                    for prefix in range(width):
                        record = checkpoint_record(ancilla, target, prefix, width)
                        self.assertAlmostEqual(float(np.linalg.norm(record)), 2.0)


if __name__ == "__main__":
    unittest.main()
