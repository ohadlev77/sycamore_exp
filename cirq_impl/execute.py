"""TODO COMPLETE."""

import os
from datetime import datetime

import qsimcirq

from mine_data import mine_data
from analyze_data import draw_scaled_prob_dist

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
            # google_raw_data_path=exp_config["google_raw_data_path"],
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
        # draw_scaled_prob_dist(
        #     df["google_noisy_prob"],
        #     hilbert_dim=hilbert_dim,
        #     exp_decay_plot=True,
        #     fig_title=f"{exp_config['name']} scaled Google probabilities distribution",
        #     savefig_path=f"{target_data_path}{exp_config['name']}_google_noisy_prob.png"
        # )
        draw_scaled_prob_dist(
            df["depolarize_single_0.0016_prob"],
            hilbert_dim=hilbert_dim,
            num_bins=70,
            exp_decay_plot=True,
            fig_title=f"{exp_config['name']} scaled probabilities distribution - depolarizing noise with $p_e = 0.0016$",
            savefig_path=f"{target_data_path}{exp_config['name']}_depolarize_single_0.0016.png"
        )

        print(f"Done with {exp_config['name']}.")
