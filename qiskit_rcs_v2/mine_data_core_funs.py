"""`gen_haar_random_circuit`, `gen_circuits`, `export_metadata` fucntions."""


import json
from typing import Tuple, List, Dict, Optional
from copy import deepcopy

from qiskit import QuantumCircuit, transpile, qpy
from qiskit.quantum_info import random_unitary


def gen_haar_random_circuit(num_qubits: int, num_layers: int) -> QuantumCircuit:
    """Returns a Haar-random quantum circuit with `num_qubits` qubits and `num_layers` layers.
    Each layer consists of a single-qubit gates ("local") sublayer,
    followed by an entangling ("nonlocal") sublayer.
    The local layer is a column of Haar-random unitaries.
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


def gen_circuits(
    num_circuits: int,
    num_qubits: int,
    num_cycles: int,
    backend
) -> Tuple[List[QuantumCircuit], List[QuantumCircuit]]:
    """TODO COMPLETE."""

    circuits = []
    transpiled_circuits = []

    for _ in range(num_circuits):

        qc_no_meas = gen_haar_random_circuit(num_qubits, num_cycles)
        circuits.append(qc_no_meas)

        qc = deepcopy(qc_no_meas)
        qc.measure_all()
        tpqc = transpile(
            qc,
            backend=backend,
            optimization_level=3
        )
        transpiled_circuits.append(tpqc)

    return circuits, transpiled_circuits


def export_metadata(
    circuits: List[QuantumCircuit],
    transpiled_circuits: List[QuantumCircuit],
    path: str,
    num_qubits: int,
    num_cycles: int,
    backend,
    f_xeb_data: Optional[Dict[str, float]] = None
) -> None:
    """TODO COMPLETE."""

    with open(f"{path}/circuits.qpy", "wb") as f:
        qpy.dump(circuits, f)

    with open(f"{path}/transpiled_circuits.qpy", "wb") as f:
        qpy.dump(transpiled_circuits, f)

    with open(f"{path}/metadata.json", "w") as f:
        circuits_metadata = {
            "num_circuits": len(circuits),
            "num_qubits": num_qubits,
            "num_cycles": num_cycles,
            "circuit_depth": circuits[0].depth(),
            "transpiled_circuit_depth": transpiled_circuits[0].depth(),
            "backend": backend.name,
            "f_xeb_data": f_xeb_data
        }

        json.dump(circuits_metadata, f, indent=4)