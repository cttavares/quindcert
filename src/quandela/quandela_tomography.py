from typing import Any, Dict, List
from base.abstract_circuit import AbstractCircuit
from base.devices import Device
from base.state_generation_helpers import generate_states_on_indexes
from quandela.circuit_helpers import generate_identity
from tomography.tomography_probers import DeviceProcessTomographyProber

from numpy import sort
import logging

class QuandelaProcessTomographyProber (DeviceProcessTomographyProber):
    """
    A class for performing process tomography using Quandela devices.
    """
    def __init__(self, number_of_modes: int, device: Device):
        """
        Initialize the prober with the number of modes and the device.

        Parameters:
        number_of_modes (int): The number of modes.
        device (Any): The device to use for experiments.
        """
        self.number_of_modes = number_of_modes
        self.device = device
        self.single_photon_results = self.generate_trivial_results (1, self.number_of_modes)
        self.double_photon_results = self.generate_trivial_results (2, self.number_of_modes)
        self.some_circuit = generate_identity (self.number_of_modes)

    def define_circuit(self, circuit: AbstractCircuit) -> None:
        """
        Define the circuit to use for experiments.

        Parameters:
        circuit (AbstractCircuit): The circuit to define.
        """
        self.some_circuit = circuit

    def generate_dummy_lists(self, number_of_photons: int, number_of_modes: int) -> List[List[int]]:
        """
        Generate dummy lists for photons and modes.

        Parameters:
        number_of_photons (int): The number of photons.
        number_of_modes (int): The number of modes.

        Returns:
        List[List[int]]: The generated dummy lists.
        """
        if number_of_photons == 1:
            return [[a] for a in range(0, number_of_modes)]

        i = 1
        result = [[a] for a in range (0, number_of_modes)]

        while i < number_of_photons:
            temp_result = []
            list = [a for a in range(0, number_of_modes)]

            for e1 in result:
                for e2 in list:
                    et = e1.copy ()
                    et.append (e2)
                    temp_result.append (et)

            result = temp_result
            i = i + 1

        return result

    def generate_trivial_results(self, number_of_photons: int, number_of_modes: int) -> Dict[str, Dict[str, int]]:
        """
        Generate trivial results for photons and modes.

        Parameters:
        number_of_photons (int): The number of photons.
        number_of_modes (int): The number of modes.

        Returns:
        Dict[str, Dict[str, int]]: The generated trivial results.
        """
        lists = self.generate_dummy_lists (number_of_photons, number_of_modes)

        dummy_results = {}
        for list1 in lists:
            dummy_results_2 = {}
            for list2 in lists:
                dummy_results_2 [str (list (sort (list2)))] = 0

            dummy_results [str (list (sort (list1)))] = dummy_results_2

        return dummy_results

    def define_double_photons_experiments(self) -> Dict[str, Any]:
        """
        Define double photon experiments.

        Returns:
        Dict[str, Any]: The defined double photon experiments.
        """
        i = 0
        states = {}
        while i < self.number_of_modes:
            j = i + 1
            while j < self.number_of_modes:
                key = str (list (sort ([i, j])))
                states [key] = (generate_states_on_indexes ([i, j], self.number_of_modes))
                j = j + 1
            i = i + 1
        logging.debug ("[Process Tomography prober] Double photon states {}".format (states))
        return states

    def define_single_photon_experiments(self) -> Dict[str, Any]:
        """
        Define single photon experiments.

        Returns:
        Dict[str, Any]: The defined single photon experiments.
        """
        i = 0
        states = {}
        while i < self.number_of_modes:
            states [str ([i])] = generate_states_on_indexes ([i], self.number_of_modes)
            i = i + 1
        logging.debug ("[Process Tomography prober] Single photon states {}".format (states))
        return states

    def perform_experiments_from_states(self, states: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform experiments based on the provided states.

        Parameters:
        states (Dict[str, Any]): The states to experiment on.

        Returns:
        Dict[str, Any]: The results of the experiments.
        """
        experiments_results = {}
        for state_index in states.keys ():
            logging.debug ("[Process Tomography prober] Doing experiment for {}".format (state_index))
            results = self.device.execute_experiment (states [state_index], self.some_circuit)
            logging.debug ("[Process Tomography prober] Results {}".format (results))
            experiments_results [state_index] = results
        return experiments_results

    def string_to_indexes(self, state_def: str) -> str:
        """
        Convert a state definition string to indexes.

        Parameters:
        state_def (str): The state definition string.

        Returns:
        str: The converted indexes as a string.
        """
        mode = 0
        numbers = state_def[1:len (state_def)-1].split (",")

        indexes = []
        for number in numbers:
            if int (number) != 0:
                x = int (number)
                while x > 0:
                    indexes.append (mode)
                    x = x - 1
            mode = mode + 1


        return str (indexes)

    def convert_to_plain_text(self, states: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert states to plain text format.

        Parameters:
        states (Dict[str, Any]): The states to convert.

        Returns:
        Dict[str, Any]: The converted states.
        """
        new_states = {}
        for key in states:
            converted_results = {}
            for output in states [key]:
                converted_results [self.string_to_indexes (str (output))] = states [key][output]
            new_states [key] = converted_results
        return new_states

    def perform_single_photon_experiments(self) -> Dict[str, Any]:
        """
        Perform single photon experiments.

        Returns:
        Dict[str, Any]: The results of the single photon experiments.
        """
        return self.convert_to_plain_text (self.perform_experiments_from_states (self.define_single_photon_experiments ()))

    def perform_double_photon_experiments(self) -> Dict[str, Any]:
        """
        Perform double photon experiments.

        Returns:
        Dict[str, Any]: The results of the double photon experiments.
        """
        return self.convert_to_plain_text (self.perform_experiments_from_states (self.define_double_photons_experiments ()))

    def fill_results(self, results: Dict[str, Any], to_fill: Dict[str, Any]) -> None:
        """
        Fill the results into the provided dictionary.

        Parameters:
        results (Dict[str, Any]): The results to fill.
        to_fill (Dict[str, Any]): The dictionary to fill the results into.
        """
        for key_1 in results.keys ():
            for key_2 in results [key_1].keys ():
                to_fill [key_1][key_2] = results [key_1][key_2]

    def make_experimental_bunch(self) -> None:
        """
        Perform the full set of experiments and fill the results.
        """
        self.fill_results (self.perform_single_photon_experiments (), self.single_photon_results)
        self.fill_results (self.perform_double_photon_experiments (), self.double_photon_results)