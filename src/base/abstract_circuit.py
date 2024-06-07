import numpy as np
from typing import Optional, Any

class AbstractCircuit:

    def __init__(self, n: int, m: Optional[Any] = None):
        """
        Initialize the AbstractCircuit with a matrix.
        
        Parameters:
        n (int): The size of the identity matrix if m is not provided.
        m (Optional[Any]): The matrix to initialize the circuit with.
        """
        if m is None:
            self.m = np.eye (n)
        else:
            self.m = np.array(m)
            if not self.is_unitary():
                raise ValueError("The provided matrix is not unitary.")
    
    def is_unitary(self) -> bool:
        """
        Check if the matrix is unitary.
        
        Returns:
        bool: True if the matrix is unitary, False otherwise.
        """
        identity = np.eye(self.m.shape[0])
        return np.allclose(identity, self.m @ self.m.conj().T)


    def compose (self, abstract_circuit: 'AbstractCircuit') -> None:
        """
        Compose the current circuit with another AbstractCircuit by matrix multiplication.
        
        Parameters:
        abstract_circuit (AbstractCircuit): The circuit to compose with.
        """
        if not isinstance(abstract_circuit, AbstractCircuit):
            raise TypeError("Expected an instance of AbstractCircuit.")
        
        self.m = self.m @ abstract_circuit.m
        
        if not self.is_unitary():
            raise ValueError("The resulting matrix after composition is not unitary.")

    def __repr__(self) -> str:
        """
        Return a string representation of the circuit's matrix.
        """
        return f"AbstractCircuit(m=\n{self.m}\n)"