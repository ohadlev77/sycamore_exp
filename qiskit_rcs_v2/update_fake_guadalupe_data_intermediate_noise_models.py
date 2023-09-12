"""
Updating fake_guadalupe data with 2 more noise models:
    (1) Depolarizing noise model with e_1 = 0.0016 * 4/3 for single qubit gates,
    and e_2 = 0.0062 * 16/15.
    (2) On top of the depolariztion described in (1), we add a readout error
    over all the qubits of e_r = 0.038.
"""


from collections import Counter
from copy import deepcopy

import pandas as pd
from qiskit import qpy
from qiskit_aer import AerSimulator, noise
from qiskit_aer.noise import NoiseModel
from qiskit.converters.circuit_to_dag import circuit_to_dag


if __name__ == "__main__":

    DATA_PATH = "src/qiskit_rcs_v2/exp_data__12q__fake_guadalupe__v2"
    NUM_BITS = 12
    HILBERT_DIM = 2**NUM_BITS
    SHOTS = 500_000

    with open(f"{DATA_PATH}/transpiled_circuits.qpy", "rb") as f:
        transpiled_circuits = qpy.load(f)

    # Depolarization noise model definition
    depo_noise_model = NoiseModel()
    depo_e1 = noise.depolarizing_error(param=0.0016 * 4/3, num_qubits=1)
    depo_e2 = noise.depolarizing_error(param=0.0062 * 16/15, num_qubits=2)
    depo_noise_model.add_all_qubit_quantum_error(depo_e1, instructions=["sx", "x"])
    depo_noise_model.add_all_qubit_quantum_error(depo_e2, instructions=["cx"])

    for index, transpiled_circuit in enumerate(transpiled_circuits):
        print(f"Handling circuit {index}..")

        # Finding out which qubits are active (the circuit is transpiled) to adjust the readout errors
        idle_qubits = [qubit.index for qubit in list(circuit_to_dag(transpiled_circuit).idle_wires())]
        active_qubits = [i for i in range(transpiled_circuit.num_qubits) if i not in idle_qubits]

        # Defining the readout errors on the active qubits
        depo_and_readout_noise_model = deepcopy(depo_noise_model)
        for qubit_index in active_qubits:
            depo_and_readout_noise_model.add_readout_error(
                error=noise.ReadoutError(
                    [
                        [1 - 0.038, 0.038],
                        [0.038, 1 - 0.038]
                    ]
                ),
                qubits=[qubit_index]
            )

        csv_file_path = f"{DATA_PATH}/circuit_{index}_data.csv"
        df = pd.read_csv(csv_file_path, dtype={"bitstring": "str"}, index_col="Unnamed: 0")
        df.rename(columns={"noisy_prob": "fake_guadalupe_prob"}, inplace=True)

        job = AerSimulator().run(transpiled_circuit, noise_model=depo_noise_model, shots=SHOTS)
        depo_counts = Counter(job.result().get_counts())
        depo_probs = [depo_counts[format(i, "b").zfill(NUM_BITS)] / SHOTS for i in range(HILBERT_DIM)]

        job = AerSimulator().run(
            transpiled_circuit,
            noise_model=depo_and_readout_noise_model,
            shots=SHOTS
        )
        depo_and_readout_counts = Counter(job.result().get_counts())
        depo_and_readout_probs = [
            depo_and_readout_counts[format(i, "b").zfill(NUM_BITS)] / SHOTS for i in range(HILBERT_DIM)
        ]

        new_df = pd.concat(
            [df, pd.DataFrame({
                "depolarization_prob": depo_probs,
                "depolarization_and_readout_prob": depo_and_readout_probs
            })],
            axis=1
        )

        new_df.to_csv(csv_file_path)

        print(f"DONE with circuit {index}.")
