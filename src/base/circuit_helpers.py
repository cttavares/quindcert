import logging
import numpy as np
import cmath

from typing import Tuple
from base import AbstractCircuit

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
    
    print (is_unitary(fourier))
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