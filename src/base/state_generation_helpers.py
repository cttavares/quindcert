import logging
import perceval as pcvl
import numpy as np
from typing import List, Tuple, Dict

def create_dummy_state() -> pcvl.BasicState:
    """
    Create a dummy quantum state.
    
    Returns:
    pcvl.BasicState: The created dummy state.
    """
    return pcvl.BasicState('|1, 0>')

def polarize_state(state: str, polarizations: List[Tuple[float, float]]) -> str:
    """
    Polarize the given quantum state with the specified polarizations.
    
    Parameters:
    state (str): The quantum state to polarize.
    polarizations (List[Tuple[float, float]]): The list of polarization angles.
    
    Returns:
    str: The polarized state.
    """
    
    print ("Entering polarizations: {}".format (polarizations))

    modes_filling = [int(occ) for occ in state [1:len(state)-1].split (",")]
    pos = 0
    polarization_strings = []
    for mode_f in modes_filling:
        
        if mode_f == 1:
            (pol_angle_1, pol_angle_2) = polarizations [pos]
            pos = pos + 1
            polarization_s = "{P:("
            polarization_s += "{},{}".format(pol_angle_1,pol_angle_2)   
            polarization_s += ")}"
            print ("Polarization: {}".format (polarization_s))
        else:
            polarization_s = "0"

        polarization_strings.append (polarization_s)
        
    print ("Polarization strings {}".format (polarization_strings))
    new_state = "|"
    for pol in polarization_strings:
        new_state += pol
        new_state += ","

    new_state = new_state[0:len(new_state)-1] + ">"
    print ("Resultant state: {}".format (new_state))
    return new_state

def generate_bunching_initial_state(number_of_modes: int) -> str:
    """
    Generate an initial bunching state for a given number of modes.
    
    Parameters:
    number_of_modes (int): The number of modes.
    
    Returns:
    str: The generated initial bunching state.
    """
    state_string = '|'
    state_string +='1'
        
    i = 1
    while i < number_of_modes / 2:
        state_string += ',0'
        i = i + 1
     
     
    while i < number_of_modes:
        state_string += ',1'
        i = i + 1
        
    state_string += '>'
    return state_string

def generate_states_on_indexes(indexes: List[int], number_of_modes: int) -> str:
    """
    Generate states based on given indexes and number of modes.
    
    Parameters:
    indexes (List[int]): The list of indexes.
    number_of_modes (int): The number of modes.
    
    Returns:
    str: The generated state.
    """
    logging.debug ("indexes: {}".format (str (indexes)))
    numbers = np.zeros (number_of_modes, dtype=int)
    for index in indexes:
        numbers [index] = numbers [index] + 1
    
    state = '|'

    for i in range (0, number_of_modes):
        state += str (numbers [i])
        if i < number_of_modes - 1:
            state += ","
    
    state += '>'
    logging.debug ("State: {}".format (state))
    return state
        
def valid(partition: List[int]) -> bool:
    """
    Check if a partition is valid.
    
    Parameters:
    partition (List[int]): The partition to check.
    
    Returns:
    bool: True if the partition is valid, False otherwise.
    """
    i = 0
    while i <= len (partition)-2:
        if partition [i] < partition [i+1]:
            return False
        i+=1
        
    return True
        
    
def generate_a_state_with_n_photons(n: int, modes: int) -> str:
    """
    Generate a state with a given number of photons and modes.
    
    Parameters:
    n (int): The number of photons.
    modes (int): The number of modes.
    
    Returns:
    str: The generated state.
    """
    state = '|'
    i = 0
    
    while i < modes:
        if (i > 0):
            state+= ','
        if n >= 1:
            state+= '1'
            n-=1
        else:
            state+= '0'
        i+=1
    
    state += '>'
    return state

def generate_a_blank_state(modes: int) -> str:
    """
    Generate a blank state with a given number of modes.
    
    Parameters:
    modes (int): The number of modes.
    
    Returns:
    str: The generated blank state.
    """
    state = '|'
    i = 0
    
    while i < modes:
        if (i > 0):
            state+= ','
        state+= '0'
        i+=1
    
    state += '>'
    return state

def generate_a_full_ones_partition(modes: int) -> str:
    """
    Generate a full ones partition for a given number of modes.
    
    Parameters:
    modes (int): The number of modes.
    
    Returns:
    str: The generated full ones partition.
    """
    state = ''
    
    i = 0
    while i < modes:
        if (i > 0):
            state+= ' '
        state+= '1'
        i+=1
    
    return state

def sum_states(state_first: str, state_second: str) -> str:
    """
    Sum two states.
    
    Parameters:
    state_first (str): The first state.
    state_second (str): The second state.
    
    Returns:
    str: The resulting state.
    """
    first_numbers = [int(occ) for occ in state_first[1:len(state_first)-1].split (",")]
    second_numbers = [int (occ) for occ in state_second[1:len(state_second)-1].split (",")]
    
    result_list = [x[0] + x[1] for x in zip(first_numbers, second_numbers)]
    return generate_state_from_list (result_list)

