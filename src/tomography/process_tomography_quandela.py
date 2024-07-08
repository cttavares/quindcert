# Some licensing message
#
# This piece of code aims at generating a bunch of randomized circuits, and evaluate their bunching probability.
#

# Including our own helpers
import numpy as np
import logging

from base.abstract_circuit import AbstractCircuit


from base.circuit_helpers import generate_fourier_transform_circuit
from tomography.process_tomography_methods import ProcessTomographyMethod
from tomography.tomography_probers import DeviceProcessTomographyProber


class DeviceCharacterizer:

    def __init__ (self, number_of_modes: int , tomography_device: DeviceProcessTomographyProber, process_tomography_method: ProcessTomographyMethod):
        """
        Initialize the DeviceCharacterizer with the number of modes, a tomography device, and a process tomography method.

        Parameters:
        number_of_modes (int): The number of modes for the device.
        tomography_device (DeviceProcessTomographyProber): The device used for process tomography.
        process_tomography_method (ProcessTomographyMethod): The method used for process tomography.
        """
        self.number_of_modes = number_of_modes
        self.tomography_device = tomography_device
        self.process_tomography_method = process_tomography_method
        self.original = None
    
    def set_circuit (self, circuit: AbstractCircuit):
        self.original = circuit

    def reconstruct_state (self):
        """
        Reconstruct the state using the process tomography method.

        Returns:
        Any: The reconstructed state.
        """
        single_photon_results = self.tomography_device.get_single_photon_experiments ()
        double_photon_results = self.tomography_device.get_double_photon_experiments ()

        #process_tomography_method = SuperStableMethod (number_of_modes, single_photon_results, double_photon_results)
        self.process_tomography_method.set_single_photon_experiments_results (single_photon_results)
        self.process_tomography_method.set_double_photon_experiments_results (double_photon_results)
        
        return self.process_tomography_method.recover_state ()

    def generate_some_circuit (self, number_of_modes: int) -> AbstractCircuit:
        """
        Generate a Fourier transform circuit for the given number of modes.

        Parameters:
        number_of_modes (int): The number of modes.

        Returns:
        Any: The generated Fourier transform circuit.
        """
        #return generate_random_circuit (number_of_modes)
        return generate_fourier_transform_circuit (number_of_modes)

    def calculate_distance_between_matrices (self, matrix_1, matrix_2):
        """
        Calculate the distance between two matrices using their density operators.

        Parameters:
        matrix_1 (np.ndarray): The first matrix.
        matrix_2 (np.ndarray): The second matrix.

        Returns:
        float: The calculated distance.
        """
        density_operator_1 = np.matrix (matrix_1) * np.matrix (matrix_1).getH() 
        density_operator_2 = np.matrix (matrix_2) * np.matrix (matrix_2).getH()
    
        logging.debug ("Density operator 1: " + str (density_operator_1))
        logging.debug ("Density operator 2: " + str (density_operator_2))
    
        return np.trace(np.dot (density_operator_1, density_operator_2))

    def characterize_device (self):
        """
        Characterize the device by generating a circuit, performing process tomography, and calculating the distance between the original and reconstructed matrices.

        Returns:
        Tuple[np.ndarray, Any, float]: A tuple containing the original unitary, the reconstructed state, and the distance.
        """
        if self.original is None:
            self.original = self.generate_some_circuit (self.number_of_modes)

        self.tomography_device.define_circuit (self.original)
        self.tomography_device.make_experimental_bunch ()
        
        logging.debug ("[Process Tomography prober] Total single photon results {}".format (self.tomography_device.get_single_photon_experiments ()))
        logging.debug ("[Process Tomography prober] Total double photon results {}".format (self.tomography_device.get_double_photon_experiments ()))

        rebuilt = self.reconstruct_state ()
        logging.debug (rebuilt)

        distance = self.calculate_distance_between_matrices (rebuilt, self.original.m)
        logging.debug ("And the distance is ba-dum-pssh:" + str (distance))
    
        return (self.original.m, rebuilt, distance)    













    

                
    
