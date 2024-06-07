from abc import ABC, abstractmethod
from base.abstract_circuit import AbstractCircuit
from base.devices import Device

class DeviceProcessTomographyProber (ABC):

    def __init__ (self, device: Device):
        """
        Initialize the DeviceProcessTomographyProber with a device.

        Parameters:
        device (Device): The device to use for the tomography prober.
        """
        self.device = device
        self.circuit = None
        self.single_photon_experiments_results = None
        self.double_photon_experiments_results = None
    
    def define_circuit (self, original: AbstractCircuit):
        """
        Define the circuit to be used for the experiments.

        Parameters:
        circuit: The circuit to set.
        """
        self.circuit = original

    @abstractmethod
    def make_experimental_bunch (self):
        """
        Execute experimental bunching for single and double photon experiments.
        This method must be implemented by subclasses.
        """
        pass

    def get_single_photon_experiments (self):
        """
        Get the results of the single photon experiments.

        Returns:
        Optional[StatesAndProbabilities]: The results of the single photon experiments.
        """    
        return self.single_photon_experiments_results

    def get_double_photon_experiments (self):
        """
        Get the results of the double photon experiments.

        Returns:
        Optional[StatesAndProbabilities]: The results of the double photon experiments.
        """
        return self.double_photon_experiments_results
