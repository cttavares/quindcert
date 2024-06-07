import unittest
from unittest.mock import MagicMock, patch
from base.state_generation_helpers import generate_states_on_indexes
from quandela.circuit_helpers import generate_identity
from quandela.quandela_tomography import QuandelaProcessTomographyProber


class TestQuandelaProcessTomographyProber(unittest.TestCase):

    def setUp(self):
        self.number_of_modes = 4
        self.device = MagicMock()
        self.prober = QuandelaProcessTomographyProber(self.number_of_modes, self.device)

    def test_generate_dummy_lists(self):
        result = self.prober.generate_dummy_lists(2, self.number_of_modes)
        self.assertEqual(len(result), self.number_of_modes ** 2)

    def test_generate_trivial_results(self):
        result = self.prober.generate_trivial_results(1, self.number_of_modes)
        self.assertEqual(len(result), self.number_of_modes)
        for key, value in result.items():
            self.assertEqual(len(value), self.number_of_modes)

    def test_define_double_photons_experiments(self):
        result = self.prober.define_double_photons_experiments()
        self.assertEqual(len(result), self.number_of_modes * (self.number_of_modes - 1) // 2)

    def test_define_single_photon_experiments(self):
        result = self.prober.define_single_photon_experiments()
        self.assertEqual(len(result), self.number_of_modes)

    @patch('quandela.quandela_tomography.QuandelaProcessTomographyProber.perform_experiments_from_states')
    def test_perform_single_photon_experiments(self, mock_perform_experiments_from_states):
        mock_perform_experiments_from_states.return_value = {'[0]': {'[0]': 1}}
        result = self.prober.perform_single_photon_experiments()
        self.assertEqual(result, {'[0]': {'[]': 1}})

    @patch('quandela.quandela_tomography.QuandelaProcessTomographyProber.perform_experiments_from_states')
    def test_perform_double_photon_experiments(self, mock_perform_experiments_from_states):
        mock_perform_experiments_from_states.return_value = {'[0, 1]': {'[0, 1]': 1}}
        result = self.prober.perform_double_photon_experiments()
        self.assertEqual(result, {'[0, 1]': {'[1]': 1}})

    def test_string_to_indexes(self):
        result = self.prober.string_to_indexes('[1, 0, 0]')
        self.assertEqual(result, '[0]')

    def test_convert_to_plain_text(self):
        states = {'[0]': {'[0]': 1}}
        result = self.prober.convert_to_plain_text(states)
        self.assertEqual(result, {'[0]': {'[]': 1}})

    @patch('quandela.quandela_tomography.QuandelaProcessTomographyProber.perform_single_photon_experiments')
    @patch('quandela.quandela_tomography.QuandelaProcessTomographyProber.perform_double_photon_experiments')
    def test_make_experimental_bunch(self, mock_double, mock_single):
        mock_single.return_value = {'[0]': {'[0]': 1}}
        mock_double.return_value = {'[0, 1]': {'[0, 1]': 1}}
        self.prober.make_experimental_bunch()
        self.maxDiff = None
        self.assertEqual(self.prober.single_photon_results, {'[0]': {'[0]': 1, '[1]': 0, '[2]': 0, '[3]': 0},'[1]': {'[0]': 0, '[1]': 0, '[2]': 0, '[3]': 0}, '[2]': {'[0]': 0, '[1]': 0, '[2]': 0, '[3]': 0}, '[3]': {'[0]': 0, '[1]': 0, '[2]': 0, '[3]': 0}})
        self.assertEqual(self.prober.double_photon_results, {'[0, 0]': {'[0, 0]': 0,'[0, 1]': 0,'[0, 2]': 0,'[0, 3]': 0,'[1, 1]': 0,'[1, 2]': 0,'[1, 3]': 0,'[2, 2]': 0,'[2, 3]': 0,'[3, 3]': 0},'[0, 1]': {'[0, 0]': 0,'[0, 1]': 1,'[0, 2]': 0,'[0, 3]': 0,'[1, 1]': 0,'[1, 2]': 0,'[1, 3]': 0,'[2, 2]': 0,'[2, 3]': 0,'[3, 3]': 0},'[0, 2]': {'[0, 0]': 0,'[0, 1]': 0,'[0, 2]': 0,'[0, 3]': 0,'[1, 1]': 0,'[1, 2]': 0,'[1, 3]': 0,'[2, 2]': 0,'[2, 3]': 0,'[3, 3]': 0},'[0, 3]': {'[0, 0]': 0,'[0, 1]': 0,'[0, 2]': 0,'[0, 3]': 0,'[1, 1]': 0,'[1, 2]': 0,'[1, 3]': 0,'[2, 2]': 0,'[2, 3]': 0,'[3, 3]': 0},'[1, 1]': {'[0, 0]': 0,'[0, 1]': 0,'[0, 2]': 0,'[0, 3]': 0,'[1, 1]': 0,'[1, 2]': 0,'[1, 3]': 0,'[2, 2]': 0,'[2, 3]': 0,'[3, 3]': 0},'[1, 2]': {'[0, 0]': 0,'[0, 1]': 0,'[0, 2]': 0,'[0, 3]': 0,'[1, 1]': 0,'[1, 2]': 0,'[1, 3]': 0,'[2, 2]': 0,'[2, 3]': 0,'[3, 3]': 0},'[1, 3]': {'[0, 0]': 0,'[0, 1]': 0,'[0, 2]': 0,'[0, 3]': 0,'[1, 1]': 0,'[1, 2]': 0,'[1, 3]': 0,'[2, 2]': 0,'[2, 3]': 0,'[3, 3]': 0},'[2, 2]': {'[0, 0]': 0,'[0, 1]': 0,'[0, 2]': 0,'[0, 3]': 0,'[1, 1]': 0,'[1, 2]': 0,'[1, 3]': 0,'[2, 2]': 0,'[2, 3]': 0,'[3, 3]': 0},'[2, 3]': {'[0, 0]': 0,'[0, 1]': 0,'[0, 2]': 0,'[0, 3]': 0,'[1, 1]': 0,'[1, 2]': 0,'[1, 3]': 0,'[2, 2]': 0,'[2, 3]': 0,'[3, 3]': 0},'[3, 3]': {'[0, 0]': 0,'[0, 1]': 0,'[0, 2]': 0,'[0, 3]': 0,'[1, 1]': 0,'[1, 2]': 0,'[1, 3]': 0,'[2, 2]': 0,'[2, 3]': 0,'[3, 3]': 0}})

if __name__ == '__main__':
    unittest.main()
