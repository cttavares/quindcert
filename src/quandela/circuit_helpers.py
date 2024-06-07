import logging
import perceval as pcvl
import perceval.components as comp
import numpy as np
import random
import cmath
import re

from base.circuit_helpers import fourier_matrix
from typing import List, Tuple

def configurable_tensor_product(circuit_1: pcvl.Circuit, circuit_2: pcvl.Circuit, dimensions: List[int] = [2, 2]) -> pcvl.Circuit:
    """
    Create a tensor product of two circuits with configurable dimensions.

    Parameters:
    circuit_1 (pcvl.Circuit): The first circuit.
    circuit_2 (pcvl.Circuit): The second circuit.
    dimensions (List[int]): The dimensions of the circuits.

    Returns:
    pcvl.Circuit: The resulting tensor product circuit.
    """
    
    print ("Dimensions: ", sum (dimensions))
    c = pcvl.Circuit(sum (dimensions))
    index = 0
    print ("Indexes: ", index, ", f:", dimensions [0] - 1)
    c.add ((index, index + dimensions [0]-1), circuit_1)
    index = dimensions [0]
    print ("Indexes: ", index, ", f:", dimensions [0] - 1)
    c.add ((index, index + dimensions [1]-1), circuit_2)
    return c


def circuit_tensor_product (circuit_1: pcvl.Circuit, circuit_2: pcvl.Circuit, dimension: int = 2) -> pcvl.Circuit:
    """
    Create a tensor product of two circuits.

    Parameters:
    circuit_1 (pcvl.Circuit): The first circuit.
    circuit_2 (pcvl.Circuit): The second circuit.
    dimension (int): The dimension of the circuits.

    Returns:
    pcvl.Circuit: The resulting tensor product circuit.
    """
    
    c = pcvl.Circuit (dimension*2)
    c.add((0,1), circuit_1)    
    c.add((2,3), circuit_2)
    return c

def circuit_tensor_product_with_extra (circuit_1: pcvl.Circuit, circuit_2: pcvl.Circuit, dimension: int = 2) -> pcvl.Circuit:
    """
    Create a tensor product of two circuits with an extra identity circuit.

    Parameters:
    circuit_1 (pcvl.Circuit): The first circuit.
    circuit_2 (pcvl.Circuit): The second circuit.
    dimension (int): The dimension of the circuits.

    Returns:
    pcvl.Circuit: The resulting tensor product circuit with an extra identity circuit.
    """
    c = pcvl.Circuit (dimension*3)
    extra = generate_identity (2)
    
    c.add((0,1), circuit_1)    
    c.add((2,3), circuit_2)
    c.add((4,5), extra)
    return c
    
def create_custom_MZ(theta: float, phi: float) -> pcvl.Circuit:
    """
    Create a custom Mach-Zehnder interferometer circuit.

    Parameters:
    theta (float): The phase shift for the first phase shifter.
    phi (float): The phase shift for the second phase shifter.

    Returns:
    pcvl.Circuit: The resulting Mach-Zehnder interferometer circuit.
    """
    return pcvl.Circuit(2) // comp.BS() // (0, comp.PS(theta)) // comp.BS() // (1, comp.PS(phi))

def approximate_with_BSplusPS(some_matrix) -> pcvl.Circuit:
    """
    Approximate a matrix using a beam splitter and phase shifter.

    Parameters:
    some_matrix: The matrix to approximate.

    Returns:
    pcvl.Circuit: The resulting circuit.
    """
    M = pcvl.Matrix(some_matrix)
    print ("Some matrix", M)
    # Create a generalized beam splitter/phase shifter - Mach Zender interferometer
    ub = pcvl.Circuit(2, name="ub") // comp.BS() // (0, comp.PS(phi=pcvl.Parameter("φ_a")))
    dec = pcvl.Circuit.decomposition(M, ub)
    print ("Result: ", dec.describe ())
    return dec
    
def approximate_with_MZ(some_matrix) -> pcvl.Circuit:
    """
    Approximate a matrix using a Mach-Zehnder interferometer.

    Parameters:
    some_matrix (np.ndarray): The matrix to approximate.

    Returns:
    pcvl.Circuit: The resulting circuit.
    """
    M = pcvl.Matrix(some_matrix)
    c1 = comp.Unitary(U=M)
    # Create a generalized beam splitter/phase shifter - Mach Zender interferometer
    ub = pcvl.Circuit(2, name="ub") // comp.BS() // (0, comp.PS(phi=pcvl.Parameter("φ_a"))) // comp.BS() // (1, comp.PS(phi=pcvl.Parameter("φ_b")))
    c2 = pcvl.Circuit.decomposition(M, ub, shape="triangle")
    
    return c2

