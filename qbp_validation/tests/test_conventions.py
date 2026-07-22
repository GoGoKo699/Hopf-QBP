from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import complex_theta, observables
from qbp_validation.conventions import (
    bit_at,
    frame_gate_specs,
    join_theta,
    manuscript_wire_from_qibo_index,
    marker_label,
    parity,
    qibo_index_from_manuscript_wire,
    split_theta,
)
from qbp_validation.reference import is_hermitian_unitary


class ConventionTests(unittest.TestCase):
    def test_marker_map_is_bijection_onto_nonzero_labels(self) -> None:
        for n in range(1, 7):
            labels = [marker_label(node, n) for node in range(1, 1 << n)]
            self.assertEqual(sorted(labels), list(range(1, 1 << n)))

    def test_big_endian_bit_convention(self) -> None:
        label = 0b1011
        self.assertEqual([bit_at(label, q, 4) for q in range(4)], [1, 0, 1, 1])
        self.assertEqual(parity(0b0110, 0b1011), 1)

    def test_manuscript_wire_qibo_index_translation(self) -> None:
        self.assertEqual(
            [manuscript_wire_from_qibo_index(index, 4) for index in range(4)],
            [4, 3, 2, 1],
        )
        self.assertEqual(
            [qibo_index_from_manuscript_wire(wire, 4) for wire in range(1, 5)],
            [3, 2, 1, 0],
        )

    def test_complex_theta_split_and_join(self) -> None:
        for n in range(1, 6):
            theta = complex_theta(n)
            theta_mag, theta_ph = split_theta(theta)
            self.assertEqual(theta_mag.size, (1 << n) - 1)
            self.assertEqual(theta_ph.size, 1 << n)
            np.testing.assert_array_equal(join_theta(theta_mag, theta_ph), theta)

    def test_frame_specs_match_active_pairs(self) -> None:
        for n in range(1, 6):
            for spec in frame_gate_specs(n):
                self.assertEqual(spec.anchor ^ spec.marker, 1 << (n - 1 - spec.target))
                self.assertEqual(bit_at(spec.anchor, spec.target, n), 0)
                self.assertEqual(bit_at(spec.marker, spec.target, n), 1)

    def test_validation_observables_satisfy_access_model(self) -> None:
        for n in range(1, 5):
            for observable in observables(n):
                self.assertTrue(is_hermitian_unitary(observable))


if __name__ == "__main__":
    unittest.main()
