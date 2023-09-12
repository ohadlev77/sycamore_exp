"""`compute_expected_fidelity` function."""


import json
from typing import Dict

import pandas as pd
from qiskit import QuantumCircuit
from qiskit.converters.circuit_to_dag import circuit_to_dag


def compute_expected_fidelity(
    qc: QuantumCircuit,
    backend_props_json_file_path: str
) -> Dict[str, float]:
    """Calculates a total expected fidelity for a given quantum circuit `qc`, according
    to characterization properties `backend_props_json_file_path` - by multiplying all
    gate-fidelties of the gates in `qc` with measurement-fidelities of the qubits in `qc.
    
    Returns:
        (Dict[str, float]): the calculated expected fidelity before taking
        readout errors into account, and after."""

    
    with open(backend_props_json_file_path, "r") as json_file:
        backend_props = json.load(json_file)
    gates_df = pd.DataFrame(backend_props["gates"])
    
    noisy_instructions = ["sx", "x", "cx"]
        
    fidelity = 1
    for instruction in qc.data:
        inst_name = instruction.operation.name
        
        if inst_name in noisy_instructions:
            inst_qubits = [qubit.index for qubit in instruction.qubits]
            
            qubits_cond = gates_df["qubits"].apply(lambda x: x == inst_qubits)
            gate_row = gates_df.loc[(gates_df["gate"] == inst_name) & qubits_cond]
            
            gate_row_index = gate_row.index[0]
            gate_fidelity = 1 - gate_row["parameters"][gate_row_index][0]["value"]
            
            fidelity *= gate_fidelity
    fidelity_before_readout = fidelity

    dag_qc = circuit_to_dag(qc)
    active_qubits = [qubit.index for qubit in qc.qubits if qubit not in dag_qc.idle_wires()]

    for qubit_index in active_qubits:
        qubit_readout_error = backend_props["qubits"][qubit_index][4]
        
        assert qubit_readout_error["name"] == "readout_error", \
        "Expected `readout_error` value, got something else."
        
        fidelity *= 1 - qubit_readout_error["value"]
        
    return {"expected_fidelity_before_readout": fidelity_before_readout, "expected_fidelity": fidelity}