from __future__ import annotations

import unittest

from qbp_validation.conventions import (
    checkpoint_cnot_charge_without_observable,
    controlled_rc_cnot_charge,
    controlled_ry_cnot_charge,
    depth_layer_cnot_charge,
    depth_preparation_cnot_charge,
    four_qubit_complex_frame_cnot_charge,
    four_qubit_complex_suffix_cnot_charge,
    frame_cnot_charge,
    inverse_suffix_cnot_charge,
)
from qbp_validation.native_schedule import native_complex_cnot_charge, native_real_cnot_charge


class ResourceLedgerTests(unittest.TestCase):
    def test_assigned_controlled_ry_charges(self) -> None:
        expected = {0: 0, 1: 2, 2: 6, 3: 14, 4: 30, 5: 56, 6: 72, 7: 88}
        self.assertEqual(
            {controls: controlled_ry_cnot_charge(controls) for controls in expected},
            expected,
        )

    def test_assigned_controlled_rc_charges(self) -> None:
        expected = {0: 0, 1: 2, 2: 6, 3: 14, 4: 30, 5: 78, 6: 102, 7: 118}
        self.assertEqual(
            {controls: controlled_rc_cnot_charge(controls) for controls in expected},
            expected,
        )

    def test_four_qubit_compiler_objects(self) -> None:
        self.assertEqual(native_real_cnot_charge(4), 100)
        self.assertEqual(native_complex_cnot_charge(4), 100)
        self.assertEqual(depth_preparation_cnot_charge(4), 140)
        self.assertEqual(frame_cnot_charge(4), 210)
        self.assertEqual(four_qubit_complex_frame_cnot_charge(), 210)
        self.assertEqual(inverse_suffix_cnot_charge(4, 2), 112)
        self.assertEqual(four_qubit_complex_suffix_cnot_charge(), 112)

    def test_four_qubit_depth_and_checkpoint_totals(self) -> None:
        self.assertEqual(
            [depth_layer_cnot_charge(depth) for depth in range(4)],
            [0, 4, 24, 112],
        )
        self.assertEqual(
            [checkpoint_cnot_charge_without_observable(4, depth) for depth in range(4)],
            [280, 276, 252, 140],
        )
        native_forward = [
            native_real_cnot_charge(4) + inverse_suffix_cnot_charge(4, depth)
            for depth in range(4)
        ]
        self.assertEqual(native_forward, [240, 236, 212, 100])

    def test_four_qubit_record_totals(self) -> None:
        self.assertEqual(native_real_cnot_charge(4) + frame_cnot_charge(4), 310)
        self.assertEqual(
            native_complex_cnot_charge(4) + four_qubit_complex_frame_cnot_charge(),
            310,
        )
        self.assertEqual(native_complex_cnot_charge(4), 100)
        self.assertEqual(
            native_real_cnot_charge(4) + inverse_suffix_cnot_charge(4, 2), 212
        )
        self.assertEqual(
            native_complex_cnot_charge(4) + four_qubit_complex_suffix_cnot_charge(),
            212,
        )


if __name__ == "__main__":
    unittest.main()
