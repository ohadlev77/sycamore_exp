""" Mining data by RCS of 12-qubit circuits, using noisy simulator models ("Fake" machines). """

import json
from typing import List, Tuple, Dict
from copy import deepcopy
from collections import Counter

import pandas as pd
from qiskit import transpile, qpy, QuantumCircuit
from qiskit.providers.fake_provider import FakeGuadalupeV2
from qiskit_aer import StatevectorSimulator

from gen_haar_random_circuit import gen_haar_random_circuit

DATA_PATH = "exp_data_12q_fake_gudalupe_v2"


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
    f_xeb_data: Dict[str, float]
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

def execute_circuit(
    circuit: QuantumCircuit,
    transpiled_circuit: QuantumCircuit,
    shots: int,
    backend,
    num_bits: int,
    hilbert_dim: int
) -> pd.DataFrame:
    """TODO COMPLETE"""

    df = pd.DataFrame(
        {
            "bitstring": [],
            "ideal_prob": [],
            "noisy_prob": []
        }
    )

    ideal_probs = Counter(StatevectorSimulator().run(circuit).result().get_counts())
    noisy_counts = Counter(backend.run(transpiled_circuit, shots=shots).result().get_counts())

    for i in range(hilbert_dim):
        bitstring = format(i, "b").zfill(num_bits)

        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    {
                        "bitstring": [bitstring],
                        "ideal_prob": [ideal_probs[bitstring]],
                        "noisy_prob": [noisy_counts[bitstring] / shots]
                    }
                )
            ]
        )
    
    return df

def run(
    circuits: List[QuantumCircuit],
    transpiled_circuits: List[QuantumCircuit],
    data_path: str,
    backend,
    shots: int
) -> Dict[str, float]:
    """TODO COMPLETE."""

    f_xeb_data = {}

    for index, (circuit, transpiled_circuit) in enumerate(zip(circuits, transpiled_circuits)):
        print(f"Executing circuit {index}..")

        num_bits = circuit.num_qubits
        hilbert_dim = 2 ** num_bits

        df = execute_circuit(circuit, transpiled_circuit, shots, backend, num_bits, hilbert_dim)

        save_path = f"{data_path}/circuit_{index}_data.csv"
        df.to_csv(save_path)

        f_xeb_data[f"circuit_{index}"] = compute_f_xeb(df["ideal_prob"], df["noisy_prob"], hilbert_dim)

        print(f"DONE.")

    return f_xeb_data

def compute_f_xeb(p_1, p_2, hilbert_dim) -> float:
    """TODO COMPLETE."""

    return (hilbert_dim * (p_1 @ p_2)) - 1

if __name__ == "__main__":

    BACKEND = FakeGuadalupeV2()
    NUM_CIRCUITS = 10
    NUM_QUBITS = 12
    NUM_CYCLES = 9
    SHOTS = 500_000

    circuits, transpiled_circuits = gen_circuits(NUM_CIRCUITS, NUM_QUBITS, NUM_CYCLES, BACKEND)

    f_xeb_data = run(circuits, transpiled_circuits, DATA_PATH, BACKEND, SHOTS)

    export_metadata(
        circuits,
        transpiled_circuits,
        path=DATA_PATH,
        num_qubits=NUM_QUBITS,
        num_cycles=NUM_CYCLES,
        backend=BACKEND,
        f_xeb_data=f_xeb_data
    )