"""Mining data by RCS of 12-qubit circuits, using noisy simulator models ("Fake" machines)."""


from typing import List, Dict
from collections import Counter

import pandas as pd
from qiskit import QuantumCircuit
from qiskit.providers.fake_provider import FakeGuadalupeV2
from qiskit_aer import StatevectorSimulator

from mine_data_core_funs import gen_circuits, export_metadata

DATA_PATH = "exp_data_12q_fake_gudalupe_v2"


def execute_circuit(
    circuit: QuantumCircuit,
    transpiled_circuit: QuantumCircuit,
    shots: int,
    backend,
    num_bits: int,
    hilbert_dim: int
) -> pd.DataFrame:
    """Executes `circuit` on the ideal, noiseless `StatevectorSimulator()`,
    and executes `transpiled_circuit` on `backend` (should be a real backend or anoisy simulator).
    
    Returns:
        (pd.DataFrame): a table with all `hilbert_dim` bitstrings, each bitstring associated with
        its ideal probability to be sampled, and its noisy reconstructed probability."""

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
    """Executes `circuits` on ideal, noiseless simulator, and `transpiled_circuits` on `backend, using
    the function `execute_circuit()`. Exports the results into CSV files in the `data_path` directory.
    
    Returns:
        (Dict[str, float]): the cross entropy benchmarking fidelity (F_XEB) for each circuit,
        calculated using the `compute_f_xeb()` function."""

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
    """Returns the cross entropy benchmarking fidelity (F_XEB) for `p_1` and `p_2` - which should be
    probability distibutions over the same sample space, of dimension `hilbert_dim`."""

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