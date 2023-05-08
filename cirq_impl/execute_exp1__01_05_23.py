"""TODO COMPLETE."""

import cirq
import qsimcirq

from execute import execute_exp

# Importing Google's original circuit-objects
from google_chosen_data.n12_m14_s0_e0.circuit_n12_m14_s0_e0_pEFGH import (
    CIRCUIT as n12_m14_circuit,
    QUBIT_ORDER as n12_m14_qubit_order
)
from google_chosen_data.n14_m14_s0_e0.circuit_n14_m14_s0_e0_pEFGH import (
    CIRCUIT as n14_m14_circuit,
    QUBIT_ORDER as n14_m14_qubit_order
)
from google_chosen_data.n16_m14_s0_e0.circuit_n16_m14_s0_e0_pEFGH import (
    CIRCUIT as n16_m14_circuit,
    QUBIT_ORDER as n16_m14_qubit_order
)
from google_chosen_data.n18_m14_s0_e0.circuit_n18_m14_s0_e0_pEFGH import (
    CIRCUIT as n18_m14_circuit,
    QUBIT_ORDER as n18_m14_qubit_order
)


GOOGLE_DATA_PATH = "google_chosen_data/"
GENERATED_DATA_PATH = "generated_data/"
BACKEND = qsimcirq.QSimSimulator()


if __name__ == "__main__":

    exp_configs = [
        {
            "name": "n12_m14_s0_e0",
            "num_bits": 12,
            "num_cycles": 14,
            "circuit_obj": n12_m14_circuit,
            "qubit_order": n12_m14_qubit_order,
            "google_raw_data_path": f"{GOOGLE_DATA_PATH}n12_m14_s0_e0/amplitudes_n12_m14_s0_e0_pEFGH.txt",
            "noisy_circuit_objs": {
                "depolarize_single_0.0016": n12_m14_circuit.with_noise(cirq.depolarize(0.0016))
            },
            "backend": BACKEND
        },
        {
            "name": "n14_m14_s0_e0",
            "num_bits": 14,
            "num_cycles": 14,
            "circuit_obj": n14_m14_circuit,
            "qubit_order": n14_m14_qubit_order,
            "google_raw_data_path": f"{GOOGLE_DATA_PATH}n14_m14_s0_e0/amplitudes_n14_m14_s0_e0_pEFGH.txt",
            "noisy_circuit_objs": {
                "depolarize_single_0.0016": n14_m14_circuit.with_noise(cirq.depolarize(0.0016))
            },
            "backend": BACKEND
        },
        {
            "name": "n16_m14_s0_e0",
            "num_bits": 16,
            "num_cycles": 14,
            "circuit_obj": n16_m14_circuit,
            "qubit_order": n16_m14_qubit_order,
            "google_raw_data_path": f"{GOOGLE_DATA_PATH}n16_m14_s0_e0/amplitudes_n16_m14_s0_e0_pEFGH.txt",
            "noisy_circuit_objs": {
                "depolarize_single_0.0016": n16_m14_circuit.with_noise(cirq.depolarize(0.0016))
            },
            "backend": BACKEND
        },
        {
            "name": "n18_m14_s0_e0",
            "num_bits": 18,
            "num_cycles": 14,
            "circuit_obj": n18_m14_circuit,
            "qubit_order": n18_m14_qubit_order,
            "google_raw_data_path": f"{GOOGLE_DATA_PATH}n18_m14_s0_e0/amplitudes_n18_m14_s0_e0_pEFGH.txt",
            "noisy_circuit_objs": {
                "depolarize_single_0.0016": n18_m14_circuit.with_noise(cirq.depolarize(0.0016))
            },
            "backend": BACKEND
        }
    ]

    execute_exp(exp_configs, GENERATED_DATA_PATH)