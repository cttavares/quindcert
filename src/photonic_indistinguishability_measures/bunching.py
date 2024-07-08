import logging
from typing import Optional

from perceval import *
from base.abstract_circuit import AbstractCircuit
from base.results import StatesAndProbabilities
from base.state_generation_helpers import generate_state_from_list
from base.circuit_helpers import generate_fourier_transform_circuit
from base.devices import Device

class BunchingCalculator:
    
    def __init__(self, device: Device, number_of_modes: int = 2):
        """
        Initialize the BunchingCalculator with a device and number of modes.
        
        Parameters:
        device (Device): The device to use for experiments.
        number_of_modes (int): The number of modes in the experiment.
        """
        self.device = device
        self.number_of_modes = number_of_modes
    

    def make_bunching_experiment(self, state: Optional[str] = None, circuit: Optional[AbstractCircuit] = None) -> StatesAndProbabilities:
        """
        Perform a bunching experiment with the given state and circuit.
        
        Parameters:
        state (Optional[str]): The initial state for the experiment.
        circuit (Optional[AbstractCircuit]): The circuit for the experiment.
        
        Returns:
        StatesAndProbabilities: The results of the experiment.
        """
        if state == None:
            state = generate_state_from_list ([1 for _ in range (self.number_of_modes)])

        if circuit == None:
            circuit = generate_fourier_transform_circuit (self.number_of_modes)
            
        self.results = self.device.execute_experiment (state, circuit)
        return self.results    

    def calculate_bunching_probability(self, probability_results: StatesAndProbabilities, min_number_of_photons: int) -> float:
        """
        Calculate the bunching probability from the experiment results.
        
        Parameters:
        probability_results (StatesAndProbabilities): The results of the experiment.
        min_number_of_photons (int): The minimum number of photons to consider bunching.
        
        Returns:
        float: The calculated bunching probability.
        """
        probability = 0
        for state in probability_results.get_probability_states():
            converted_state = "{}".format(state)
    
            for occ in converted_state[1:len(converted_state)-1].split (","):
                if int(occ) >= min_number_of_photons: 
                    #print ('Bunch event, considering to the calculation')
                    probability += probability_results.get_probability (state) 
                    break
        
        return probability

    def calculate_full_bunching_probability(self, probability_results: StatesAndProbabilities, number_of_modes: Optional [int] = None) -> float:
        """
        Calculate the full bunching probability from the experiment results.
        
        Parameters:
        probability_results (StatesAndProbabilities): The results of the experiment.
        
        Returns:
        float: The calculated full bunching probability.
        """
        if number_of_modes is None:
            return self.calculate_bunching_probability (probability_results, self.number_of_modes)
        else:
            return self.calculate_bunching_probability (probability_results, number_of_modes)
    
    def do_the_experiments_for_full_bunching_indistinguishable_case(self) -> float:
        """
        Perform experiments for the full bunching indistinguishable case.
        
        Returns:
        float: The full bunching probability.
        """
        self.results = self.make_bunching_experiment ()
        return self.calculate_full_bunching_probability (self.results)

    def do_the_experiments_for_full_bunching_distinguishable_case(self) -> float:
        """
        Perform experiments for the full bunching distinguishable case.
        
        Returns:
        float: The bunching probability for distinguishable case.
        """
        results_distinguishable_total = StatesAndProbabilities ()

        #print ("Entering distinguishable case")
        for i in range (self.number_of_modes):
            l = [1 if j == i else 0 for j in range (self.number_of_modes)]
            results_distinguishable = self.make_bunching_experiment (generate_state_from_list (l), generate_fourier_transform_circuit (self.number_of_modes))
            #print ("Input state: ", l, ", Results: ", results_distinguishable.get_probabilities ())
            
            results_distinguishable_total.aggregate (results_distinguishable.get_probabilities ())
        
        #print ("Out of distinguishability case")

        #print ("Combined results: ")
        #for i in results_distinguishable_total.get_probability_states():
            #print ("key: ", i, " ;", results_distinguishable_total.get_probability (i))
        
        return self.calculate_bunching_probability (results_distinguishable_total, self.number_of_modes)
    
    
    