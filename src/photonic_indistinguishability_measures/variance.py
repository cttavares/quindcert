import logging
from typing import List, Dict, Optional

from base.abstract_circuit import AbstractCircuit
from base.results import StatesAndProbabilities
from base.state_generation_helpers import generate_state_from_list
from base.circuit_helpers import generate_fourier_transform_circuit
from base.devices import Device

class Variance:
    @staticmethod
    def calculate_minimum_three_modes(variance: float) -> float:
        """
        Calculates a transformed variance for scenarios with at least three modes.

        Parameters:
        variance (float): The input variance.

        Returns:
        float: The transformed variance.
        """
        return ((9/4)*variance - 2)**2

    @staticmethod
    def calculate_bound_average_n_modes(variance: float, variance_distinguishable: float, n: int) -> float:
        """
        Calculates the boundary for the average variance across n modes.

        Parameters:
        variance (float): The variance for indistinguishable particles.
        variance_distinguishable (float): The variance for distinguishable particles.
        n (int): The number of modes.

        Returns:
        float: The calculated boundary for the average variance.
        """
        return (1/(n*(n-1)))*((variance - 2*variance_distinguishable + 1)/(1 - variance_distinguishable))**2 - (1/(n-1))

    @staticmethod
    def calculate_max_expected_variance(n: int) -> float:
        """
        Calculates the maximum expected variance for n modes.

        Parameters:
        n (int): The number of modes.

        Returns:
        float: The maximum expected variance.
        """
        return 2 - 2/n
    
    @staticmethod
    def calculate_min_expected_variance(n: int) -> float:
        """
        Calculates the minimum expected variance for n modes.

        Parameters:
        n (int): The number of modes.

        Returns:
        float: The minimum expected variance.
        """
        return 1 - 1/n

    @staticmethod
    def calculate_expected_value_of_the_expected_variance(gram_matrix: List[List[float]], n: int) -> float:
        """
        Calculates the expected value of the variance given a Gram matrix of overlaps between modes.

        Parameters:
        gram_matrix (List[List[float]]): The Gram matrix representing overlaps between the modes.
        n (int): The number of modes.

        Returns:
        float: The expected value of the expected variance.
        """
        sum_overlaps_ab = 0
        for a in range (n):
            for  b in range (n):
                if a != b:
                    sum_overlaps_ab += gram_matrix [a][b]
        return 1 + (1/(n*(n + 1)))*sum_overlaps_ab - (2/(n+1))  
    
    @staticmethod
    def calculate_variance_value_of_the_expected_variance (gram_matrix):
        pass

    def __init__(self, device: Device, number_of_modes: int = 2):
        """
        Initializes a new instance of the Variance class.

        Parameters:
        device (Device): The quantum device used to execute experiments.
        number_of_modes (int, optional): The number of modes involved in the experiment. Defaults to 2.
        """
        self.device = device
        self.number_of_modes = number_of_modes

    def calculate_expected_value_per_mode(self, results: StatesAndProbabilities, mode: int) -> float:
        """
        Calculates the expected value of the result for a specified mode.

        Parameters:
        results (StatesAndProbabilities): The results from an experiment.
        mode (int): The mode for which to calculate the expected value.

        Returns:
        float: The expected value for the specified mode.
        """
        expected_value = 0
        for key_ in results.get_probability_states ():
            mode_ = 0
            key = str (key_)
            for occ in key[1:len(key)-1].split (","):
                if mode_ == mode:
                   expected_value = expected_value + results.get_probability (key_) * int (occ)
                   break     
                
                mode_ = mode_ + 1

        logging.debug ("[Loss Function] Expected value {}".format (expected_value))
        return expected_value

    def calculate_variance(self, results: StatesAndProbabilities, mode: int) -> float:
        """
        Calculates the variance for a specified mode based on experiment results.

        Parameters:
        results (StatesAndProbabilities): The results from an experiment.
        mode (int): The mode for which to calculate variance.

        Returns:
        float: The variance for the specified mode.
        """
        expected_value = self.calculate_expected_value_per_mode (results, mode)
        variance = 0
        for key_ in results.get_probability_states ():
            mode_ = 0
            key = str (key_)
            for occ in key[1:len(key)-1].split (","):
                if mode_ == mode:
                   variance = variance + results.get_probability (key_) * ((int (occ) - expected_value)*(int (occ) - expected_value)) 
                   break     
                
                mode_ = mode_ + 1
            
        logging.debug ("[Loss Function] Variance {}".format (variance))
        return variance
    
    def calculate_expected_variance(self, results: StatesAndProbabilities, number_of_modes: int) -> float:
        """
        Aggregates the variance over all modes to calculate the expected variance for the experiment.

        Parameters:
        results (StatesAndProbabilities): The results from an experiment.
        number_of_modes (int): The total number of modes.

        Returns:
        float: The expected variance averaged over all modes.
        """
        variance = 0
        for i in range(number_of_modes):
            variance = variance + self.calculate_variance (results, i)

        logging.debug ("[Loss Function] Expected variance {}".format (variance/number_of_modes))   
        return variance/number_of_modes
    
    
    def execute_experiment_variance(self, state: Optional[str] = None, circuit: Optional[AbstractCircuit] = None) -> float:
        """
        Executes an experiment to calculate variance using the specified state and circuit.

        Parameters:
        state (Optional[str]): The initial state for the experiment. Defaults to a uniform state.
        circuit (Optional[AbstractCircuit]): The circuit for the experiment. Defaults to a Fourier transform circuit.

        Returns:
        float: The calculated expected variance from the experiment.
        """
        if state == None:
            state = generate_state_from_list ([1 for i in range (self.number_of_modes)])

        if circuit == None:
            circuit = generate_fourier_transform_circuit (self.number_of_modes)

        results = self.device.execute_experiment (state, circuit)    
        return self.calculate_expected_variance (results, self.number_of_modes)
    
    def execute_experiment_variance_distinguishable_scenario(self, number_of_modes: int) -> float:
        """
        Executes experiments for a distinguishable scenario across multiple modes and calculates the expected variance.

        Parameters:
        number_of_modes (int): The number of modes.

        Returns:
        float: The calculated expected variance for a distinguishable scenario.
        """
        results_agrregated = StatesAndProbabilities ()

        for i in range (number_of_modes):
            l = [1 if j == i else 0 for j in range (number_of_modes)]
            results_distinguishable = self.device.execute_experiment (generate_state_from_list (l), generate_fourier_transform_circuit (self.number_of_modes))
            results_agrregated.aggregate (results_distinguishable)

        return self.calculate_expected_variance (results_agrregated, number_of_modes)

    def execute_experiment_variance_indistinguishable_scenario(self, number_of_modes: int) -> float:
        """
        Executes experiments for an indistinguishable scenario across multiple modes and calculates the expected variance.

        Parameters:
        number_of_modes (int): The number of modes.

        Returns:
        float: The calculated expected variance for an indistinguishable scenario.
        """
        results =  self.device.execute_experiment (generate_state_from_list ([1 for i in range (number_of_modes)]), generate_fourier_transform_circuit (number_of_modes), number_of_modes)
        return self.calculate_expected_variance (results, number_of_modes)
    