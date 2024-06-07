import unittest
from unittest.mock import MagicMock, patch
import numpy as np

from tomography.process_tomography_methods import ProcessTomographyMethod
from tomography.process_tomography_quandela import DeviceCharacterizer
from tomography.tomography_probers import DeviceProcessTomographyProber


class TestDeviceCharacterizer(unittest.TestCase):

    def setUp(self):
        self.number_of_modes = 3
        self.tomography_device = MagicMock(spec=DeviceProcessTomographyProber)
        self.process_tomography_method = MagicMock(spec=ProcessTomographyMethod)
        self.characterizer = DeviceCharacterizer(self.number_of_modes, self.tomography_device, self.process_tomography_method)

    def test_reconstruct_state(self):
        single_photon_results = MagicMock()
        double_photon_results = MagicMock()

        self.tomography_device.get_single_photon_experiments.return_value = single_photon_results
        self.tomography_device.get_double_photon_experiments.return_value = double_photon_results

        self.characterizer.reconstruct_state()

        self.process_tomography_method.set_single_photon_experiments_results.assert_called_once_with(single_photon_results)
        self.process_tomography_method.set_double_photon_experiments_results.assert_called_once_with(double_photon_results)
        self.process_tomography_method.recover_state.assert_called_once()
        
    def test_calculate_distance_between_matrices(self):
        matrix_1 = np.random.rand(3, 3)
        matrix_2 = np.random.rand(3, 3)
        distance = self.characterizer.calculate_distance_between_matrices(matrix_1, matrix_2)
        self.assertIsInstance(distance, float)

    

if __name__ == '__main__':
    unittest.main()
