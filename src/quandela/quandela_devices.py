from enum import Enum
from typing import Any, Dict

import perceval as pcvl

from base import AbstractCircuit

from base.devices import Device, DeviceFactory, DeviceMode
from base.results import StatesAndProbabilities
from quandela.enchancedanalyzer import EnhancedAnalyzer
from quandela.circuit_helpers import approximate_with_MZ

class QuandelaLocalDevices (Enum):
    NAIVE = "Naive"
    SLOS = "SLOS"
    STEP = "Stepper"
    MPS = "MPS"
    CLIFFORD = "CliffordClifford2017"

class QuandelaRemoteDevices (Enum):
    QPU_ASCELLA = "qpu:ascella"
    SIM_ASCELLA = "sim:ascella"
    SIM_CLIFFORD = "sim:clifford"

class QuandelaDeviceFactory (DeviceFactory):
    """
    Factory class for creating Quandela devices and processors.
    """
    def create_local_processor (self, name: str) -> pcvl.Processor:
        """
        Create a local processor with the given name.

        Parameters:
        name (str): The name of the local processor. Acceptable names are:
                    "CliffordClifford2017", "SLOS", "Naive", "Stepper", "MPS".

        Returns:
        pcvl.Processor: The created local processor.
        """
        assert ((name == "CliffordClifford2017") or (name == "SLOS") 
                or (name == "Naive") or (name == "Stepper") or (name == "MPS")), "Local processor unknown."
        return pcvl.Processor(name)
    
    
    def create_remote_processor (self, name: str, token: str) -> pcvl.RemoteProcessor:
        """
        Create a remote processor with the given name and token.

        Parameters:
        name (str): The name of the remote processor. Acceptable names are:
                    "qpu:ascella", "sim:ascella", "sim:clifford".
        token (str): The token for authentication.

        Returns:
        pcvl.RemoteProcessor: The created remote processor.
        """
        assert ((name == "qpu:ascella") or (name == "sim:ascella") or (name == "sim:clifford")), "Remote processor unknown."
        return pcvl.RemoteProcessor(name, token)

    def create_remote_device (self, name: str, mode: DeviceMode, token: str) -> Device:
        """
        Create a remote device with the given name, mode, and token.

        Parameters:
        name (str): The name of the remote processor.
        mode (str): The mode of the device.
        token (str): The token for authentication.

        Returns:
        QuandelaDevice: The created remote device.
        """
        return QuandelaDevice (self.create_remote_processor (name, token), str (mode))

    def create_local_device (self, name: str, mode: DeviceMode) -> Device:
        """
        Create a local device with the given name and mode.

        Parameters:
        name (str): The name of the local processor.
        mode (str): The mode of the device.

        Returns:
        QuandelaDevice: The created local device.
        """   
        return QuandelaDevice (self.create_local_processor (name), mode)

class QuandelaDevice (Device):

    @staticmethod
    def abstract_circuit_to_quandela_circuit (circuit: AbstractCircuit) -> pcvl.Circuit:
        """
        Convert an AbstractCircuit to a Quandela Circuit.

        Parameters:
        circuit (AbstractCircuit): The abstract circuit to convert.

        Returns:
        pcvl.Circuit: The corresponding Quandela circuit.
        """
        return approximate_with_MZ (circuit.m)
    
    @staticmethod
    def quandela_circuit_to_abstract_circuit (circuit: pcvl.Circuit) -> AbstractCircuit:
        """
        Convert a Quandela Circuit to an AbstractCircuit.

        Parameters:
        circuit (pcvl.Circuit): The Quandela circuit to convert.

        Returns:
        AbstractCircuit: The corresponding abstract circuit.
        """
        return AbstractCircuit (circuit.compute_unitary ())
    
    def __init__ (self, processor: pcvl.Processor, mode: DeviceMode, number_of_samples: int = 1000):
        """
        Initialize the QuandelaDevice with a processor, mode, and number of samples.

        Parameters:
        processor (pcvl.Processor): The processor to use.
        mode (DeviceMode): The mode of the device (SAMPLER or ANALYZER).
        number_of_samples (int): The number of samples to use for the experiment. Default is 1000.
        """
        self.processor = processor
        self.number_of_samples = number_of_samples
        self.mode = mode
       
    # Example of initial state '|1,1>'
    def set_initial_state(self, input_state: str) -> None:
        """
        Set the initial state of the device.

        Parameters:
        input_state (str): The initial state to set (e.g., '|1,1>').
        """
        self.processor.with_input(pcvl.BasicState(input_state))
        
    def set_circuit(self, circuit: AbstractCircuit) -> None:
        """
        Set the circuit for the device.

        Parameters:
        circuit (AbstractCircuit): The abstract circuit to set.
        """
        self.processor.set_circuit (QuandelaDevice.abstract_circuit_to_quandela_circuit (circuit))
    
    def fill_results (self, job_results: Dict[str, Any]) -> StatesAndProbabilities:
        """
        Fill the results based on the job results.

        Parameters:
        job_results (Dict[str, Any]): The job results from the processor.

        Returns:
        StatesAndProbabilities: The filled results.
        """
        return_results = StatesAndProbabilities ()
        
        if self.mode == DeviceMode.SAMPLER:
            
            total_count = 0
            for i in job_results:
                total_count += job_results [i]

            for i in job_results:
                return_results.set_probability (str (i), job_results [i]/total_count)
                return_results.set_counting (str (i), job_results [i])
        
        else:
            for index, i in enumerate (job_results ['output_states']):
                 return_results.set_probability (str (i), job_results ['results'][0][index])   

        return return_results
     
    def execute_experiment_(self) -> StatesAndProbabilities:
        """
        Execute the experiment based on the current mode and settings.

        Returns:
        StatesAndProbabilities: The results of the experiment.
        """
        if self.mode == DeviceMode.SAMPLER:
            # First it is necessary to create a sampler using the processor
            sampler = pcvl.algorithm.Sampler(self.processor)
            # Sampler exposes 'sample_count' returning a dictionary {state: count}
            job = sampler.sample_count(self.number_of_samples)
            return self.fill_results (job ['results'])
        else:
            analyzer = EnhancedAnalyzer (self.processor, [pcvl.BasicState (self.processor.input_state)])
            return self.fill_results (analyzer.compute ())    
    
    def execute_experiment(self, initial_state: str, circuit: AbstractCircuit) -> StatesAndProbabilities:
        """
        Execute an experiment with the given initial state and circuit.

        Parameters:
        initial_state (str): The initial state to set (e.g., '|1,1>').
        circuit (AbstractCircuit): The abstract circuit to set.

        Returns:
        StatesAndProbabilities: The results of the experiment.
        """
        self.set_circuit (circuit)
        self.set_initial_state (initial_state)
        return self.execute_experiment_ ()
    

