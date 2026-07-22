from __future__ import annotations

import unittest

import numpy as np
from qibo import gates, models

from qbp_validation.circuits import add_y_basis_rotation, probabilities


class CircuitConventionTests(unittest.TestCase):
    def test_qibo_qubit_zero_is_most_significant(self) -> None:
        circuit = models.Circuit(3)
        circuit.add(gates.X(0))
        state = np.asarray(circuit().state())
        self.assertEqual(int(np.argmax(np.abs(state))), 0b100)

    def test_y_basis_rotation_has_manuscript_sign(self) -> None:
        # Prepare |+i> = S H |0>.  S^dagger followed by H must map it to |0>.
        circuit = models.Circuit(1)
        circuit.add(gates.H(0))
        circuit.add(gates.Unitary(np.diag([1.0, 1.0j]), 0))
        add_y_basis_rotation(circuit, 0)
        probs = probabilities(circuit)
        np.testing.assert_allclose(probs, [1.0, 0.0], atol=1e-13, rtol=0.0)


if __name__ == "__main__":
    unittest.main()
