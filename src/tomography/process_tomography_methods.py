
# Some licensing message
#
# This piece of code aims at generating a bunch of randomized circuits, and evaluate their bunching probability.
#
from typing import Optional, Any
from abc import ABC, abstractmethod


from fractions import Fraction
from functools import reduce
import logging
import numpy as np

class ProcessTomographyMethod:
    def __init__ (self, number_of_modes:int, single_photon_experiments_results: Optional[Any] = None, double_photon_experiment_results: Optional[Any] = None):
        """
        Initialize the ProcessTomographyMethod with the number of modes and optionally with experiment results.

        Parameters:
        number_of_modes (int): The number of modes for the tomography.
        single_photon_experiments_results (Optional[Any]): Results from single photon experiments.
        double_photon_experiment_results (Optional[Any]): Results from double photon experiments.
        """
        self.number_of_modes = number_of_modes
        self.single_photon_experiments_results = single_photon_experiments_results
        self.double_photon_experiment_results = double_photon_experiment_results

    def set_single_photon_experiments_results (self, single_photon_experiments_results):
        """
        Set the results of single photon experiments.

        Parameters:
        single_photon_experiments_results: The results of the single photon experiments.
        """
        self.single_photon_experiments_results = single_photon_experiments_results

    def set_double_photon_experiments_results (self, double_photon_experiment_results):
        """
        Set the results of double photon experiments.

        Parameters:
        double_photon_experiment_results (Any): The results of the double photon experiments.
        """
        self.double_photon_experiment_results = double_photon_experiment_results

    @abstractmethod
    def recover_state (self) -> Any:
        """
        Recover the state based on the experiment results. This method should be implemented by subclasses.

        Returns:
        Any: The recovered state.
        """
        pass

