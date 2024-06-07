from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Type

from base.results import StatesAndProbabilities
from base.abstract_circuit import AbstractCircuit

class DeviceMode(Enum):
    SAMPLER = "Sampler"
    ANALYZER = "Analyzer"

class DeviceFactory (ABC):

    @abstractmethod
    def create_remote_device(self, name, mode: DeviceMode, token: str) -> 'Device':
        """
        Creates a remote device with the given name, mode, and token.

        Parameters:
        name (str): The name of the device.
        mode (DeviceMode): The mode of the device.
        token (str): The token for authentication.

        Returns:
        Device: The created remote device.
        """
        pass

    @abstractmethod
    def create_local_device(self, name, mode: DeviceMode) -> 'Device':
        """
        Creates a local device with the given name and mode.

        Parameters:
        name (str): The name of the device.
        mode (DeviceMode): The mode of the device.

        Returns:
        Device: The created local device.
        """
        pass

class Device (ABC):

    def __init__(self, input_state: Optional[str], circuit: Optional[AbstractCircuit]):
        """
        Initializes the Device with an input state and a circuit.

        Parameters:
        input_state (Optional[str]): The initial state of the device.
        circuit (Optional[AbstractCircuit]): The circuit of the device.
        """
        if input_state is not None:
            self.set_initial_state(input_state)
        
        if circuit is not None:
            self.set_circuit(circuit)

    @abstractmethod
    def set_initial_state(self, input_state: str):
        """
        Sets the initial state of the device.

        Parameters:
        input_state (str): The initial state to set.
        """
        pass
    
    @abstractmethod
    def set_circuit (self, circuit: AbstractCircuit):
        """
        Sets the circuit of the device.

        Parameters:
        circuit (AbstractCircuit): The circuit to set.
        """
        pass
    
    @abstractmethod
    def execute_experiment_ (self) -> StatesAndProbabilities:
        """
        Executes the experiment with the current state and circuit.

        Returns:
        Results: The results of the experiment.
        """
        pass

    def execute_experiment (self, initial_state: str, circuit: AbstractCircuit) -> StatesAndProbabilities:
        """
        Executes the experiment with the given initial state and circuit.

        Parameters:
        initial_state (str): The initial state to use.
        circuit (AbstractCircuit): The circuit to use.

        Returns:
        Results: The results of the experiment.
        """
        self.set_circuit (circuit)
        self.set_initial_state (initial_state)
        return self.execute_experiment_ ()  


