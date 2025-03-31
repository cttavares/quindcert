import logging
import random
import numpy as np
import cmath

from typing import Tuple

from perceval import Matrix
from base import AbstractCircuit

def random_preparation(n):
    """
    Generate a random unitary matrix of dimension n.
    """
    return Matrix.random_unitary(n).tolist()



def fully_indistinguishable_matrix (n):
    matrix_of_ones = [[1 for _ in range(n)] for _ in range(n)]
    return matrix_of_ones

def fully_distinguishable_matrix (n):
    return constant_matrix_gram_matrix (n, 0)

def random_matrix (n):
    m = np.zeros ((n,n))
    for i in range (n): 
        for j in range (n):
            if i == j:
                m [i][j] = 1
            else:
                m [i][j] = random.randint(0, 100)*0.01 
    
    return m
    
def constant_matrix_gram_matrix (n, v):
    m = np.zeros ((n,n))
    for i in range (n): 
        for j in range (n):
            if i == j:
                m [i][j] = 1
            else:
                m [i][j] = v
    
    return m
    
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

def generate_matrix_from_parameters (gamma, beta, alpha, phi):

    r_AB, r_BC, r_AC = overlap_calculation_for_three_modes(gamma, beta, alpha, phi)

    r_CA = r_AC
    r_BA = r_AB
    r_CB = r_BC

    gram_matrix = [[1, r_AB, r_AC],
                   [r_BA, 1, r_BC],
                   [r_CA, r_CB, 1]]
    
    return gram_matrix


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


def fourier_matrix(matrix_dimension):
    """
    Generate the Fourier matrix for a given dimension.

    Parameters:
    matrix_dimension (int): The dimension of the Fourier matrix.

    Returns:
    np.ndarray: The generated Fourier matrix.
    """
    fourier = np.zeros ((matrix_dimension,matrix_dimension),dtype=np.complex_)
    root_of_unity = 2 * np.pi * 1j

    for y in range(0, matrix_dimension):
        for x in range(0, matrix_dimension):
            fourier [x][y] = np.exp(root_of_unity*y*x/matrix_dimension)
    
    phases = np.zeros ((matrix_dimension,matrix_dimension),dtype=np.complex_)
    for y in range(0, matrix_dimension):
        for x in range(0, matrix_dimension):
            phases [x][y] = cmath.phase (cmath.exp (root_of_unity*y*x/matrix_dimension))
    
    logging.debug ("Phases {}".format (phases))
    
    # Normalize the Fourier matrix
    fourier*=1/np.sqrt(matrix_dimension)
    
    logging.debug ("Fourier matrix {}".format (fourier))
    
    return fourier
    
def is_unitary(m: np.ndarray) -> bool:
    """
    Check if a matrix is unitary.

    Parameters:
    m (np.ndarray): The matrix to check.

    Returns:
    bool: True if the matrix is unitary, False otherwise.
    """
    return np.allclose(np.eye(len(m)), m.dot(m.T.conj()))

def generate_fourier_transform_circuit (dimension):
    """
    Generate a Fourier transform circuit.
    
    Parameters:
    dimension (int): The dimension of the circuit.
    
    Returns:
    AbstractCircuit: The generated Fourier transform circuit.
    """
    return AbstractCircuit (dimension, fourier_matrix (dimension))

def generate_random_abstract_circuit (dimension):
    return AbstractCircuit (dimension, random_preparation (dimension))