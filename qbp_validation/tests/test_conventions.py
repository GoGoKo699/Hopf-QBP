from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import complex_theta, observables
from qbp_validation.conventions import (
    anchor_label,
    bit_at,
    checkpoint_interface_projector,
    infer_n_from_theta_mag,
    join_theta,
    manuscript_wire_from_qibo_index,
    marker_map,
    node_depth_position,
    parity,
    qibo_index_from_manuscript_wire,
    split_theta,
)
from qbp_validation.reference import is_hermitian_unitary


class ConventionTests(unittest.TestCase):
    def test_complete_complex_vector_roundtrip(self) -> None:
        for n in range(1, 6):
            theta = complex_theta(n)
            mag, phase = split_theta(theta)
            self.assertEqual(infer_n_from_theta_mag(mag), n)
            np.testing.assert_array_equal(join_theta(mag, phase), theta)
            self.assertEqual(mag.size, (1 << n) - 1)
            self.assertEqual(phase.size, 1 << n)

    def test_breadth_first_nodes_and_addresses(self) -> None:
        self.assertEqual(node_depth_position(1), (0, 0))
        self.assertEqual(node_depth_position(5), (2, 1))
        self.assertEqual(anchor_label(5, 4), 0b0100)
        self.assertEqual(marker_map(4)[5], 0b0110)
        self.assertEqual(set(marker_map(4).values()), set(range(1, 16)))

    def test_big_endian_wire_translation(self) -> None:
        n = 4
        self.assertEqual(bit_at(0b1010, 0, n), 1)
        self.assertEqual(bit_at(0b1010, 3, n), 0)
        self.assertEqual(manuscript_wire_from_qibo_index(0, n), 4)
        self.assertEqual(manuscript_wire_from_qibo_index(3, n), 1)
        self.assertEqual(qibo_index_from_manuscript_wire(4, n), 0)
        self.assertEqual(qibo_index_from_manuscript_wire(1, n), 3)

    def test_parity(self) -> None:
        self.assertEqual(parity(0b0110, 0b1011), 1)
        self.assertEqual(parity(0b0110, 0b1111), 0)

    def test_checkpoint_projector(self) -> None:
        projector = checkpoint_interface_projector(4, 2)
        expected = np.diag([1.0 if label % 2 == 0 else 0.0 for label in range(16)])
        np.testing.assert_array_equal(projector, expected)
        np.testing.assert_array_equal(
            checkpoint_interface_projector(4, 3), np.eye(16, dtype=complex)
        )

    def test_validation_observables_match_access_model(self) -> None:
        for n in range(1, 5):
            for observable in observables(n):
                self.assertTrue(is_hermitian_unitary(observable))


if __name__ == "__main__":
    unittest.main()
