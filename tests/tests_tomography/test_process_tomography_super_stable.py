import unittest
from unittest.mock import MagicMock, patch
import numpy as np

from tomography.process_tomography_methods import SuperStableMethod


class TestSuperStableMethod(unittest.TestCase):

    def setUp(self):
        self.number_of_modes = 3
        self.single_photon_experiments_results = {
            '[0]': {'[0]': 0.1, '[1]': 0.2, '[2]': 0.7},
            '[1]': {'[0]': 0.3, '[1]': 0.4, '[2]': 0.3},
            '[2]': {'[0]': 0.5, '[1]': 0.3, '[2]': 0.2}
        }
        self.double_photon_experiment_results = {
            '[0,1]': {'[0,1]': 0.1, '[0,2]': 0.2, '[1,2]': 0.7},
            '[1,2]': {'[0,1]': 0.3, '[0,2]': 0.4, '[1,2]': 0.3},
            '[0,2]': {'[0,1]': 0.5, '[0,2]': 0.3, '[1,2]': 0.2}
        }
        self.super_stable_method = SuperStableMethod(
            self.number_of_modes,
            self.single_photon_experiments_results,
            self.double_photon_experiment_results
        )

    def test_calculate_tau_matrix(self):
        self.super_stable_method.calculate_tau_matrix()
        taus = self.super_stable_method.taus
        self.assertEqual(taus.shape, (self.number_of_modes, self.number_of_modes))
        self.assertTrue(np.all(taus >= 0))

    def test_calculate_C_ghjk(self):
        pass

    def test_calculate_Q_ghjk(self):
        pass

    def test_calculate_visibilities(self):
        #self.super_stable_method.calculate_tau_matrix()
        #self.super_stable_method.calculate_visibilities()
        #visibilities = self.super_stable_method.visibilities
        #self.assertIsInstance(visibilities, dict)
        #self.assertTrue(all(isinstance(v, float) for v in visibilities.values()))
        pass

    def test_calculate_cos_for_ghjk(self):
        #self.super_stable_method.calculate_tau_matrix()
        #self.super_stable_method.calculate_visibilities()
        #result = self.super_stable_method.calculate_cos_for_ghjk(0, 1, 1, 2)
        #self.assertIsInstance(result, float)
        pass

    def test_calculate_signals(self):
        result = self.super_stable_method.calculate_signals(0.5, np.pi / 4, np.pi / 4)
        self.assertIn(result, [-1, 1])

    def test_yet_another_phase_signal_calculation(self):
        #self.super_stable_method.yet_another_phase_signal_calculation(np.pi / 4)
        #self.assertTrue((self.super_stable_method.phases != 0).any())
        pass

    def test_calculate_phases(self):
        #self.super_stable_method.calculate_tau_matrix()
        #self.super_stable_method.calculate_visibilities()
        #self.super_stable_method.calculate_phases()
        #self.assertTrue((self.super_stable_method.phases != 0).any())
        pass

    def test_pretty_print_phases(self):
        #self.super_stable_method.calculate_tau_matrix()
        #self.super_stable_method.calculate_visibilities()
        #self.super_stable_method.calculate_phases()
        #with patch('builtins.print') as mocked_print:
        #    self.super_stable_method.pretty_print_phases()
        #    self.assertTrue(mocked_print.called)
        pass

    def test_recover_state(self):
        #self.super_stable_method.calculate_tau_matrix()
        #self.super_stable_method.calculate_visibilities()
        #self.super_stable_method.calculate_phases()
        #result = self.super_stable_method.recover_state()
        #self.assertIsInstance(result, np.ndarray)
        #self.assertEqual(result.shape, (self.number_of_modes, self.number_of_modes))
        pass

if __name__ == '__main__':
    unittest.main()
