import unittest
import perceval as pcvl
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Dict, Type

from base.results import StatesAndProbabilities
from base.devices import DeviceMode
from quandela.circuit_helpers import generate_fourier_transform_circuit, generate_identity
from quandela.quandela_devices import QuandelaDeviceFactory


class TestQuandelaDevice(unittest.TestCase):

    def setUp(self):
        factory = QuandelaDeviceFactory ()
        self.device = factory.create_local_device ("Naive", DeviceMode.SAMPLER)

    def test_constructor (self):
        self.assertEqual (self.device.mode, DeviceMode.SAMPLER)
        self.assertEqual (self.device.number_of_samples, 1000)
    
    def test_fill_results(self):
        job_results = {"|1,1>": 2, "|0,2>": 3}
        results = self.device.fill_results(job_results)
        self.assertAlmostEqual(results.states_and_probabilities["|1,1>"], 0.4)
        self.assertAlmostEqual(results.states_and_probabilities["|0,2>"], 0.6)

    def test_execute_experiment_sampler(self):
        initial_state = "|1,1>"
        circuit = generate_identity (2)
        results = self.device.execute_experiment(initial_state, circuit)
        self.assertIsInstance(results, StatesAndProbabilities)

    def test_execute_experiment_analyzer(self):
        factory = QuandelaDeviceFactory ()
        self.device = factory.create_local_device ("Naive", DeviceMode.ANALYZER)
        initial_state = "|1,1,1>"
        circuit = generate_fourier_transform_circuit (3)
        results = self.device.execute_experiment(initial_state, circuit)
        self.assertIsInstance(results, StatesAndProbabilities)
    

if __name__ == '__main__':
    unittest.main()