import itertools
import functools
import numpy as np
import perceval as pcvl

from typing import List, Dict, Tuple

from base.abstract_circuit import AbstractCircuit
from photonic_indistinguishability_measures.variance import Variance
from quandela.circuit_helpers import generate_random_circuit
from tomography.process_tomography_quandela import DeviceCharacterizer

class GramMatrixFromVariance:

    def __init__ (self, variance_calculator: Variance, device_characterizer: DeviceCharacterizer):
        self.variance_calculator = variance_calculator
        self.device_characterizer = device_characterizer
    
    # Including our own helpers
    def sum_all(self, matrix: List[List[complex]], expected_variance: float, n: int) -> float:
        """
        Calculate the sum of all elements with a specific transformation.

        Parameters:
        matrix (np.ndarray): The input matrix.
        expected_variance (float): The expected variance.
        n (int): The dimension of the matrix.

        Returns:
        float: The transformed sum.
        """
        sum_4 = self.sum_all_4(matrix, n)
        #print ("Sum 4: ", sum_4)
        return expected_variance - 1 + 1/n * sum_4

    def sum_all_4(self, matrix: List[List[complex]], n: int) -> float:
        """
        Calculate the sum of the fourth power of the absolute values of the matrix elements.

        Parameters:
        matrix (List[List[float]]): The input matrix.
        n (int): The dimension of the matrix.

        Returns:
        float: The sum of the fourth powers.
        """
        sum_4 = 0
        for i in range (0, n):
            for j in range (0, n):
                sum_4 += abs(matrix [i][j])**4
        return sum_4

    def calculate_variable_coefficients(self, matrix: List[List[complex]], n: int) -> Dict[Tuple[int, int], float]:
        """
        Calculate variable coefficients for the matrix.

        Parameters:
        matrix (List[List[float]]): The input matrix.
        n (int): The dimension of the matrix.

        
        Returns:
        Dict[Tuple[int, int], float]: A dictionary of variable coefficients.
        """
        results = {}
        for j in itertools.product (range (0, n), repeat = 2):
            (a, b) = j
            if (a != b):
                coeficient = (1/n * functools.reduce (lambda x, y: x+y, [abs (matrix [i][a])**2 * abs (matrix [i][b])**2 for i in range (0, n)]))   
                if b > a:
                    results [(a, b)] = coeficient
                else:
                    results [(b, a)] += coeficient
           
        #print ("Coeficients: ",  results)
        return results

    def to_vector(self, var_map: Dict[Tuple[int, int], float], n: int) -> List[float]:
        """
        Convert a dictionary of variable coefficients to a vector.

        Parameters:
        var_map (Dict[Tuple[int, int], float]): The variable coefficients.
        n (int): The dimension of the matrix.

        Returns:
        List[float]: The vector of coefficients.
        """
        var_number = ((n * (n-1)) // 2) 
        vars = [0 for _ in range (var_number)]
        
        for i in var_map:
            (l,c) = i
            start_point = sum([n-(d+1) for d in range (l)])
            #print ("Start point: ", start_point)
            # pos = l * (n-1) + (c-(l+1))
            pos = start_point + (c-(l+1))
            #print ("Pos: ", pos) 
            vars [pos] = var_map [i]
    
        #print (vars)
        return vars

    # This function solves equations about expected variance of the form A.X = B
    def find_overlaps(self, matrices_variance_pairs: List[Tuple[List[List[complex]], float]], n: int) -> List[float]:
        """
        Solve the system of equations A.X = B to find the overlaps.

        Parameters:
        matrices_variance_pairs (List[Tuple[List[List[float]], float]]): A list of matrices and their expected variances.
        n (int): The dimension of the matrices.

        Returns:
        List[float]: The solution vector X.
        """
        print ("Matrices: " + str (matrices_variance_pairs))
        A, B = self.transform_into_equational_system (matrices_variance_pairs, n)
            
        A_numpy = np.array (A)
        B_numpy = np.array (B)

        print ("A: ", A_numpy)
        print ("B: ", B_numpy)
        
        det = np.linalg.det (A_numpy)
        print ("Determinant: ", )
        print ("Condition number: ", np.linalg.cond (A))
        
        if det != 0:
            X = np.linalg.solve (A_numpy, B_numpy)
            return X
        else:
            raise Exception ("Indeterminate system")
      
    def transform_into_equational_system(self, matrices_variance_pairs, n):
        A = []
        B = []
        
        for i in matrices_variance_pairs:
            B.append (self.sum_all (i [0], i [1], n))
            A.append (self.to_vector (self.calculate_variable_coefficients (i [0], n),n))
       
        return A,B

    def calculate_expected_variance(self, gram_matrix: List[List[float]], interferometer: List[List[complex]]) -> float:
        """
        Calculate the expected variance for a given Gram matrix and interferometer.

        Parameters:
        gram_matrix (List[List[float]]): The Gram matrix.
        interferometer (List[List[float]]): The interferometer matrix.

        Returns:
        float: The expected variance.
        """
        n = len (gram_matrix)
        sum = 0
        for j in itertools.product (range (0, n), repeat=2):
            (a, b) = j
            if a != b:
                sum += gram_matrix [a][b] * functools.reduce (lambda x, y: x + y, [abs (interferometer [i][a])**2 * abs (interferometer [i][b])**2 for i in range (0, n)])
    
        return 1 + (1/n) * sum - (1/n) * self.sum_all_4 (interferometer, n)

    def do_experiments_to_calculate_the_gram_matrix (self, number_of_modes: int):
        number_of_preparations = ((number_of_modes * number_of_modes) - number_of_modes)//2  
        #print ("Number of necessary preparations: ", number_of_preparations)

        matrices = []
        for i in range (number_of_preparations):
            matrix = generate_random_circuit (number_of_modes).compute_unitary ()
            absCirc = AbstractCircuit (number_of_modes, matrix)
            matrices.append (absCirc)
        
        expected_variances_pairs = []
        for i in matrices:
            self.device_characterizer.set_circuit (i)
            
            characterized_matrix = (self.device_characterizer.characterize_device ()) [1]
            self.variance_calculator.device.set_circuit (i)
            
            expected_variances_pairs.append ((characterized_matrix, self.variance_calculator.execute_experiment_variance ()))

        
        X = self.find_overlaps (expected_variances_pairs, number_of_preparations)
        return X
