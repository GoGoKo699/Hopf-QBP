from __future__ import annotations

import unittest

import numpy as np

from qbp_validation.cases import (
    complex_theta_mag,
    regular_theta_mag,
    singular_theta_mag,
    theta_ph,
)
from qbp_validation.native_schedule import (
    native_complex_cnot_charge,
    native_complex_schedule,
    native_real_cnot_charge,
    native_real_schedule,
)
from qbp_validation.reference import complex_state, real_tree_data


def _apply_native_real_schedule(theta_mag: np.ndarray) -> np.ndarray:
    """Independent small-state simulator for the native schedule."""

    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    n = int(round(np.log2(theta_mag.size + 1)))
    dimension = 1 << n
    state = np.zeros(dimension, dtype=float)
    state[0] = 1.0

    for gate in native_real_schedule(n):
        assert isinstance(gate.theta_index, int)
        target = gate.target_mask
        c = float(np.cos(theta_mag[gate.theta_index - 1]))
        s = float(np.sin(theta_mag[gate.theta_index - 1]))
        updated = state.copy()
        for label0 in range(dimension):
            if label0 & target:
                continue
            if (label0 & gate.ctrl_mask) != gate.ctrl_mask:
                continue
            if label0 & gate.anti_mask:
                continue
            label1 = label0 | target
            a0 = state[label0]
            a1 = state[label1]
            updated[label0] = c * a0 - s * a1
            updated[label1] = s * a0 + c * a1
        state = updated
    return state


def _apply_native_complex_schedule(
    theta_mag: np.ndarray, theta_phase: np.ndarray
) -> np.ndarray:
    """Independent small-state simulator for the native complex schedule."""

    theta_mag = np.asarray(theta_mag, dtype=float).reshape(-1)
    theta_phase = np.asarray(theta_phase, dtype=float).reshape(-1)
    n = int(round(np.log2(theta_mag.size + 1)))
    dimension = 1 << n
    if theta_phase.size != dimension:
        raise ValueError("theta_phase must contain one phase for every leaf.")

    state = np.zeros(dimension, dtype=complex)
    state[0] = 1.0
    for gate in native_complex_schedule(n):
        target = gate.target_mask
        if isinstance(gate.theta_index, int):
            angle = theta_mag[gate.theta_index - 1]
            c = float(np.cos(angle))
            s = float(np.sin(angle))
            matrix = np.asarray([[c, -s], [s, c]], dtype=complex)
        else:
            magnitude_index, left_phase_index, right_phase_index = gate.theta_index
            angle = theta_mag[magnitude_index - 1]
            left_phase = theta_phase[left_phase_index - dimension]
            right_phase = theta_phase[right_phase_index - dimension]
            c = float(np.cos(angle))
            s = float(np.sin(angle))
            matrix = np.asarray(
                [
                    [np.exp(1j * left_phase) * c, -np.exp(-1j * right_phase) * s],
                    [np.exp(1j * right_phase) * s, np.exp(-1j * left_phase) * c],
                ],
                dtype=complex,
            )

        updated = state.copy()
        for label0 in range(dimension):
            if label0 & target:
                continue
            if (label0 & gate.ctrl_mask) != gate.ctrl_mask:
                continue
            if label0 & gate.anti_mask:
                continue
            label1 = label0 | target
            updated[label0] = matrix[0, 0] * state[label0] + matrix[0, 1] * state[label1]
            updated[label1] = matrix[1, 0] * state[label0] + matrix[1, 1] * state[label1]
        state = updated
    return state


class NativeScheduleTests(unittest.TestCase):
    def test_four_qubit_native_real_schedule_matches_first_paper_table(self) -> None:
        schedule = native_real_schedule(4)
        self.assertEqual(
            [gate.ctrl_mask for gate in schedule],
            [0, 0, 0, 0, 2, 4, 4, 8, 8, 8, 6, 10, 12, 12, 14],
        )
        self.assertEqual(
            [gate.anti_mask for gate in schedule],
            [0, 8, 12, 14, 0, 0, 2, 0, 4, 6, 0, 0, 0, 2, 0],
        )
        self.assertEqual(
            [gate.target_mask for gate in schedule],
            [8, 4, 2, 1, 1, 2, 1, 4, 2, 1, 1, 1, 2, 1, 1],
        )
        self.assertEqual(
            [gate.theta_index for gate in schedule],
            [1, 2, 4, 8, 9, 5, 10, 3, 6, 12, 11, 13, 7, 14, 15],
        )

    def test_four_qubit_native_complex_promotions(self) -> None:
        indices = [gate.theta_index for gate in native_complex_schedule(4)]
        self.assertEqual(
            indices,
            [
                1,
                2,
                4,
                (8, 16, 17),
                (9, 18, 19),
                5,
                (10, 20, 21),
                3,
                6,
                (12, 24, 25),
                (11, 22, 23),
                (13, 26, 27),
                7,
                (14, 28, 29),
                (15, 30, 31),
            ],
        )

    def test_native_schedule_masks_are_well_formed(self) -> None:
        for n in range(1, 9):
            for case, schedule in (
                ("real", native_real_schedule(n)),
                ("complex", native_complex_schedule(n)),
            ):
                with self.subTest(n=n, case=case):
                    self.assertEqual(len(schedule), (1 << n) - 1)
                    for gate in schedule:
                        self.assertEqual(gate.ctrl_mask & gate.anti_mask, 0)
                        self.assertEqual(
                            gate.target_mask & (gate.ctrl_mask | gate.anti_mask), 0
                        )
                        self.assertGreater(gate.target_mask, 0)
                        self.assertEqual(
                            gate.target_mask & (gate.target_mask - 1), 0
                        )
                        self.assertLess(
                            gate.ctrl_mask | gate.anti_mask | gate.target_mask,
                            1 << n,
                        )

    def test_native_real_schedule_prepares_recursive_state(self) -> None:
        for n in range(1, 6):
            for theta_mag in (regular_theta_mag(n), singular_theta_mag(n)):
                with self.subTest(n=n, singular=bool(np.any(theta_mag == 0.0))):
                    np.testing.assert_allclose(
                        _apply_native_real_schedule(theta_mag),
                        real_tree_data(theta_mag).state,
                        atol=2e-12,
                        rtol=0.0,
                    )

    def test_native_complex_schedule_prepares_recursive_state(self) -> None:
        for n in range(1, 6):
            theta_mag = complex_theta_mag(n)
            theta_phase = theta_ph(n)
            with self.subTest(n=n):
                np.testing.assert_allclose(
                    _apply_native_complex_schedule(theta_mag, theta_phase),
                    complex_state(theta_mag, theta_phase),
                    atol=2e-12,
                    rtol=0.0,
                )

    def test_four_qubit_native_assigned_charges(self) -> None:
        self.assertEqual(native_real_cnot_charge(4), 100)
        self.assertEqual(native_complex_cnot_charge(4), 100)


if __name__ == "__main__":
    unittest.main()