#  We implemented the super stable process tomography method, as available in: https://arxiv.org/pdf/1208.2868
class SuperStableMethod (ProcessTomographyMethod):
    
    def __init__ (self, number_of_modes, single_photon_experiments_results = None, double_photon_experiment_results = None):
        super().__init__ (number_of_modes, single_photon_experiments_results, double_photon_experiment_results)
        
        self.taus = []
        self.visibilities = {}
        self.phases = []
        self.signs = []
        
    def calculate_x_ghjk (self, k, j, h, g):
        return (self.taus [k][j] * self.taus [h][g])/(self.taus [h][j]*self.taus [k][g]) 

    def calculate_y_ghjk (self, k, j, h, g):
        x_ghjk = self.calculate_x_ghjk (k, j, h, g)
        return x_ghjk + (1 / x_ghjk)

    def calculate_tilde_x (self, k, j, h, g):
        return self.calculate_x_ghjk (k, j, h, g) * (self.taus [h][j] * self.taus [k][g])/(self.taus [k][j])
    
    # Creates a n x m matrix
    def calculate_tau_matrix (self):
        matrix = np.zeros ((self.number_of_modes, self.number_of_modes), dtype = complex)
    
        # Here we assume the results are a dictionary with probabilies indexed by the actual mode
        for input_index_s in self.single_photon_experiments_results.keys ():
            sum = reduce (lambda x, y: x + y, 
                          map (lambda z: self.single_photon_experiments_results [input_index_s][z], 
                               self.single_photon_experiments_results [input_index_s].keys ()))
            
            for output_index_s in self.single_photon_experiments_results [input_index_s].keys ():
                input_index = int (input_index_s [1])
                output_index = int (output_index_s [1])
                matrix [input_index][output_index] = self.single_photon_experiments_results [input_index_s][output_index_s]/sum
                matrix [input_index][output_index] = np.sqrt (matrix [input_index][output_index])
        
        self.taus = matrix
        logging.debug ("[Process Tomography methods] Tau matrix {}".format (self.taus))

    # Function that calculates the C's from single states. k, h are input states, 
    # while j,g are output states
    def calculate_C_ghjk (self, k, j, h, g):
        j_s = str ([j])
        k_s = str ([k])
        h_s = str ([h])
        g_s = str ([g])
        
        logging.debug ("Current case: [" + k_s + "," + h_s + ";" + j_s + "," + g_s + "]")
        

        sum_k = reduce (lambda x, y: x + y, 
                          map (lambda z: self.single_photon_experiments_results [k_s][z], 
                               self.single_photon_experiments_results [k_s].keys ()))
    
        sum_h = reduce (lambda x, y: x + y, 
                          map (lambda z: self.single_photon_experiments_results [h_s][z], 
                               self.single_photon_experiments_results [h_s].keys ()))


        R_jk = self.single_photon_experiments_results [k_s][j_s] / sum_k
        R_gh = self.single_photon_experiments_results [h_s][g_s] / sum_h
        R_gk = self.single_photon_experiments_results [k_s][g_s] / sum_k
        R_jh = self.single_photon_experiments_results [h_s][j_s] / sum_h

        logging.debug ("Rs: " + str (R_jk) + "(r_jk);" + str (R_gh) + "(r_gh);" + str (R_gk) + "(r_gk);" + str (R_jh) + "(r_jh);" )
        logging.debug ("Total: " + str (R_jk * R_gh + R_gk * R_jh))
        return R_jk * R_gh + R_gk * R_jh

    def calculate_Q_ghjk (self, k, j, h, g):
        input_key = str (list (sorted ([k, h])))
        output_key = str (list (sorted ([j, g])))
        
        #logging.debug ("Input key: {}".format (input_key))
        #logging.debug ("Output key: {}".format (output_key))
        
        sum = reduce (lambda x, y: x + y, 
                          map (lambda z: self.double_photon_experiment_results [input_key][z], 
                               self.double_photon_experiment_results [input_key].keys ()))

        Q_ghjk = self.double_photon_experiment_results [input_key][output_key]
        #logging.debug ("Q: {}".format (Q_ghjk))
        Q_ghjk = Q_ghjk / sum
        #logging.debug ("Q  prob: {}".format (Q_ghjk))
        return Q_ghjk
    
    
    def calculate_visibilities (self):
        visibilities = {}
        # Now we will have to visit all the relevant modes 
        k = 0
        while k < self.number_of_modes:
            h = k + 1  
            while h  < self.number_of_modes:       
                j = 0
                while j < self.number_of_modes:
                    g = 0
                    while g < self.number_of_modes:             
                        #logging.debug ("------------")
                        C_ghjk = self.calculate_C_ghjk (k, j, h, g)
                        Q_ghjk = self.calculate_Q_ghjk (k, j, h, g)
                        V_ghjk =  (C_ghjk - Q_ghjk)/C_ghjk
                        key = "[" + str (k) + "," + str (h) + ";" + str (j) + "," + str (g) + "]"
                        visibilities [key] = V_ghjk
                        #logging.debug ("------------")
                        g = g + 1 
                    j = j + 1 
                h = h + 1
            k = k + 1 
    
        self.visibilities = visibilities
        #logging.debug ("Visibilities: {}".format (self.visibilities))
    
    def calculate_cos_for_ghjk (self, g, h, j, k):
        inputs = list (sorted ([k, h]))
        outputs = list (sorted ([j, g]))
        key = "[" + str (inputs [0]) + "," + str (inputs [1]) + ";" + str (outputs [0]) + "," + str (outputs [1]) + "]"
        logging.debug ("Key in calculate phase enhanced:" + str (key))
        logging.debug (";Visibilities: "+ str (self.visibilities [key]))
        return -1/2 * self.visibilities[key] * self.calculate_y_ghjk (k, j, h, g)
    
    def calculate_signals (self, cos_dif, alpha, beta):
        sin_alpha = (cos_dif - np.cos (alpha)*np.cos(beta)) / np.sin (beta)  
        if sin_alpha < 0:
            return -1
        else: 
            return 1
    
    def yet_another_phase_signal_calculation (self, reference_phase):
        self.phase_signals = np.ones ((self.number_of_modes, self.number_of_modes), dtype=int)
        phase_cos = np.zeros ((self.number_of_modes, self.number_of_modes), dtype=float)
        
        logging.debug ("Calculating phases for the second line")
        for x in range (2, self.number_of_modes):
            phase_cos [1][x] = self.calculate_cos_for_ghjk (0, 1, 1, x)
            self.phases [1][x] *= self.calculate_signals (phase_cos [1][x], self.phases [1][x], reference_phase)
            
        logging.debug ("Now for second column")
        for y in range (2, self.number_of_modes):
            phase_cos [y][1] = self.calculate_cos_for_ghjk (1, 0, y, 1)
            self.phases [y][1] *=  self.calculate_signals (phase_cos [y][1], self.phases [y][1], reference_phase)
                        
        logging.debug("Now for every other experiment")
        for y in range (2, self.number_of_modes):
            for x in range (2, self.number_of_modes):
                phase_cos [y][x] = self.calculate_cos_for_ghjk (0, 1, y, x)
                self.phases [y][x] *=  self.calculate_signals (phase_cos [y][x], self.phases [y][x], self.phases [y][1])
                
        logging.debug ("Phase cos: ")
        self.pretty_print_phases_arg (phase_cos) 

        logging.debug ("Final phases")
        self.pretty_print_phases_arg (self.phases)
      
    def calculate_phases (self):
        self.phases = np.zeros ((self.number_of_modes, self.number_of_modes), dtype=float)

        y = 1
        while y < self.number_of_modes:
            x = 1 
            while x < self.number_of_modes:
                #logging.debug ("Visiting on phase calculation: " + str (y) +";"+ str (x))
                key = "[" + str (0) + "," + str (y) + ";" + str (0) + "," + str (x) + "]"
                #logging.debug ("Key in calculate phase:" + str (key) + ";Visibilities: "+ str (self.visibilities [key]))
                self.phases [y][x] = np.arccos (-1/2 * self.visibilities[key] * self.calculate_y_ghjk (0, 0, y, x))
                x = x + 1
            y = y + 1
        
    def pretty_print_phases (self):
        pretty = map (lambda x:  map (lambda z: str (Fraction (z/np.pi).limit_denominator (10)), x), self.phases)
        
        logging.debug ("Not pretty phases:")
        logging.debug (self.phases)

        logging.debug ("Pretty phases: ")
        for l in pretty:
           logging.debug (str (list (l)))

    def pretty_print_phases_arg (self, some_phases):
        pretty = map (lambda x:  map (lambda z: str (Fraction (z/np.pi).limit_denominator (10)), x), some_phases)
        
        logging.debug ("Not pretty phases:")
        logging.debug (some_phases)

        logging.debug ("Pretty phases: ")
        for l in pretty:
           logging.debug (str (list (l)))
            
    def recover_state (self):
        self.calculate_tau_matrix ()
        self.calculate_visibilities ()
       
        
        logging.debug ("----------")
        self.calculate_phases ()
        self.pretty_print_phases ()

       
        self.yet_another_phase_signal_calculation (self.phases [1][1])
        
        state_matrix = self.taus.copy ()
        y = 1
        while y < self.number_of_modes:
            x = 1 
            while x < self.number_of_modes:
                state_matrix [y][x] = self.calculate_tilde_x (0, 0, y, x) * np.exp (self.phases [y][x] * 1j)
                x = x + 1
            y = y + 1

        return state_matrix




    

                
    
