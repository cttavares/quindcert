import perceval as pcvl
from perceval.algorithm.analyzer import Analyzer
import numpy as np
import logging

# An extension of the analyzer by quandela, 
# because it doesn't do what I need it to do.
class EnhancedAnalyzer(Analyzer):
	
    # Reimplementation of the method compute
    def compute(self, normalize=False, expected=None, progress_callback=None):
        logging.debug ("[Enhanced analyzer -> compute ()] Calculating distributions for input states using permanents")
        probs_res = {}
        logical_perf = []
        if expected is not None:
            normalize = True
            self.error_rate = 0

        # Compute probabilities for all input states
        for idx, i_state in enumerate(self.input_states_list):
            logging.debug ("[Enhanced analyzer -> compute ()] For input state: {}".format (i_state))
            self._processor.with_input(i_state)
            job = self._sampler.probs
            job.name = f'{self.default_job_name} {idx+1}/{len(self.input_states_list)}'
            probs_output = job.execute_sync()
            probs = probs_output['results']
            logging.debug ("[Enhanced analyzer -> compute ()] ,the output distribution is {}".format (probs))
            probs_res[i_state] = probs
            if 'logical_perf' in probs_output:
                logical_perf.append(probs_output['logical_perf'])
            else:
                logical_perf.append(1)
            if progress_callback is not None:
                progress_callback((idx+1)/len(self.input_states_list))

        # Create a distribution matrix and compute performance / error rate if needed
        probs_ = list(probs_res.values ())[0]
        self._distribution = np.zeros((len(self.input_states_list), len(probs_)))
        for iidx, i_state in enumerate(self.input_states_list):
            sum_p = 0
            for oidx, o_state in enumerate(probs_):
                self._distribution[iidx, oidx] = probs_res[i_state][o_state]
                sum_p += probs_res[i_state][o_state]
            
            if expected is not None:
                if i_state in expected:
                    expected_o = expected[i_state]
                elif i_state in self._mapping and self._mapping[i_state] in expected:
                    expected_o = expected[self._mapping[i_state]]
                if not isinstance(expected_o, pcvl.BasicState):
                    for k, v in self._mapping.items():
                        if v == expected_o:
                            expected_o = k
                            break
                if sum_p > 0:
                    self.error_rate += 1 - self._distribution[iidx, self.output_states_list.index(expected_o)]/sum_p
            if normalize and sum_p != 0:
                self._distribution[iidx, :] /= sum_p
                
        self.performance = min(logical_perf)
        output = {'results': self._distribution, 'input_states': self.input_states_list,
                  'output_states': list (probs_.keys()), 'performance': self.performance}
        if expected is not None:
            self.error_rate /= len(self.input_states_list)
            output['error_rate'] = self.error_rate
            self.fidelity = 1 - self.error_rate
            output['fidelity'] = self.fidelity
        
        return output