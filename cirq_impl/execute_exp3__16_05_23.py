"""TODO COMPLETE."""

import os
import sys
from importlib import import_module
from typing import Optional

import cirq
import qsimcirq

from execute import execute_exp


GOOGLE_DATA_PATH = "cirq_impl/google_chosen_data/"
GENERATED_DATA_PATH = "cirq_impl/generated_data/"
BACKEND = qsimcirq.QSimSimulator()

sys.path.append(os.getcwd())
        

def dir_to_exp_config(
        dir_path: str,
        num_bits: int,
        num_cycles: int,
        p1_error: float,
        meas_error: Optional[float] = None,
        shots: Optional[int] = 500_000,
        noise_model_name: Optional[str] = "NO_NAME_NOISE_MODEL" # TODO CONSIDER
):
    """TODO COMPLETE."""

    dir_path_dots = dir_path.replace("/", ".")

    exp_configs = []
    for entry in os.scandir(dir_path):
        
        if entry.is_file():
            entry_dict = {}
            
            entry_dict["name"] = entry.name.removesuffix(".py")
            entry_dict["num_bits"] = num_bits
            entry_dict["num_cycles"] = num_cycles
            
            module = import_module(dir_path_dots + entry_dict["name"])
            entry_dict["circuit_obj"] = module.CIRCUIT
            entry_dict["qubit_order"] = module.QUBIT_ORDER
            entry_dict["noisy_circuit_objs"] = {
                noise_model_name: module.CIRCUIT.with_noise(cirq.depolarize(p1_error))
            }
            
            entry_dict["backend"] = BACKEND
            entry_dict["shots"] = shots
            entry_dict["p1_error"] = p1_error
            entry_dict["meas_error"] = meas_error
            
            exp_configs.append(entry_dict)
    
    return exp_configs


if __name__ == "__main__":

    dir_path_n14_m14_e0 = f"{GOOGLE_DATA_PATH}n12_m14_e0_DRAFT/"
    num_bits = 12
    num_cycles = 14
    p1_error = 0.0016
    meas_error = 0.038
    shots = 500_000

    exp_configs = dir_to_exp_config(
        dir_path_n14_m14_e0,
        num_bits,
        num_cycles,
        p1_error,
        meas_error,
        shots,
        noise_model_name="p1_0.0016__p2_0__m_0.038"
    )

    # print("\n".join(sorted([exp_config["name"] for exp_config in exp_configs])))
    execute_exp(exp_configs, GENERATED_DATA_PATH)