import unittest
import numpy as np
import random
from perceval import Matrix
import cmath

from base.circuit_helpers import random_GramMatrix_three_modes, random_preparation
from tomography.estimating_overlaps import GramMatrixFromVariance

class TestGramMatrixFromVariance(unittest.TestCase):

    def setUp(self):
        self.variance_calculator = GramMatrixFromVariance()

    def test_sum_all(self):
        matrix = random_GramMatrix_three_modes()
        expected_variance = 0.5
        result = self.variance_calculator.sum_all(matrix, expected_variance, 3)
        self.assertIsInstance(result, float)

    def test_sum_all_4(self):
        matrix = random_GramMatrix_three_modes()
        result = self.variance_calculator.sum_all_4(matrix, 3)
        self.assertIsInstance(result, float)

    def test_calculate_variable_coefficients(self):
        matrix = random_GramMatrix_three_modes()
        result = self.variance_calculator.calculate_variable_coefficients(matrix, 3)
        self.assertIsInstance(result, dict)

    def test_to_vector(self):
        matrix = random_GramMatrix_three_modes()
        var_map = self.variance_calculator.calculate_variable_coefficients(matrix, 3)
        result = self.variance_calculator.to_vector(var_map, 3)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

    def test_find_overlaps(self):
        matrix_variance_pairs = [(random_GramMatrix_three_modes(), 0.5), (random_GramMatrix_three_modes(), 0.7), (random_GramMatrix_three_modes(), 0.8)]
        result = self.variance_calculator.find_overlaps(matrix_variance_pairs, 3)
        self.assertIsInstance(result, np.ndarray)

    def test_calculate_expected_variance(self):
        gram_matrix = random_GramMatrix_three_modes()
        interferometer = random_preparation(3)
        result = self.variance_calculator.calculate_expected_variance(gram_matrix, interferometer)
        self.assertIsInstance(result, float)

if __name__ == '__main__':
    unittest.main()
