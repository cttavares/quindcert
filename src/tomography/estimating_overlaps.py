import itertools
import functools
import numpy as np
import perceval as pcvl

from typing import List, Dict, Tuple

class GramMatrixFromVariance:

    def __init__ (self):
        pass
    
    # Including our own helpers
    def sum_all(self, matrix: List[List[float]], expected_variance: float, n: int) -> float:
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
        print ("Sum 4: ", sum_4)
        return expected_variance - 1 + 1/n * sum_4

    def sum_all_4(self, matrix: List[List[float]], n: int) -> float:
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

    def calculate_variable_coefficients(self, matrix: List[List[float]], n: int) -> Dict[Tuple[int, int], float]:
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
           
        print ("Coeficients: ",  results)
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
        
        if (n-1) % 2 == 0:
            var_number = (n-1)//2 * n
        else:
            var_number = (n-1)//2 * n + n//2
    
        print ("N: ", n)
        print ("Var number: ", var_number)
    
        vars = [0 for _ in range (0, var_number)]
        print ("Vars:_", vars)
        for i in var_map:
            (l,c) = i
            pos = l * (n-1) + (c-(l+1)) 
            vars [pos] = var_map [i]
    
        print (vars)
        return vars

    # This function solves equations about expected variance of the form A.X = B
    def find_overlaps(self, matrices_variance_pairs: List[Tuple[List[List[float]], float]], n: int) -> List[float]:
        """
        Solve the system of equations A.X = B to find the overlaps.

        Parameters:
        matrices_variance_pairs (List[Tuple[List[List[float]], float]]): A list of matrices and their expected variances.
        n (int): The dimension of the matrices.

        Returns:
        List[float]: The solution vector X.
        """
        A = []
        print (A)
        B = []
        for i in matrices_variance_pairs:
            B.append (self.sum_all (i [0], i [1], n))
            A.append (self.to_vector (self.calculate_variable_coefficients (i [0], n),n))
            
        A_numpy = np.array (A)
        B_numpy = np.array (B)

        print ("A: ", A_numpy)
        print ("B: ", B_numpy)
    
        print ("Determinant: ", np.linalg.det (A_numpy))
        #X = np.linalg.lstsq (A_numpy, B_numpy)
        X = np.linalg.solve (A_numpy, B_numpy)
        return X

    def calculate_expected_variance(self, gram_matrix: List[List[float]], interferometer: List[List[float]]) -> float:
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


import cmath
import perceval as pcvl
import random

# A preparation of three random matrices
def random_preparation (n):
    return pcvl.Matrix.random_unitary(n)
    #return fourier_matrix (n)

def overlap_calculation_for_three_modes (gamma, beta, alpha, phi):
 # So the parameters have the following restrictions:
    #           - alpha, beta, gama: [0, pi/2]
    #           - phi: [0, 2pi]
    #r_BC = cmath.cos (beta)
    r_AB = cmath.cos (beta*cmath.pi/2)
    r_AB *= np.conjugate (r_AB)
    r_AB = np.real(r_AB)
    r_BC = cmath.cos (gamma*cmath.pi/2) * cmath.cos (beta*cmath.pi/2) + cmath.sin (gamma*cmath.pi/2) * cmath.sin (beta*cmath.pi/2) * cmath.sin (alpha*cmath.pi/2) * cmath.exp(phi*cmath.pi * (0 + 1j))
    r_BC *= np.conjugate (r_BC)
    r_BC = np.real (r_BC)
    r_AC = cmath.cos (gamma*cmath.pi/2)
    r_AC *= np.conjugate (r_AC)
    r_AC = np.real (r_AC)

    return (r_AB, r_BC, r_AC)

def random_GramMatrix_three_modes ():

    gamma = random.random()*(np.pi/2)
    beta = random.random()*(np.pi/2)
    alpha = random.random()*(np.pi/2)

    phi = random.random()*(np.pi)

    (r_AB, r_BC, r_AC) = overlap_calculation_for_three_modes (gamma, beta, alpha, phi)

    r_CA = r_AC
    r_BA = r_AB
    r_CB = r_BC

    gram_matrix = [[1, r_AB, r_AC],
                   [r_BA, 1, r_BC],
                   [r_CA, r_CB, 1]]
    
    #gram_matrix =  [[1, 1, 1],
    #               [1, 1, 1],
    #               [1, 1, 1]]
       
    return gram_matrix