# First do the necessary permutations
def generate_permutations(n: int) -> pcvl.Circuit:
    """
    Generate a circuit with permutations and beam splitters.

    Parameters:
    n (int): The number of modes.

    Returns:
    pcvl.Circuit: The resulting circuit.
    """
    circuit_perm = pcvl.Circuit(n)

    perm = [j for j in range (0, n)]
    i = 1
    half = n >> 1
    while i <= half:
        temp = perm [i]
        perm [i] = perm [i + half - 1]
        perm [half + i - 1] = temp
        i+=2

    print (perm)
    circuit_perm //= comp.PERM (perm)

    j = 0
    while j <= n-2:
        circuit_perm.add ((j, j+1), comp.BS())
        j = j + 2
    
    
    return circuit_perm

def generate_identity (n_modes: int) -> pcvl.Circuit:
    """
    Generate an identity circuit.

    Parameters:
    n_modes (int): The number of modes.

    Returns:
    pcvl.Circuit: The resulting identity circuit.
    """
    circuit_perm = pcvl.Circuit(n_modes)
    perm = [j for j in range (0, n_modes)]
    circuit_perm //= comp.PERM (perm)    
    return circuit_perm

# First do the necessary permutations
def generate_random_permutation(n: int) -> pcvl.Circuit:
    """
    Generate a random permutation circuit.

    Parameters:
    n (int): The number of modes.

    Returns:
    pcvl.Circuit: The resulting random permutation circuit.
    """
    circuit_perm = pcvl.Circuit(n)

    perm = [j for j in range (0, n)]
    n1 = round (random.random ()*((n-1)))
    n2 = round (random.random ()*((n-1)))

    temp = perm [n1]
    perm [n1] = perm [n2]
    perm [n2] = temp

    print ("Generated permutation {}".format (perm))
    circuit_perm //= comp.PERM (perm)    
    return circuit_perm

def generate_several_random_permutations(number_of_photons: int, number_of_permutations: int) -> List[pcvl.Circuit]:
    """
    Generate several random permutation circuits.

    Parameters:
    number_of_photons (int): The number of modes.
    number_of_permutations (int): The number of permutations to generate.

    Returns:
    List[pcvl.Circuit]: The list of generated random permutation circuits.
    """
    i = 0
    random_permutations = []
    print ("Numebr of modes {}".format (number_of_photons))
    print ("Number of permutations to generate: {}".format (number_of_permutations))
    while i < number_of_permutations:
        circuit = generate_random_permutation (number_of_photons)
        random_permutations.append (circuit)
        i = i + 1
    
    print ("Generated permutations: {}".format (random_permutations))
    return random_permutations

def generate_dagger_circuit (circuit):
    """
    Generate the dagger (inverse) of a given circuit.

    Parameters:
    circuit (pcvl.Circuit): The circuit to invert.

    Returns:
    np.ndarray: The inverted circuit as a matrix.
    """
    return np.linalg.inv (circuit.compute_unitary ())


def generate_bunching_circuit(n: int) -> pcvl.Circuit:
    """
    Generate a bunching circuit for the given number of modes.

    Parameters:
    n (int): The number of modes.

    Returns:
    pcvl.Circuit: The resulting bunching circuit.
    """
    half = n >> 1
    d = half

    total_circuit = pcvl.Circuit(n, name="bunch")

    circuit_m = approximate_with_MZ (fourier_matrix (d))
    #print ("Fourier transform {}".format (circuit_m.describe ()))
    #pcvl.pdisplay(circuit_fm)

    total_circuit //= (circuit_m)
    total_circuit //= generate_permutations (n)
    #pcvl.pdisplay(generate_permutations (n))
    #bunching_circuit = Circuit(n, name="bunch") // circuit_fm

    print ("Total circuit {}".format (total_circuit.describe ()))
    #pcvl.pdisplay(generate_permutations (n))
    return total_circuit

def generate_fourier_transform_circuit(dimension: int) -> pcvl.Circuit:
    """
    Generate a Fourier transform circuit for the given dimension.

    Parameters:
    dimension (int): The dimension of the circuit.

    Returns:
    pcvl.Circuit: The resulting Fourier transform circuit.
    """
    total_circuit = approximate_with_MZ (fourier_matrix (dimension))
    return total_circuit


def cut_unused_parameters(circuit: pcvl.Circuit) -> pcvl.Circuit:
    """
    Remove unused parameters from a circuit.

    Parameters:
    circuit (pcvl.Circuit): The circuit to process.

    Returns:
    pcvl.Circuit: The processed circuit with unused parameters removed.
    """
    
    depths = circuit.depths()
    mode = 0

    last_items = []

    for d in depths:
       print (circuit.getitem ((mode, d-1), False)) 
       last_item = circuit.getitem ((mode, d-1), False)
       if isinstance (last_item, comp.unitary_components.PS) == True:
            print ("Got one object to delete {}".format (last_item))
            last_items.append (last_item)
       mode = mode + 1
    
    print ("Last items: {}".format(last_items))
    
    parameters_to_delete = []
    for to_delete in last_items:    
        for component_tuple in circuit._components:
            if component_tuple[1] == to_delete:
                parameters_to_delete += to_delete.get_parameters (True)
                circuit._components.remove(component_tuple)
    
    #print ("Params to delete: ",  parameters_to_delete)
    #print ("Keys are: ", circuit.params)
    
    for param_to_delete in parameters_to_delete:
        del circuit._params [param_to_delete.name]           

    return circuit

