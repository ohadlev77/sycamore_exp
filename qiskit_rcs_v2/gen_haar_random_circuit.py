""" `gen_haar_random_circuit function`. """

from qiskit import QuantumCircuit
from qiskit.quantum_info import random_unitary

def gen_haar_random_circuit(num_qubits: int, num_layers: int) -> QuantumCircuit:
    """Generates a random quantum circuit with `num_qubits` qubits and `num_layers` layers.
    Each layer consists of a single-qubit gates ("local") sublayer followed by an entangling ("nonlocal") sublayer.
    The local layer is a column of Haar random unitaries.
    The entangling layer is a column of alternating CNOT gates."""
    
    qc = QuantumCircuit(num_qubits)
    
    for layer_index in range(num_layers):
        
        # Single-qubit sublayer
        for qubit_index in range(num_qubits):
            qc.append(random_unitary(2), qargs=[qubit_index])
        qc.barrier()
        
        # Two-qubit gates
        for qubit_index in range(layer_index % 2, num_qubits - 1, 2):
            qc.cx(qubit_index, qubit_index + 1)
        qc.barrier()
    
    return qc