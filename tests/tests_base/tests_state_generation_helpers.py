import unittest
import numpy as np
from base.state_generation_helpers import (
    create_dummy_state,
    polarize_state,
    generate_bunching_initial_state,
    generate_states_on_indexes,
    valid,
    generate_a_state_with_n_photons,
    generate_a_blank_state,
    generate_a_full_ones_partition,
    sum_states,
    generate_state_from_list,
    generate_initial_states,
    generate_partition_h,
    generate_partitions,
    unique_permutations,
    generate_all_orders_for_partitions,
    generate_trivial_orders_for_partitions,
    generate_states_from_orders,
    generate_all_state_combinations,
    generate_state_combinations_no_orders
)

class TestStateGenerationHelpers(unittest.TestCase):

    def test_create_dummy_state(self):
        state = create_dummy_state()
        self.assertEqual(str(state), '|1,0>', "Dummy state creation failed.")

    def test_polarize_state(self):
        state = '|1,1>'
        polarizations = [(45, 45), (90, 90)]
        polarized_state = polarize_state(state, polarizations)
        expected_state = '|{P:(45,45)},{P:(90,90)}>'
        self.assertEqual(polarized_state, expected_state, "State polarization failed.")

    def test_generate_bunching_initial_state(self):
        state = generate_bunching_initial_state(4)
        self.assertEqual(state, '|1,0,1,1>', "Bunching initial state generation failed.")

    def test_generate_states_on_indexes(self):
        state = generate_states_on_indexes([0, 2, 2], 4)
        self.assertEqual(state, '|1,0,2,0>', "States on indexes generation failed.")

    def test_valid(self):
        self.assertTrue(valid([3, 2, 2, 1]), "Valid partition check failed.")
        self.assertFalse(valid([1, 2, 3]), "Invalid partition check failed.")

    def test_generate_a_state_with_n_photons(self):
        state = generate_a_state_with_n_photons(2, 4)
        self.assertEqual(state, '|1,1,0,0>', "State with n photons generation failed.")

    def test_generate_a_blank_state(self):
        state = generate_a_blank_state(4)
        self.assertEqual(state, '|0,0,0,0>', "Blank state generation failed.")

    def test_generate_a_full_ones_partition(self):
        partition = generate_a_full_ones_partition(4)
        self.assertEqual(partition, '1 1 1 1', "Full ones partition generation failed.")

    def test_sum_states(self):
        state1 = '|1,0,1>'
        state2 = '|0,1,1>'
        summed_state = sum_states(state1, state2)
        self.assertEqual(summed_state, '|1,1,2>', "Sum states failed.")

    def test_generate_state_from_list(self):
        state = generate_state_from_list([1, 0, 2])
        self.assertEqual(state, '|1,0,2>', "State generation from list failed.")

    def test_generate_initial_states(self):
        partitions = [[2, 1], [1, 1, 1]]
        states = generate_initial_states(partitions, 3)
        expected = {'1 1 1': {'|1,0,0>': 3}, '2 1': {'|1,0,0>': 1, '|1,1,0>': 1}}
        self.assertEqual(states, expected, "Initial states generation failed.")

    def test_generate_partitions(self):
        partitions = generate_partitions(3)
        expected = [[1, 1, 1], [2, 1], [3]]
        self.assertEqual(partitions, expected, "Partitions generation failed.")

    def test_unique_permutations(self):
        permutations = unique_permutations([1, 1, 2])
        expected = {(1, 1, 2), (1, 2, 1), (2, 1, 1)}
        self.assertEqual(permutations, expected, "Unique permutations generation failed.")

    def test_generate_all_orders_for_partitions(self):
        partitions = [[1, 1, 1], [2, 1]]
        orders = generate_all_orders_for_partitions(partitions)
        expected = {'1 1 1': {(1, 1, 1)}, '2 1': {(2, 1), (1, 2)}}
        self.assertEqual(orders, expected, "All orders for partitions generation failed.")

    def test_generate_trivial_orders_for_partitions(self):
        partitions = [[1, 1, 1], [2, 1]]
        orders = generate_trivial_orders_for_partitions(partitions)
        expected = {'1 1 1': {(1, 1, 1)}, '2 1': {(2, 1)}}
        self.assertEqual(orders, expected, "Trivial orders for partitions generation failed.")

    def test_generate_states_from_orders(self):
        orders = {'1 1 1': {(1, 1, 1)}, '2 1': {(2, 1)}}
        states = generate_states_from_orders(orders, 3)
        expected = {'1 1 1': [[[1, 0, 0], [0, 1, 0], [0, 0, 1]]], '2 1': [[[1, 1, 0], [0, 0, 1]]]}
        self.assertEqual(states, expected, "States from orders generation failed.")

    def test_generate_all_state_combinations(self):
        states = generate_all_state_combinations(3)
        expected = {'1 1 1': [[[1, 0, 0], [0, 1, 0], [0, 0, 1]]], '2 1': [[[1, 0, 0], [0, 1, 1]], [[1, 1, 0], [0, 0, 1]]], '3': [[[1, 1, 1]]]}
        self.assertEqual(states, expected, "All state combinations generation failed.")

    def test_generate_state_combinations_no_orders(self):
        states = generate_state_combinations_no_orders(3)
        expected = {'1 1 1': [[[1, 0, 0], [0, 1, 0], [0, 0, 1]]], '2 1': [[[1, 1, 0], [0, 0, 1]]], '3': [[[1, 1, 1]]]}
        self.assertEqual(states, expected, "State combinations without orders generation failed.")

if __name__ == "__main__":
    unittest.main()
