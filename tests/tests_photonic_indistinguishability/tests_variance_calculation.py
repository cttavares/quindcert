import unittest
from unittest.mock import MagicMock, patch

from base.results import StatesAndProbabilities
from base.state_generation_helpers import generate_state_from_list
from base.circuit_helpers import generate_fourier_transform_circuit
from base.devices import Device
from photonic_indistinguishability_measures.variance import Variance

class TestVariance(unittest.TestCase):

    def setUp(self):
        self.device = MagicMock(spec=Device)
        self.variance_calculator = Variance(device=self.device, number_of_modes=3)

    def test_calculate_minimum_three_modes(self):
        result = Variance.calculate_minimum_three_modes(1.0)
        expected = ((9 / 4) * 1.0 - 2) ** 2
        self.assertAlmostEqual(result, expected)

    def test_calculate_bound_average_n_modes(self):
        result = Variance.calculate_bound_average_n_modes(1.0, 0.5, 3)
        expected = (1 / (3 * (3 - 1))) * ((1.0 - 2 * 0.5 + 1) / (1 - 0.5)) ** 2 - (1 / (3 - 1))
        self.assertAlmostEqual(result, expected)

    def test_calculate_max_expected_variance(self):
        result = Variance.calculate_max_expected_variance(3)
        expected = 2 - 2 / 3
        self.assertAlmostEqual(result, expected)

    def test_calculate_min_expected_variance(self):
        result = Variance.calculate_min_expected_variance(3)
        expected = 1 - 1 / 3
        self.assertAlmostEqual(result, expected)

    def test_calculate_expected_value_of_the_expected_variance(self):
        gram_matrix = [
            [1, 0.5, 0.5],
            [0.5, 1, 0.5],
            [0.5, 0.5, 1]
        ]
        result = Variance.calculate_expected_value_of_the_expected_variance(gram_matrix, 3)
        sum_overlaps_ab = sum([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
        expected = 1 + (1 / (3 * (3 + 1))) * sum_overlaps_ab - (2 / (3 + 1))
        self.assertAlmostEqual(result, expected)

    @patch.object(Variance, 'calculate_expected_variance')
    def test_execute_experiment_variance_distinguishable_scenario(self, mock_calculate_expected_variance):
        mock_calculate_expected_variance.return_value = 0.9

        result = self.variance_calculator.execute_experiment_variance_distinguishable_scenario(3)

        self.assertEqual(self.device.execute_experiment.call_count, 3)
        mock_calculate_expected_variance.assert_called_once()
        self.assertEqual(result, 0.9)

    @patch.object(Variance, 'calculate_expected_variance')
    def test_execute_experiment_variance_indistinguishable_scenario(self, mock_calculate_expected_variance):
        mock_calculate_expected_variance.return_value = 0.8

        result = self.variance_calculator.execute_experiment_variance_indistinguishable_scenario(3)

        self.device.execute_experiment.assert_called_once()
        mock_calculate_expected_variance.assert_called_once()
        self.assertEqual(result, 0.8)

if __name__ == '__main__':
    unittest.main()
