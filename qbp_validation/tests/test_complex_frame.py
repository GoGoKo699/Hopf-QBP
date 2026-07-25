from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import complex_theta_mag, theta_ph
from qbp_validation.circuits import (
    complex_frame_rc_4q_circuit,
    complex_frame_separated_circuit,
)
from qbp_validation.reference import (
    addressed_rc_frame_matrix_4q,
    centered_leaf_phases,
    complex_frame_matrix,
)


class ComplexFrameTests(unittest.TestCase):
    def test_separated_full_frame_n1_to_n4(self) -> None:
        for n in range(1, 5):
            mag = complex_theta_mag(n)
            phase = theta_ph(n)
            qibo_frame = np.asarray(
                complex_frame_separated_circuit(mag, phase).unitary(), dtype=complex
            )
            np.testing.assert_allclose(
                qibo_frame, complex_frame_matrix(mag, phase), atol=3e-12, rtol=0.0
            )

    def test_addressed_rc_compiler_is_complete_frame_up_to_common_phase(self) -> None:
        mag = complex_theta_mag(4)
        phase = theta_ph(4)
        qibo_frame = np.asarray(complex_frame_rc_4q_circuit(mag, phase).unitary())
        independent = addressed_rc_frame_matrix_4q(mag, phase)
        mean, _ = centered_leaf_phases(phase)
        exact = np.exp(-1j * mean) * complex_frame_matrix(mag, phase)
        np.testing.assert_allclose(qibo_frame, independent, atol=3e-12, rtol=0.0)
        np.testing.assert_allclose(qibo_frame, exact, atol=3e-12, rtol=0.0)

    def test_addressed_rc_inverse(self) -> None:
        mag = complex_theta_mag(4)
        phase = theta_ph(4)
        forward = np.asarray(complex_frame_rc_4q_circuit(mag, phase).unitary())
        inverse = np.asarray(
            complex_frame_rc_4q_circuit(mag, phase, inverse=True).unitary()
        )
        np.testing.assert_allclose(inverse, forward.conj().T, atol=3e-12, rtol=0.0)


if __name__ == "__main__":
    unittest.main()
