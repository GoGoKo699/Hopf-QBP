from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import observables, singular_theta_mag, theta_ph
from qbp_validation.circuits import (
    complex_checkpoint_measurement_circuit,
    probabilities,
    real_checkpoint_measurement_circuit,
    real_global_measurement_circuit,
)
from qbp_validation.decoders import (
    decode_balanced_magnitude_gradient,
    decode_checkpoint_gradient,
)
from qbp_validation.reference import complex_magnitude_gradient, real_gradient, real_tree_data


class SingularChartTests(unittest.TestCase):
    def test_zero_metric_coordinates_decode_to_zero(self) -> None:
        for n in range(2, 5):
            theta_mag = singular_theta_mag(n)
            data = real_tree_data(theta_mag)
            zero = np.flatnonzero(data.metric < 1e-28)
            self.assertGreater(zero.size, 0)
            observable = observables(n)[-1]
            probs = probabilities(
                real_global_measurement_circuit(theta_mag, observable)
            )
            decoded = decode_balanced_magnitude_gradient(
                probs, data.sqrt_metric, n
            )
            exact = real_gradient(theta_mag, observable)
            np.testing.assert_allclose(decoded, exact, atol=3e-12, rtol=0.0)
            np.testing.assert_allclose(decoded[zero], 0.0, atol=3e-12, rtol=0.0)

    def test_real_and_complex_checkpoints_at_singular_points(self) -> None:
        for n in range(2, 5):
            theta_mag = singular_theta_mag(n)
            theta_phase = theta_ph(n)
            observable = observables(n)[1]
            exact_real = real_gradient(theta_mag, observable)
            exact_complex = complex_magnitude_gradient(
                theta_mag, theta_phase, observable
            )
            for depth in range(n):
                start = (1 << depth) - 1
                stop = (1 << (depth + 1)) - 1
                real_decoded = decode_checkpoint_gradient(
                    probabilities(
                        real_checkpoint_measurement_circuit(
                            theta_mag, observable, depth
                        )
                    ),
                    n,
                    depth,
                )
                complex_decoded = decode_checkpoint_gradient(
                    probabilities(
                        complex_checkpoint_measurement_circuit(
                            theta_mag, theta_phase, observable, depth
                        )
                    ),
                    n,
                    depth,
                )
                np.testing.assert_allclose(
                    real_decoded, exact_real[start:stop], atol=3e-12, rtol=0.0
                )
                np.testing.assert_allclose(
                    complex_decoded,
                    exact_complex[start:stop],
                    atol=3e-12,
                    rtol=0.0,
                )


if __name__ == "__main__":
    unittest.main()
