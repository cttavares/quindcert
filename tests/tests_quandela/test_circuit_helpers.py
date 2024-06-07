import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import perceval as pcvl
import perceval.components as comp

from quandela.circuit_helpers import (
    configurable_tensor_product,
    circuit_tensor_product,
    circuit_tensor_product_with_extra,
    create_custom_MZ,
    approximate_with_BSplusPS,
    approximate_with_MZ,
    generate_permutations,
    generate_identity,
    generate_random_permutation,
    generate_several_random_permutations,
    generate_dagger_circuit,
    generate_bunching_circuit,
    generate_fourier_transform_circuit,
    cut_unused_parameters,
    create_generic_circuit,
    create_generic_circuit_with_circuit_cutting,
    generate_random_circuit,
    generate_random_circuit_cut_unused_parameters,
    extract_parameters_from_random_circuit,
    generate_parameters_from_random_circuit,
    randomize_parameters_from_perceval_circuit
)

class TestCircuitHelpers(unittest.TestCase):

    def setUp(self):
        self.circuit_1 = pcvl.Circuit(2)
        self.circuit_2 = pcvl.Circuit(2)
        self.some_matrix = np.eye(2)

    def test_configurable_tensor_product(self):
        result = configurable_tensor_product(self.circuit_1, self.circuit_2, [2, 2])
        self.assertIsInstance(result, pcvl.Circuit)
        
    def test_circuit_tensor_product(self):
        result = circuit_tensor_product(self.circuit_1, self.circuit_2, 2)
        self.assertIsInstance(result, pcvl.Circuit)
        

    def test_circuit_tensor_product_with_extra(self):
        result = circuit_tensor_product_with_extra(self.circuit_1, self.circuit_2, 2)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_create_custom_MZ(self):
        result = create_custom_MZ(0.5, 0.5)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_approximate_with_BSplusPS(self):
        pass

    def test_approximate_with_MZ(self):
        pass

    def test_generate_permutations(self):
        result = generate_permutations(4)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_generate_identity(self):
        result = generate_identity(4)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_generate_random_permutation(self):
        result = generate_random_permutation(4)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_generate_several_random_permutations(self):
        result = generate_several_random_permutations(4, 3)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(isinstance(c, pcvl.Circuit) for c in result))

    def test_generate_dagger_circuit(self):
        circuit = pcvl.Circuit(2)
        result = generate_dagger_circuit(circuit)
        self.assertIsInstance(result, np.ndarray)

    def test_generate_bunching_circuit(self):
        result = generate_bunching_circuit(4)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_generate_fourier_transform_circuit(self):
        result = generate_fourier_transform_circuit(4)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_cut_unused_parameters(self):
        circuit = create_generic_circuit(4)
        result = cut_unused_parameters(circuit)
        self.assertIsInstance(result, pcvl.Circuit)

    def test_create_generic_circuit(self):
        result = create_generic_circuit(4)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_create_generic_circuit_with_circuit_cutting(self):
        result = create_generic_circuit_with_circuit_cutting(4)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_generate_random_circuit(self):
        result = generate_random_circuit(4)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_generate_random_circuit_cut_unused_parameters(self):
        result = generate_random_circuit_cut_unused_parameters(4)
        self.assertIsInstance(result, pcvl.Circuit)
    
    def test_extract_parameters_from_random_circuit(self):
        circuit = generate_random_circuit(4)
        result = extract_parameters_from_random_circuit(circuit)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(p, float) for p in result))

    def test_generate_parameters_from_random_circuit(self):
        result = generate_parameters_from_random_circuit(4)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 9)
        self.assertTrue(all(isinstance(p, float) for p in result))

    def test_randomize_parameters_from_perceval_circuit(self):
        circuit = generate_random_circuit(4)
        result = randomize_parameters_from_perceval_circuit(circuit, 2)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(p, float) for p in result))

if __name__ == '__main__':
    unittest.main()
