import unittest
import numpy as np
import cmath
from base.circuit_helpers import fourier_matrix, is_unitary, generate_fourier_transform_circuit
from base import AbstractCircuit

class TestFourierTransform(unittest.TestCase):

    def test_fourier_matrix(self):
        matrix_dimension = 2
        matrix = fourier_matrix(matrix_dimension)
        expected = np.array([[1 / np.sqrt(2) + 0j, 1 / np.sqrt(2) + 0j],
                             [1 / np.sqrt(2) + 0j, -1 / np.sqrt(2) + 0j]])
        np.testing.assert_almost_equal(matrix, expected, decimal=6, err_msg="Fourier matrix generation failed.")

    def test_is_unitary(self):
        matrix = fourier_matrix(2)
        self.assertTrue(is_unitary(matrix), "Unitary check failed for Fourier matrix.")

    def test_generate_fourier_transform_circuit(self):
        dimension = 2
        circuit = generate_fourier_transform_circuit(dimension)
        expected_matrix = np.array([[1 / np.sqrt(2) + 0j, 1 / np.sqrt(2) + 0j],
                                    [1 / np.sqrt(2) + 0j, -1 / np.sqrt(2) + 0j]])
        self.assertIsInstance(circuit, AbstractCircuit, "Circuit creation failed.")
        np.testing.assert_almost_equal(circuit.m, expected_matrix, decimal=6, err_msg="Fourier transform circuit generation failed.")

if __name__ == "__main__":
    unittest.main()
