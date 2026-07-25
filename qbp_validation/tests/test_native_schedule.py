from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import complex_theta_mag, regular_theta_mag, theta_ph
from qbp_validation.native_schedule import (
    native_complex_cnot_charge,
    native_complex_schedule,
    native_complex_statevector,
    native_real_cnot_charge,
    native_real_schedule,
    native_real_statevector,
)
from qbp_validation.reference import complex_state, real_state


class NativeScheduleTests(unittest.TestCase):
    def test_four_qubit_native_schedule_shape(self) -> None:
        real = native_real_schedule(4)
        complex_schedule = native_complex_schedule(4)
        self.assertEqual(len(real), 15)
        self.assertEqual(len(complex_schedule), 15)
        self.assertEqual(sum(gate.is_rc for gate in complex_schedule), 8)
        self.assertEqual(
            [gate.theta_index for gate in complex_schedule if gate.is_rc],
            [
                (8, 16, 17),
                (9, 18, 19),
                (10, 20, 21),
                (12, 24, 25),
                (11, 22, 23),
                (13, 26, 27),
                (14, 28, 29),
                (15, 30, 31),
            ],
        )

    def test_native_real_state_columns_through_n5(self) -> None:
        for n in range(1, 6):
            theta = regular_theta_mag(n)
            np.testing.assert_allclose(
                native_real_statevector(theta), real_state(theta), atol=3e-12, rtol=0.0
            )

    def test_native_complex_state_columns_through_n5(self) -> None:
        for n in range(1, 6):
            mag = complex_theta_mag(n)
            phase = theta_ph(n)
            np.testing.assert_allclose(
                native_complex_statevector(mag, phase),
                complex_state(mag, phase),
                atol=3e-12,
                rtol=0.0,
            )

    def test_four_qubit_native_charges(self) -> None:
        self.assertEqual(native_real_cnot_charge(4), 100)
        self.assertEqual(native_complex_cnot_charge(4), 100)


if __name__ == "__main__":
    unittest.main()
