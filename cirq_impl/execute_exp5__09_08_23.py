""" Mining data for patch circuits, n=12, m=14. """

import os
import sys
from importlib import import_module
from typing import Optional

import cirq
import qsimcirq

from execute import execute_exp


GOOGLE_DATA_PATH = "src/cirq_impl/google_chosen_data/"
GENERATED_DATA_PATH = "src/cirq_impl/generated_data/"
BACKEND = qsimcirq.QSimSimulator()

sys.path.append(os.getcwd())
        

def dir_to_exp_config(
        dir_path: str,
        num_bits: int,
        num_cycles: int,
        p1_error: float,
        meas_error: Optional[float] = None,
        shots: Optional[int] = 500_000,
        noise_model_name: Optional[str] = "NO_NAME_NOISE_MODEL", # TODO CONSIDER
        weber_nm: Optional[bool] = False
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
            entry_dict["weber_nm"] = weber_nm
            
            exp_configs.append(entry_dict)
    
    return exp_configs


if __name__ == "__main__":

    google_data_dir_path = f"{GOOGLE_DATA_PATH}patch_n12_m14_e18/"
    num_bits = 12
    num_cycles = 14
    p1_error = 0.0016
    meas_error = None
    weber_nm = True
    shots = 500_000

    exp_configs = dir_to_exp_config(
        google_data_dir_path,
        num_bits,
        num_cycles,
        p1_error,
        meas_error,
        shots,
        noise_model_name="depolarize_p1_0.0016",
        weber_nm=weber_nm
    )

    execute_exp(exp_configs, GENERATED_DATA_PATH)