from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import complex_theta_mag, observables, theta_ph
from qbp_validation.circuits import (
    complex_magnitude_integrated_4q_circuit,
    complex_magnitude_separated_circuit,
    probabilities,
)
from qbp_validation.decoders import decode_balanced_magnitude_gradient
from qbp_validation.reference import complex_magnitude_gradient, real_tree_data


class ComplexMagnitudeTests(unittest.TestCase):
    def test_separated_estimator_n1_to_n4(self) -> None:
        for n in range(1, 5):
            mag = complex_theta_mag(n)
            phase = theta_ph(n)
            sqrt_metric = real_tree_data(mag).sqrt_metric
            for obs_index, observable in enumerate(observables(n)):
                with self.subTest(n=n, observable=obs_index):
                    probs = probabilities(
                        complex_magnitude_separated_circuit(mag, phase, observable)
                    )
                    decoded = decode_balanced_magnitude_gradient(
                        probs, sqrt_metric, n
                    )
                    exact = complex_magnitude_gradient(mag, phase, observable)
                    np.testing.assert_allclose(decoded, exact, atol=3e-12, rtol=0.0)

    def test_integrated_four_qubit_frame_matches_separated_distribution(self) -> None:
        mag = complex_theta_mag(4)
        phase = theta_ph(4)
        sqrt_metric = real_tree_data(mag).sqrt_metric
        for obs_index, observable in enumerate(observables(4)):
            with self.subTest(observable=obs_index):
                separated = probabilities(
                    complex_magnitude_separated_circuit(mag, phase, observable)
                )
                integrated = probabilities(
                    complex_magnitude_integrated_4q_circuit(mag, phase, observable)
                )
                np.testing.assert_allclose(integrated, separated, atol=3e-12, rtol=0.0)
                decoded = decode_balanced_magnitude_gradient(integrated, sqrt_metric, 4)
                exact = complex_magnitude_gradient(mag, phase, observable)
                np.testing.assert_allclose(decoded, exact, atol=3e-12, rtol=0.0)


if __name__ == "__main__":
    unittest.main()