def create_generic_circuit(number_of_modes: int) -> pcvl.Circuit:
    """
    Create a generic interferometer circuit.

    Parameters:
    number_of_modes (int): The number of modes.

    Returns:
    pcvl.Circuit: The resulting generic interferometer circuit.
    """
    c = pcvl.Circuit.generic_interferometer(number_of_modes,
                                        #lambda i: comp.BS() // comp.PS(pcvl.P("φ%d" % i)),
                                        lambda i: (pcvl.BS() // (0, pcvl.PS(pcvl.P("φ%d" % (i*2))))
       // pcvl.BS() // (1, pcvl.PS(pcvl.P("φ%d" % (i*2 + 1))))),
                                        shape="triangle")
    return c

def create_generic_circuit_with_circuit_cutting (number_of_modes: int) -> pcvl.Circuit:
    """
    Create a generic interferometer circuit with unused parameters removed.

    Parameters:
    number_of_modes (int): The number of modes.

    Returns:
    pcvl.Circuit: The resulting generic interferometer circuit with unused parameters removed.
    """
    circ = create_generic_circuit (number_of_modes)
    return cut_unused_parameters (circ)


def generate_random_circuit (number_of_modes: int) -> pcvl.Circuit:
    """
    Generate a random circuit.

    Parameters:
    number_of_modes (int): The number of modes.

    Returns:
    pcvl.Circuit: The resulting random circuit.
    """
    
    unitary = pcvl.Matrix.random_unitary(number_of_modes) #creates a random unitary of dimension number_of_modes
    mzi = (pcvl.BS() // (0, pcvl.PS(phi=pcvl.Parameter("φ_a")))
       // pcvl.BS() // (1, pcvl.PS(phi=pcvl.Parameter("φ_b"))))
    circuit = pcvl.Circuit.decomposition(unitary, mzi,
                                               #phase_shifter_fn=pcvl.PS,
                                               shape="triangle")
    return circuit

def generate_random_circuit_cut_unused_parameters (number_of_modes: int) -> pcvl.Circuit:
    """
    Generate a random circuit with unused parameters removed.

    Parameters:
    number_of_modes (int): The number of modes.

    Returns:
    pcvl.Circuit: The resulting random circuit with unused parameters removed.
    """
    circuit = generate_random_circuit (number_of_modes)
    print ("Random circuit: ", circuit.describe ())
    depths = circuit.depths()
    mode = 0

    last_items = []

    for d in depths:
       print (circuit.getitem ((mode, d-1), False)) 
       last_item = circuit.getitem ((mode, d-1), False)
       if isinstance (last_item, comp.unitary_components.PS) == True:
            print ("Got one object to delete {}".format (last_item))
            last_items.append (last_item)
       mode = mode + 1
    
    print ("Last items: {}".format(last_items))
    
    for to_delete in last_items:    
        for component_tuple in circuit._components:
            if component_tuple[1] == to_delete:
                circuit._components.remove(component_tuple)
        
    return circuit

def extract_parameters_from_random_circuit(circuit: pcvl.Circuit) -> List[float]:
    """
    Extract parameters from a random circuit.

    Parameters:
    circuit (pcvl.Circuit): The circuit to process.

    Returns:
    List[float]: The extracted parameters.
    """
    s = circuit.describe ()
    
    #logging.info ("Circuit to be dealt with:", s)
    pattern = r'phi=([+-]?\d+\.\d+)'
    matches = re.findall (pattern ,s)

    return [float (match) for match in matches]

def generate_parameters_from_random_circuit (number_of_modes: int) -> List[float]:
    """
    Generate parameters from a random circuit.

    Parameters:
    number_of_modes (int): The number of modes.

    Returns:
    List[float]: The generated parameters.
    """
    parameters = []

    while len (parameters)!=9:
        circuit = generate_random_circuit_cut_unused_parameters (number_of_modes)
        print ("The circuit: ", circuit.describe ())
        parameters = extract_parameters_from_random_circuit (circuit)
    
    return parameters 

def randomize_parameters_from_perceval_circuit(circuit: pcvl.Circuit, max_round: int = -1) -> List[float]:
    """
    Randomize parameters from a Perceval circuit.

    Parameters:
    circuit (pcvl.Circuit): The circuit to process.
    max_round (int): The maximum rounding for the parameters.

    Returns:
    List[float]: The randomized parameters.
    """
    
    list_Parameters = circuit.get_parameters(False)
    randomized_parameters = []
    for _, p in enumerate(list_Parameters):
       rnumber = random.random ()*(p.max - p.min) + p.min
       if max_round != -1:
           rnumber = round (rnumber, max_round)
       randomized_parameters.append (rnumber)
    return randomized_parameters


