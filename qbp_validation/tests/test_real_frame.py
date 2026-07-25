from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import regular_theta_mag, singular_theta_mag
from qbp_validation.circuits import frame_circuit
from qbp_validation.reference import real_frame_matrix, real_tree_data


class RealFrameTests(unittest.TestCase):
    def test_regular_frames_n1_to_n4(self) -> None:
        for n in range(1, 5):
            theta = regular_theta_mag(n)
            qibo_frame = np.asarray(frame_circuit(theta).unitary(), dtype=complex)
            reference = real_frame_matrix(theta)
            np.testing.assert_allclose(qibo_frame, reference, atol=3e-12, rtol=0.0)
            np.testing.assert_allclose(
                qibo_frame.conj().T @ qibo_frame,
                np.eye(1 << n),
                atol=3e-12,
                rtol=0.0,
            )

    def test_singular_frames_remain_unitary_and_keep_completion_columns(self) -> None:
        for n in range(1, 5):
            theta = singular_theta_mag(n)
            data = real_tree_data(theta)
            qibo_frame = np.asarray(frame_circuit(theta).unitary(), dtype=complex)
            np.testing.assert_allclose(qibo_frame, real_frame_matrix(theta), atol=3e-12, rtol=0.0)
            zero = np.flatnonzero(np.abs(data.sqrt_metric) < 1e-14)
            if zero.size:
                for index in zero:
                    self.assertAlmostEqual(float(np.linalg.norm(data.derivatives[index])), 0.0, places=12)

    def test_inverse_frame(self) -> None:
        theta = regular_theta_mag(4)
        forward = np.asarray(frame_circuit(theta).unitary(), dtype=complex)
        inverse = np.asarray(frame_circuit(theta, inverse=True).unitary(), dtype=complex)
        np.testing.assert_allclose(inverse, forward.conj().T, atol=3e-12, rtol=0.0)


if __name__ == "__main__":
    unittest.main()
