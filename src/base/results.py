from typing import Any, Dict, Iterable, Optional

from base.state_generation_helpers import sum_states

class StatesAndProbabilities:

    def __init__ (self):
        self.states_and_probabilities: Dict[str, float] = {}
        self.states_and_countings: Dict[str, int] = {}

    def set_probability(self, state: str, probability: float) -> None:
        """
        Set the probability for a given state.
        """
        self.states_and_probabilities [state] = probability
    
    def get_probability(self, state: str) -> Optional[float]:
        """
        Get the probability of a given state.
        """
        return self.states_and_probabilities.get(state)
    
    def set_probability_states(self, probs: Dict [str, float]):
        self.states_and_probabilities = probs.copy ()

    def get_probabilities (self):
        return self.states_and_probabilities

    def get_probability_states(self) -> Iterable[Any]:
        """
        Get the states for which probabilities have been set.

        Returns:
            Iterable[Any]: An iterable of states with assigned probabilities.
        """
        return self.states_and_probabilities.keys()
    
    def set_counting(self, state: str, countings: int) -> None:
        """
        Set the counting for a given state.
        """
        self.states_and_countings[state] = countings

    def get_counting(self, state: str) -> Optional[int]:
        """
        Get the counting of a given state.
        """
        return self.states_and_countings.get(state)
        
    def has_countings(self) -> bool:
        """
        Check if there are any countings set.
        """
        return len(self.states_and_countings) > 0
    
    def has_probabilities(self) -> bool:
        """
        Check if there are any probabilities set.
        """
        return len(self.states_and_probabilities) > 0
    
    def aggregate(self, results_to_aggregate: Dict[str, float], operation: str = "*") -> None:
        """
        Aggregate probabilities with another set of results.
        
        Parameters:
        results_to_aggregate (Dict[str, float]): The results to aggregate.
        operation (str): The operation to perform ('+' or '*').
        """
        if not self.has_probabilities ():
            self.set_probability_states (results_to_aggregate)
            return 
        
        combined_probs = {}
        
        for state_first, prob_first in self.states_and_probabilities.items ():
            for state_second, prob_second in results_to_aggregate.items ():
                
                new_state = sum_states (state_first, state_second)
                
                if operation == '*':
                    new_prob = prob_first * prob_second
                elif operation == '+':
                    new_prob = prob_first + prob_second
                else:
                    raise ValueError("Unsupported operation. Use '+' or '*'.")

                if new_state not in combined_probs:
                    combined_probs [new_state] = new_prob
                else:
                    combined_probs [new_state] += new_prob    
        
        self.states_and_probabilities = combined_probs