def generate_state_from_list(state_l: List[int]) -> str:
    """
    Generate a state from a list of integers.
    
    Parameters:
    state_l (List[int]): The list of integers representing the state.
    
    Returns:
    str: The generated state.
    """
    state = '|'
    
    i = 0
    for mode_has_photon in state_l:
        if (i > 0):
            state+= ','
        state += "{}".format (mode_has_photon)
        i+=1
    
    state += '>'
    return state

def generate_initial_states(all_possible_partitions: List[List[int]], modes: int) -> Dict[str, Dict[str, int]]:
    """
    Generate initial states for all possible partitions.
    
    Parameters:
    all_possible_partitions (List[List[int]]): The list of all possible partitions.
    modes (int): The number of modes.
    
    Returns:
    Dict[str, Dict[str, int]]: The generated initial states.
    """
    all_states = {}
    for p in all_possible_partitions:
        part_dict = {}
        for a in p:
            state = generate_a_state_with_n_photons (a, modes)
            if state in part_dict:
                part_dict [state]+=1
            else:
                part_dict [state] = 1
            key = ' '.join(map(str, p))
            all_states[key] = part_dict
    return all_states
    
import itertools

def generate_partition_h (prefix, remain, n, partitions):
    """
    Helper function to generate partitions.
    
    Parameters:
    prefix (List[int]): The prefix list.
    remain (List[int]): The remaining list.
    n (int): The length of the remaining list.
    partitions (List[List[int]]): The list of partitions to append to.
    """
    i = 1
    while (i < n):
        next_partition = [remain [0] + remain [1]]
        next_partition += remain [2:]
        if valid (prefix + next_partition): 
            partitions.append (prefix + next_partition)
        remain = next_partition
        
        generate_partition_h (prefix + remain [:1], remain [1:], len (remain [1:]), partitions)
        i+=1

def generate_partitions(n: int) -> List[List[int]]:
    """
    Generate partitions of a given number.
    
    Parameters:
    n (int): The number to partition.
    
    Returns:
    List[List[int]]: The list of partitions.
    """
    base_partition = [1 for i in range (0, n)]
    partitions = [base_partition]
    generate_partition_h ([], base_partition, n, partitions)
    return partitions

def unique_permutations(nums: List[int]) -> set:
    """
    Generate unique permutations of a list of numbers.
    
    Parameters:
    nums (List[int]): The list of numbers.
    
    Returns:
    set: The set of unique permutations.
    """
    nums.sort()  # sort the list to ensure similar numbers are adjacent
    return set(itertools.permutations(nums))

def generate_all_orders_for_partitions (partitions):
    """
    Generate all orders for given partitions.
    
    Parameters:
    partitions (List[List[int]]): The list of partitions.
    
    Returns:
    Dict[str, set]: The dictionary of orders for each partition.
    """
    orders = {}
    for p in partitions:
        key = ' '.join(map(str, p))
        orders [key] = unique_permutations(p)
            
    return orders

def generate_trivial_orders_for_partitions (partitions):
    """
    Generate trivial orders for given partitions.
    
    Parameters:
    partitions (List[List[int]]): The list of partitions.
    
    Returns:
    Dict[str, List[int]]: The dictionary of trivial orders for each partition.
    """
    orders = {}
    for p in partitions:
        key = ' '.join(map(str, p))
        orders [key] = {tuple (p)}
            
    return orders

def generate_states_from_orders(orders: Dict[str, set], modes: int) -> Dict[str, List[List[int]]]:
    """
    Generate states from orders.
    
    Parameters:
    orders (Dict[str, set]): The dictionary of orders.
    modes (int): The number of modes.
    
    Returns:
    Dict[str, List[List[int]]]: The generated states.
    """
    states = {}
    for part in orders:
        logging.debug ("[State generation] Partition {}".format (part))
        set_of_orders = orders [part]
        
        states_for_part = []
        
        for order in set_of_orders:
            logging.debug ("[State generation] Possible order for partition: {}".format (order))
            states_for_order = []
            
            i = 0
            for element in order:
                blank_state = [0 for x in range(modes)]
                number_of_photons = element
                while number_of_photons > 0:
                    blank_state [i] = 1
                    i = i + 1
                    number_of_photons = number_of_photons - 1
                logging.debug ("[State generation] Bosonic state to consider. {}".format (blank_state))
                states_for_order.append (blank_state)
            states_for_part.append (states_for_order)
        states [part] = states_for_part 
        logging.debug ("[State generation] States for partition  {}".format (states_for_part))
    return states
    
def generate_all_state_combinations(number_of_modes: int) -> Dict[str, List[List[int]]]:
    """
    Generate all state combinations for a given number of modes.
    
    Parameters:
    number_of_modes (int): The number of modes.
    
    Returns:
    Dict[str, List[List[int]]]: The generated state combinations.
    """
    return generate_states_from_orders (generate_all_orders_for_partitions (generate_partitions (number_of_modes)), number_of_modes)


def generate_state_combinations_no_orders(number_of_modes: int) -> Dict[str, List[List[int]]]:
    """
    Generate state combinations without considering orders for a given number of modes.
    
    Parameters:
    number_of_modes (int): The number of modes.
    
    Returns:
    Dict[str, List[List[int]]]: The generated state combinations without orders.
    """
    return generate_states_from_orders (generate_trivial_orders_for_partitions (generate_partitions (number_of_modes)), number_of_modes)