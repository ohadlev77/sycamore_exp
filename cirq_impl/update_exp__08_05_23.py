""" Executes an experiment that updates the generated data of the 08/05/2023 experiment with
data from a simulation on a `weber` QVM noise model. """

import os
import sys
from importlib import import_module
from typing import List

import pandas as pd

import cirq
import cirq_google
import qsimcirq

GOOGLE_DATA_PATH = "src/cirq_impl/google_chosen_data/n14_m14_e0"
EXP_GEN_DATA_PATH = "src/cirq_impl/generated_data/exp_D08.05.23_T17.42.25"

sys.path.append(os.getcwd())


def update_weber_qvm_execution(
        google_py_files: List[str],
        py_files_dots_path: str,
        existing_csv_files: List[str],
        csv_files_path: str,
        num_bits: int,
        shots: int
) -> None:
    """ Iterates over existing CSV experimental data files already generated, and updates
    each CSV file with a new column that contains experimental data of executing Google's circuits
    from `google_py_files` on a `weber` Quantum Virtual Machine (and its defined noise model)."""

    
    # Setting-up the `weber` QVM
    cal = cirq_google.engine.load_median_device_calibration("weber")
    noise_props = cirq_google.noise_properties_from_calibration(cal)
    noise_model = cirq_google.NoiseModelFromGoogleNoiseProperties(noise_props)
    weber_qvm_sim = qsimcirq.QSimSimulator(noise=noise_model)

    for py_file, csv_file in zip(google_py_files, existing_csv_files):
        print()
        print("Handling", py_file, csv_file, "...")

        py_module = import_module(f"{py_files_dots_path}.{py_file}")
        
        if not py_module.CIRCUIT.has_measurements():
            py_module.CIRCUIT.append(cirq.measure(py_module.QUBIT_ORDER, key="end_meas"))

        weber_run_res = weber_qvm_sim.run(py_module.CIRCUIT, repetitions=shots)
        weber_run_hist = weber_run_res.histogram(key="end_meas")

        csv_file_path = f"{csv_files_path}/{csv_file}"
        df = pd.read_csv(csv_file_path, index_col=0, dtype="str")

        qvm_weber_prob = pd.Series(
            [weber_run_hist[num] / shots for num in range(2**num_bits)],
            name="qvm_weber_prob"
        )
        df = pd.concat([df, qvm_weber_prob], axis=1)

        df.to_csv(csv_file_path)

        print("Done.")

if __name__ == "__main__":
    
    l1 = os.listdir(GOOGLE_DATA_PATH)
    l1 = [element[:-3] for element in l1 if element.endswith(".py")]
    l1.sort()
    # print("Google data:")
    # pprint(l1)

    l2 = os.listdir(EXP_GEN_DATA_PATH)
    l2 = [element for element in l2 if element.endswith(".csv")]
    l2.sort()
    # print()
    # print("Experiment existing data:")
    # pprint(l2)

    update_weber_qvm_execution(
        l1,
        GOOGLE_DATA_PATH.replace("/", "."),
        l2,
        EXP_GEN_DATA_PATH,
        num_bits=14,
        shots=500_000
    )