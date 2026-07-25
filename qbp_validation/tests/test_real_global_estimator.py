from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import observables, regular_theta_mag
from qbp_validation.circuits import (
    probabilities,
    real_global_measurement_circuit,
    real_global_native_forward_circuit,
)
from qbp_validation.decoders import decode_balanced_magnitude_gradient
from qbp_validation.reference import real_gradient, real_tree_data


class RealGlobalEstimatorTests(unittest.TestCase):
    def test_exact_distribution_returns_complete_gradient(self) -> None:
        for n in range(1, 5):
            theta = regular_theta_mag(n)
            data = real_tree_data(theta)
            for obs_index, observable in enumerate(observables(n)):
                with self.subTest(n=n, observable=obs_index):
                    probs = probabilities(real_global_measurement_circuit(theta, observable))
                    decoded = decode_balanced_magnitude_gradient(probs, data.sqrt_metric, n)
                    exact = real_gradient(theta, observable)
                    np.testing.assert_allclose(decoded, exact, atol=3e-12, rtol=0.0)
                    direct = decode_balanced_magnitude_gradient(
                        probs, data.sqrt_metric, n, use_fwht=False
                    )
                    np.testing.assert_allclose(decoded, direct, atol=3e-12, rtol=0.0)

    def test_native_forward_has_same_complete_distribution(self) -> None:
        theta = regular_theta_mag(4)
        observable = observables(4)[-1]
        frame_forward = probabilities(real_global_measurement_circuit(theta, observable))
        native_forward = probabilities(real_global_native_forward_circuit(theta, observable))
        np.testing.assert_allclose(frame_forward, native_forward, atol=3e-12, rtol=0.0)


if __name__ == "__main__":
    unittest.main()
