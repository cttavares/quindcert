import unittest
import numpy as np
from base.abstract_circuit import AbstractCircuit

class TestAbstractCircuit(unittest.TestCase):
    def test_initialization_with_identity(self):
        n = 3
        circuit = AbstractCircuit(n)
        expected_matrix = np.eye(n)
        np.testing.assert_array_almost_equal(circuit.m, expected_matrix, err_msg="Initialization with identity matrix failed")

    def test_initialization_with_custom_matrix(self):
        custom_matrix = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        circuit = AbstractCircuit(2, custom_matrix)
        np.testing.assert_array_almost_equal(circuit.m, custom_matrix, err_msg="Initialization with custom matrix failed")

    def test_non_unitary_initialization_raises_error(self):
        non_unitary_matrix = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError, msg="Non-unitary matrix initialization did not raise error"):
            AbstractCircuit(2, non_unitary_matrix)

    def test_is_unitary(self):
        unitary_matrix = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        circuit = AbstractCircuit(2, unitary_matrix)
        self.assertTrue(circuit.is_unitary(), "is_unitary method failed for a unitary matrix")

    def test_compose_with_unitary_matrix(self):
        hadamard = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        pauli_x = np.array([[0, 1], [1, 0]])
        expected_composed_matrix = (1/np.sqrt(2)) * np.array([[1, 1], [-1, 1]])

        circuit1 = AbstractCircuit(2, hadamard)
        circuit2 = AbstractCircuit(2, pauli_x)
        circuit1.compose(circuit2)
        np.testing.assert_array_almost_equal(circuit1.m, expected_composed_matrix, err_msg="Composition with unitary matrix failed")

if __name__ == "__main__":
    unittest.main()