from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import complex_theta_mag, observables, regular_theta_mag, theta_ph
from qbp_validation.circuits import (
    complex_magnitude_measurement_circuit,
    depth_preparation_circuit,
    frame_circuit,
    native_complex_circuit,
    native_real_preparation_circuit,
    statevector,
    probabilities,
)
from qbp_validation.decoders import decode_balanced_magnitude_gradient
from qbp_validation.reference import (
    complex_magnitude_gradient,
    complex_state,
    real_tree_data,
)


class AsymmetricCompletionTests(unittest.TestCase):
    def test_native_depth_and_addressed_completions_share_only_state_column(self) -> None:
        theta_mag = regular_theta_mag(4)
        reference_state = real_tree_data(theta_mag).state

        native = np.asarray(native_real_preparation_circuit(theta_mag).unitary())
        checkpoint = np.asarray(depth_preparation_circuit(theta_mag).unitary())
        addressed = np.asarray(frame_circuit(theta_mag).unitary())

        for unitary in (native, checkpoint, addressed):
            np.testing.assert_allclose(
                unitary[:, 0], reference_state, atol=2e-12, rtol=0.0
            )

        self.assertGreater(float(np.max(np.abs(addressed - checkpoint))), 1e-3)
        self.assertGreater(float(np.max(np.abs(native - checkpoint))), 1e-3)


    def test_native_complex_state_column(self) -> None:
        for n in range(1, 5):
            theta_mag = complex_theta_mag(n)
            theta_phase = theta_ph(n)
            np.testing.assert_allclose(
                statevector(native_complex_circuit(theta_mag, theta_phase)),
                complex_state(theta_mag, theta_phase),
                atol=3e-12,
                rtol=0.0,
            )

    def test_asymmetric_complex_decoder_uses_checkpoint_forward_state(self) -> None:
        n = 4
        theta_mag = complex_theta_mag(n)
        theta_phase = theta_ph(n)
        observable = observables(n)[-1]
        probs = probabilities(
            complex_magnitude_measurement_circuit(
                theta_mag, theta_phase, observable
            )
        )
        data = real_tree_data(theta_mag)
        decoded = decode_balanced_magnitude_gradient(
            probs, data.sqrt_metric, n
        )
        exact = complex_magnitude_gradient(theta_mag, theta_phase, observable)
        np.testing.assert_allclose(decoded, exact, atol=3e-12, rtol=0.0)


if __name__ == "__main__":
    unittest.main()
