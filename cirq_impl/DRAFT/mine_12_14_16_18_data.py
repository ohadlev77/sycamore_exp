"""TODO COMPLETE."""

import os
from typing import Dict, Optional, Union
from datetime import datetime
from collections import Counter

import qsimcirq

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

from sycamore_exp import SycamoreExpDataEng, SycamoreExpDataAnalysis

# Global constants
cwd = os.getcwd()
ENG_DATA_PATH = f"{cwd}/eng_data"
GOOGLE_DATA_PATH = f"{cwd}/google_chosen_data"

def mine_data(
    exp_configs, #: Dict[str, Dict[str, Union[str, int]]],
    backend,
    target_path: Optional[str] = None,
    shots: Optional[int] = 500_000
) -> None: # TODO NONE?
    """TODO COMPLETE"""

    if target_path is None:
        timestamp = datetime.now().strftime("D%d.%m.%y_T%H.%M.%S")
        dir_name = f"exp_{timestamp}"
        target_path = f"{ENG_DATA_PATH}/{dir_name}/"
        os.mkdir(target_path)

    for name, exp_config in exp_configs.items():
        
        exp_interface = SycamoreExpDataEng(name, exp_config["num_qubits"], exp_config["num_cycles"])

        raw_df, curated_df = exp_interface.data_file_to_df(exp_config["raw_data_path"])
        ideal_sim_res = exp_interface.simulate(
            exp_config["circuit_obj"],
            exp_config["qubit_order"],
            backend,
            shots
        )

        # TODO REMOVE THIS DEBUGGING
        print()
        print(f"------------ {name}: -------------")
        print("Curated DF:")
        print(curated_df)

        print()
        print("Ideally simulated statevector's probabilities:")
        print(f"p_vec = {ideal_sim_res.probs_vector}")
        print(f"len(p_vec) = {len(ideal_sim_res.probs_vector)}")

        print("F_XEB checks:")
        data_an_interface = SycamoreExpDataAnalysis(
            name,
            exp_config["num_qubits"],
            exp_config["num_cycles"]
        )

        data_amps_probs = curated_df["real_amp"]**2 + curated_df["imag_amp"]**2
        print(data_an_interface.compute_f_xeb(curated_df["data_probs"], data_amps_probs))

        counts = {
            key: value / len(raw_df["bitstring"]) for key, value in Counter(raw_df["bitstring"]).items()
        }
        print(counts)
        print()
        print(sum(counts.values()))


if __name__ == "__main__":

    mine_data(
        exp_configs={
            "n12_m14_s0_e0": {
                "num_qubits": 12,
                "num_cycles": 14,
                "raw_data_path": f"{GOOGLE_DATA_PATH}/n12_m14_s0_e0/amplitudes_n12_m14_s0_e0_pEFGH.txt",
                "circuit_obj": n12_m14_circuit,
                "qubit_order": n12_m14_qubit_order
            },
            # "n14_m14_s0_e0": {
            #     "num_qubits": 14,
            #     "num_cycles": 14,
            #     "raw_data_path": f"{GOOGLE_DATA_PATH}/n14_m14_s0_e0/amplitudes_n14_m14_s0_e0_pEFGH.txt",
            #     "circuit_obj": n14_m14_circuit,
            #     "qubit_order": n14_m14_qubit_order
            # },
            # "n16_m14_s0_e0": {
            #     "num_qubits": 16,
            #     "num_cycles": 14,
            #     "raw_data_path": f"{GOOGLE_DATA_PATH}/n16_m14_s0_e0/amplitudes_n16_m14_s0_e0_pEFGH.txt",
            #     "circuit_obj": n16_m14_circuit,
            #     "qubit_order": n16_m14_qubit_order
            # },
            # "n18_m14_s0_e0": {
            #     "num_qubits": 18,
            #     "num_cycles": 14,
            #     "raw_data_path": f"{GOOGLE_DATA_PATH}/n18_m14_s0_e0/amplitudes_n18_m14_s0_e0_pEFGH.txt",
            #     "circuit_obj": n18_m14_circuit,
            #     "qubit_order": n18_m14_qubit_order
            # }
        },
        backend=qsimcirq.QSimSimulator()
    )