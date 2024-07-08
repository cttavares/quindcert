import unittest
from unittest.mock import MagicMock, patch
from base.results import StatesAndProbabilities
from base.circuit_helpers import generate_fourier_transform_circuit
from base.state_generation_helpers import generate_state_from_list
from base.devices import Device, DeviceMode
from photonic_indistinguishability_measures.bunching import BunchingCalculator
from quandela.quandela_devices import QuandelaDeviceFactory, QuandelaLocalDevices

class TestBunchingCalculator(unittest.TestCase):

    def setUp(self):
        self.device = MagicMock(spec=Device)
        self.calculator = BunchingCalculator(device=self.device, number_of_modes=2)

      
    def test_calculate_bunching_probability(self):
        probability_results = {
            '|2,0>': 0.5,
            '|1,1>': 0.3,
            '|0,2>': 0.2
        }
        s = StatesAndProbabilities ()
        s.set_probability_states (probability_results)
        result = self.calculator.calculate_bunching_probability(s, 2)
        self.assertEqual(result, 0.7)  # Only '|2,0>' and '|0,2>' should be considered

    def test_calculate_full_bunching_probability(self):
        probability_results = {
            '|2,0>': 0.5,
            '|1,1>': 0.3,
            '|0,2>': 0.2
        }
        s = StatesAndProbabilities ()
        s.set_probability_states (probability_results)
        result = self.calculator.calculate_full_bunching_probability(s)
        self.assertEqual(result, 0.7)

    @patch.object(BunchingCalculator, 'make_bunching_experiment')
    @patch.object(BunchingCalculator, 'calculate_full_bunching_probability')
    def test_do_the_experiments_for_full_bunching_indistinguishable_case(self, mock_calculate_full_bunching_probability, mock_make_bunching_experiment):
        mock_make_bunching_experiment.return_value = StatesAndProbabilities()
        mock_calculate_full_bunching_probability.return_value = 0.8

        result = self.calculator.do_the_experiments_for_full_bunching_indistinguishable_case()

        mock_make_bunching_experiment.assert_called_once()
        mock_calculate_full_bunching_probability.assert_called_once_with(mock_make_bunching_experiment.return_value)
        self.assertEqual(result, 0.8)

    @patch.object(BunchingCalculator, 'make_bunching_experiment')
    @patch.object(BunchingCalculator, 'calculate_bunching_probability')
    def test_do_the_experiments_for_full_bunching_distinguishable_case(self, mock_calculate_bunching_probability, mock_make_bunching_experiment):
        self.calculator.number_of_modes = 3
        mock_make_bunching_experiment.return_value = StatesAndProbabilities()
        mock_calculate_bunching_probability.return_value = 0.9

        result = self.calculator.do_the_experiments_for_full_bunching_distinguishable_case()

        self.assertEqual(mock_make_bunching_experiment.call_count, 3)
        mock_calculate_bunching_probability.assert_called_once()
        self.assertEqual(result, 0.9)
    
    def test_calculate_full_bunching_distinguishable_case (self):
        probability_results = {
            '|1,0,0>': 1/3,
            '|0,1,0>': 1/3,
            '|0,0,1>': 1/3
        }
        
        states_and_probabilities = StatesAndProbabilities ()
        states_and_probabilities.set_probability_states (probability_results)

        states_and_probabilities.aggregate (probability_results)
        states_and_probabilities.aggregate (probability_results)

        result = self.calculator.calculate_full_bunching_probability (states_and_probabilities, 3)
        self.assertEqual(result, 1/9)
    
    def test_fb_indistinguishable_vs_distinguishable (self):
        number_of_modes = 3

        print (str (QuandelaLocalDevices.NAIVE.value))
        device = QuandelaDeviceFactory().create_local_device (str (QuandelaLocalDevices.NAIVE.value), DeviceMode.SAMPLER)

        bc = BunchingCalculator (device, number_of_modes)

        P_fb_i = bc.do_the_experiments_for_full_bunching_indistinguishable_case ()
        
        P_fb_d = bc.do_the_experiments_for_full_bunching_distinguishable_case ()
        self.assertLessEqual (abs (P_fb_i/P_fb_d-6), 0.2)


if __name__ == '__main__':
    unittest.main()
