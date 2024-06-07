import unittest
import numpy as np
import random
from perceval import Matrix
import cmath

from tomography.estimating_overlaps import GramMatrixFromVariance

def random_preparation(n):
    """
    Generate a random unitary matrix of dimension n.
    """
    return Matrix.random_unitary(n).tolist()

def overlap_calculation_for_three_modes(gamma, beta, alpha, phi):
    """
    Calculate overlaps for three modes based on input parameters.
    
    Parameters:
    gamma, beta, alpha (float): Angles in radians.
    phi (float): Phase angle in radians.
    
    Returns:
    Tuple[float, float, float]: Overlap values r_AB, r_BC, r_AC.
    """
    r_AB = cmath.cos(beta * cmath.pi / 2)
    r_AB *= np.conjugate(r_AB)
    r_AB = np.real(r_AB)
    r_BC = cmath.cos(gamma * cmath.pi / 2) * cmath.cos(beta * cmath.pi / 2) + cmath.sin(gamma * cmath.pi / 2) * cmath.sin(beta * cmath.pi / 2) * cmath.sin(alpha * cmath.pi / 2) * cmath.exp(phi * cmath.pi * (0 + 1j))
    r_BC *= np.conjugate(r_BC)
    r_BC = np.real(r_BC)
    r_AC = cmath.cos(gamma * cmath.pi / 2)
    r_AC *= np.conjugate(r_AC)
    r_AC = np.real(r_AC)

    return (r_AB, r_BC, r_AC)

def random_GramMatrix_three_modes():
    """
    Generate a random Gram matrix for three modes.
    
    Returns:
    List[List[float]]: The random Gram matrix.
    """
    gamma = random.random() * (np.pi / 2)
    beta = random.random() * (np.pi / 2)
    alpha = random.random() * (np.pi / 2)
    phi = random.random() * (np.pi)

    r_AB, r_BC, r_AC = overlap_calculation_for_three_modes(gamma, beta, alpha, phi)

    r_CA = r_AC
    r_BA = r_AB
    r_CB = r_BC

    gram_matrix = [[1, r_AB, r_AC],
                   [r_BA, 1, r_BC],
                   [r_CA, r_CB, 1]]
    
    return gram_matrix

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
