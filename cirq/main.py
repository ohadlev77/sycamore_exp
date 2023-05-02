"""TODO COMPLETE."""

import os
from datetime import datetime

import cirq
import qsimcirq

from mine_data import mine_data
from analyze_data import draw_scaled_prob_dist

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

def execute_exp(exp_configs, target_data_path):

    target_data_path += f"exp_{datetime.now().strftime('D%d.%m.%y_T%H.%M.%S')}/"
    os.mkdir(target_data_path)

    for exp_config in exp_configs:

        print()
        print(f"Executing {exp_config['name']}.")

        df = mine_data(
            num_bits=exp_config["num_bits"],
            circuit_obj=exp_config["circuit_obj"],
            qubit_order=exp_config["qubit_order"],
            google_raw_data_path=exp_config["google_raw_data_path"],
            noisy_circuit_objs=exp_config["noisy_circuit_objs"],
            backend=exp_config["backend"]
        )
        df.to_csv(f"{target_data_path}{exp_config['name']}.csv")

        hilbert_dim = 2**exp_config["num_bits"]
        draw_scaled_prob_dist(
            df["ideal_prob"],
            hilbert_dim=hilbert_dim,
            exp_decay_plot=True,
            fig_title=f"{exp_config['name']} scaled ideal probabilities distribution",
            savefig_path=f"{target_data_path}{exp_config['name']}_ideal_prob.png"
        )
        draw_scaled_prob_dist(
            df["google_noisy_prob"],
            hilbert_dim=hilbert_dim,
            exp_decay_plot=True,
            fig_title=f"{exp_config['name']} scaled Google probabilities distribution",
            savefig_path=f"{target_data_path}{exp_config['name']}_google_noisy_prob.png"
        )
        draw_scaled_prob_dist(
            df["depolarize_single_0.0016_prob"],
            hilbert_dim=hilbert_dim,
            num_bins=70,
            exp_decay_plot=True,
            fig_title=f"{exp_config['name']} scaled probabilities distribution - depolarizing noise with $p_e = 0.0016$",
            savefig_path=f"{target_data_path}{exp_config['name']}_depolarize_single_0.0016.png"
        )

        print(f"Done with {exp_config['name']}.")
        

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