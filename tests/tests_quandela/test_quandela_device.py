import unittest
from unittest.mock import MagicMock, patch
import perceval as pcvl
import numpy as np

from base.abstract_circuit import AbstractCircuit
from base.devices import DeviceMode
from base.results import StatesAndProbabilities

from quandela.quandela_devices import QuandelaDevice

class TestQuandelaDevice(unittest.TestCase):

    def setUp(self):
        self.processor = MagicMock()
        self.mode = DeviceMode.SAMPLER
        self.number_of_samples = 1000
        self.device = QuandelaDevice(self.processor, self.mode, self.number_of_samples)

    def test_set_initial_state(self):
        initial_state = '|1,1>'
        self.device.set_initial_state(initial_state)
        self.processor.with_input.assert_called_once_with(pcvl.BasicState(initial_state))

    def test_set_circuit(self):
        circuit = AbstractCircuit(3, np.eye(3))
        self.device.set_circuit(circuit)
        self.processor.set_circuit.assert_called_once()

    def test_fill_results_sampler_mode(self):
        job_results = {'|0,1>': 500, '|1,0>': 500}
        self.device.mode = DeviceMode.SAMPLER
        results = self.device.fill_results(job_results)
        self.assertIsInstance(results, StatesAndProbabilities)
        self.assertEqual(results.get_probability('|0,1>'), 0.5)
        self.assertEqual(results.get_probability('|1,0>'), 0.5)

    def test_fill_results_analyzer_mode(self):
        job_results = {'output_states': ['|0,1>', '|1,0>'], 'results': [[0.6, 0.4]]}
        self.device.mode = DeviceMode.ANALYZER
        results = self.device.fill_results(job_results)
        self.assertIsInstance(results, StatesAndProbabilities)
        self.assertEqual(results.get_probability('|0,1>'), 0.6)
        self.assertEqual(results.get_probability('|1,0>'), 0.4)

    @patch('perceval.algorithm.Sampler')
    def test_execute_experiment_sampler_mode(self, mock_sampler):
        mock_sampler.return_value.sample_count.return_value = {'results': {'|0,1>': 500, '|1,0>': 500}}
        results = self.device.execute_experiment_()
        self.assertIsInstance(results, StatesAndProbabilities)
    
    @patch('quandela.quandela_devices.QuandelaDevice.set_circuit')
    @patch('quandela.quandela_devices.QuandelaDevice.set_initial_state')
    @patch('quandela.quandela_devices.QuandelaDevice.execute_experiment_')
    def test_execute_experiment(self, mock_execute_experiment_, mock_set_initial_state, mock_set_circuit):
        initial_state = '|1,1>'
        circuit = AbstractCircuit(3, np.eye(3))
        self.device.execute_experiment(initial_state, circuit)
        mock_set_circuit.assert_called_once_with(circuit)
        mock_set_initial_state.assert_called_once_with(initial_state)
        mock_execute_experiment_.assert_called_once()

if __name__ == '__main__':
    unittest.main()
