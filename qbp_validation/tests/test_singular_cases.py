from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import observables, singular_theta_mag, theta_ph
from qbp_validation.circuits import (
    complex_checkpoint_separated_circuit,
    complex_phase_measurement_circuit,
    probabilities,
    real_checkpoint_measurement_circuit,
    real_global_measurement_circuit,
)
from qbp_validation.decoders import (
    decode_balanced_magnitude_gradient,
    decode_checkpoint_gradient,
    decode_phase_gradient,
)
from qbp_validation.reference import (
    complex_magnitude_gradient,
    complex_phase_gradient,
    real_gradient,
    real_tree_data,
)


class SingularCaseTests(unittest.TestCase):
    def test_zero_metric_coordinates_decode_to_zero(self) -> None:
        for n in range(2, 5):
            theta = singular_theta_mag(n)
            data = real_tree_data(theta)
            observable = observables(n)[-1]
            decoded = decode_balanced_magnitude_gradient(
                probabilities(real_global_measurement_circuit(theta, observable)),
                data.sqrt_metric,
                n,
            )
            exact = real_gradient(theta, observable)
            np.testing.assert_allclose(decoded, exact, atol=3e-12, rtol=0.0)
            zero = np.flatnonzero(data.metric < 1e-28)
            if zero.size:
                np.testing.assert_allclose(decoded[zero], 0.0, atol=3e-12, rtol=0.0)

    def test_singular_real_and_complex_checkpoints(self) -> None:
        for n in range(2, 5):
            theta = singular_theta_mag(n)
            phase = theta_ph(n)
            observable = observables(n)[-1]
            exact_real = real_gradient(theta, observable)
            exact_complex = complex_magnitude_gradient(theta, phase, observable)
            for depth in range(n):
                start = (1 << depth) - 1
                stop = (1 << (depth + 1)) - 1
                decoded_real = decode_checkpoint_gradient(
                    probabilities(
                        real_checkpoint_measurement_circuit(theta, observable, depth)
                    ),
                    n,
                    depth,
                )
                decoded_complex = decode_checkpoint_gradient(
                    probabilities(
                        complex_checkpoint_separated_circuit(
                            theta, phase, observable, depth
                        )
                    ),
                    n,
                    depth,
                )
                np.testing.assert_allclose(
                    decoded_real, exact_real[start:stop], atol=3e-12, rtol=0.0
                )
                np.testing.assert_allclose(
                    decoded_complex, exact_complex[start:stop], atol=3e-12, rtol=0.0
                )

    def test_zero_amplitude_phase_leaves(self) -> None:
        n = 3
        theta = singular_theta_mag(n)
        phase = theta_ph(n)
        observable = observables(n)[-1]
        decoded = decode_phase_gradient(
            probabilities(complex_phase_measurement_circuit(theta, phase, observable))
        )
        exact = complex_phase_gradient(theta, phase, observable)
        np.testing.assert_allclose(decoded, exact, atol=3e-12, rtol=0.0)


if __name__ == "__main__":
    unittest.main()
