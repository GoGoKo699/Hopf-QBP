from __future__ import annotations

import unittest

import numpy as np
from qibo import gates, models

from qbp_validation.circuits import add_y_basis_rotation, probabilities, statevector


class CircuitConventionTests(unittest.TestCase):
    def test_qibo_index_zero_is_most_significant(self) -> None:
        circuit = models.Circuit(2)
        circuit.add(gates.X(0))
        expected = np.zeros(4, dtype=complex)
        expected[0b10] = 1.0
        np.testing.assert_allclose(statevector(circuit), expected, atol=1e-12, rtol=0.0)

    def test_sdag_then_h_decodes_positive_y_as_bit_zero(self) -> None:
        circuit = models.Circuit(1)
        circuit.add(gates.H(0))
        circuit.add(gates.Unitary(np.diag([1.0, 1.0j]), 0))
        add_y_basis_rotation(circuit, 0)
        np.testing.assert_allclose(probabilities(circuit), [1.0, 0.0], atol=1e-12, rtol=0.0)


if __name__ == "__main__":
    unittest.main()
