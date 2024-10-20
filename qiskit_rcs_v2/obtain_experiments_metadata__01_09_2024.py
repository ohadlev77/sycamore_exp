import json
from pathlib import PosixPath, Path
from typing import Iterable

import pandas as pd


QUBIT_PARAMS_INDEXES = {
    "T1": 0,
    "T2": 1,
    "frequency": 2,
    "anharmonicity": 3,
    "readout_error": 4,
    "prob_meas0_prep1": 5,
    "prob_meas1_prep0": 6,
    "readout_length": 7
}


def calculate_avg_error_rate_guadalupe(
    props_json_path: str | PosixPath,
    param_key_name: str,
    qubit_indexes: Iterable[int] = range(16)
) -> float:
    
    with open(props_json_path, "r") as f:
        props = json.load(f)

    total_error = 0
    for qubit_index in qubit_indexes:
        total_error += props["qubits"][qubit_index][
            QUBIT_PARAMS_INDEXES[param_key_name]
        ]["value"]

    avg_error = total_error / len(qubit_indexes)

    return avg_error


def calculate_avg_error_rate_nairobi_jakarta(
    props_csv_path: str | PosixPath,
    param_key_name: str,
    qubit_indexes: Iterable[int] = range(7)
) -> float:
    
    df = pd.read_csv(props_csv_path)
    
    total_error = 0
    for qubit_index in qubit_indexes:
        total_error += df[param_key_name][qubit_index]

    avg_error = total_error / len(qubit_indexes)

    return avg_error


def calculate_data_for_first_email() -> dict[str, float]:

    guadalupe_props_json_path = Path("sycamore_exp/qiskit_rcs_v2/exp_data__12q__fake_guadalupe__v2/props_guadalupe.json")
    guadalupe_total_num_qubits = 16
    guadalupe_used_qubit_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14]

    guadalupe_config = {
        "FakeGuadalupe_average__prob_meas0_prep1": {
            "props_json_path": guadalupe_props_json_path,
            "param_key_name": "prob_meas0_prep1",
            "qubit_indexes": range(guadalupe_total_num_qubits)
        },
        "FakeGuadalupe_average__prob_meas1_prep0": {
            "props_json_path": guadalupe_props_json_path,
            "param_key_name": "prob_meas1_prep0",
            "qubit_indexes": range(guadalupe_total_num_qubits)
        },
        "FakeGuadalupe_average__prob_meas0_prep1__used_qubits_only": {
            "props_json_path": guadalupe_props_json_path,
            "param_key_name": "prob_meas0_prep1",
            "qubit_indexes": guadalupe_used_qubit_indexes,
        },
        "FakeGuadalupe_average__prob_meas1_prep0__used_qubits_only": {
            "props_json_path": guadalupe_props_json_path,
            "param_key_name": "prob_meas1_prep0",
            "qubit_indexes": guadalupe_used_qubit_indexes,
        },
    }

    print("guadalupe_used_qubit_indexes =", guadalupe_used_qubit_indexes)
    for field_name, kwargs in guadalupe_config.items():
        print(f"{field_name} =", calculate_avg_error_rate_guadalupe(**kwargs))
    print()
    
    nairobi_props_csv_path = Path(
        "/home/ohadlev77/personal/research/gil/sycamore_exp/qiskit_rcs_v2/exp_data__5q__ibm_nairobi__v1/ibm_nairobi_calibrations_2023-07-23T10_28_09Z.csv"
    )
    jakarta_props_csv_path = Path(
        "/home/ohadlev77/personal/research/gil/sycamore_exp/qiskit_rcs_v2/exp_data__5q__ibmq_jakarta__v1/ibmq_jakarta_calibrations_2023-07-23T09_18_50Z.csv"
    )
    nairobi_jakarta_total_num_qubits = 7
    nairobi_used_qubit_indexes = [0, 1, 3, 5, 6]
    jakarta_used_qubit_indexes = [1, 2, 3, 5, 6]

    nairobi_jakarta_config = {
        "IBM_Nairobi_average__prob_meas0_prep1": {
            "props_csv_path": nairobi_props_csv_path,
            "param_key_name": "Prob meas0 prep1 ",
            "qubit_indexes": range(nairobi_jakarta_total_num_qubits)
        },
        "IBM_Nairobi_average__prob_meas1_prep0": {
            "props_csv_path": nairobi_props_csv_path,
            "param_key_name": "Prob meas1 prep0 ",
            "qubit_indexes": range(nairobi_jakarta_total_num_qubits)
        },
        "IBM_Nairobi_average__prob_meas0_prep1__used_qubits_only": {
            "props_csv_path": nairobi_props_csv_path,
            "param_key_name": "Prob meas0 prep1 ",
            "qubit_indexes": nairobi_used_qubit_indexes,
        },
        "IBM_Nairobi_average__prob_meas1_prep0__used_qubits_only": {
            "props_csv_path": nairobi_props_csv_path,
            "param_key_name": "Prob meas1 prep0 ",
            "qubit_indexes": nairobi_used_qubit_indexes,
        },
        "IBM_Jakarta_average__prob_meas0_prep1": {
            "props_csv_path": jakarta_props_csv_path,
            "param_key_name": "Prob meas0 prep1 ",
            "qubit_indexes": range(nairobi_jakarta_total_num_qubits)
        },
        "IBM_Jakarta_average__prob_meas1_prep0": {
            "props_csv_path": jakarta_props_csv_path,
            "param_key_name": "Prob meas1 prep0 ",
            "qubit_indexes": range(nairobi_jakarta_total_num_qubits)
        },
        "IBM_Jakarta_average__prob_meas0_prep1__used_qubits_only": {
            "props_csv_path": jakarta_props_csv_path,
            "param_key_name": "Prob meas0 prep1 ",
            "qubit_indexes": jakarta_used_qubit_indexes,
        },
        "IBM_Jakarta_average__prob_meas1_prep0__used_qubits_only": {
            "props_csv_path": jakarta_props_csv_path,
            "param_key_name": "Prob meas1 prep0 ",
            "qubit_indexes": jakarta_used_qubit_indexes,
        },
    }

    print("nairobi_used_qubit_indexes =", nairobi_used_qubit_indexes)
    print("jakarta_used_qubit_indexes =", jakarta_used_qubit_indexes)
    for field_name, kwargs in nairobi_jakarta_config.items():
        print(f"{field_name} =", calculate_avg_error_rate_nairobi_jakarta(**kwargs))

if __name__ == "__main__":

    # from pathlib import Path
    # from qiskit import qpy 

    # path = Path(
    #     "/home/ohadlev77/personal/research/gil/sycamore_exp/qiskit_rcs_v2/exp_data__5q__ibmq_jakarta__v1/transpiled_circuits.qpy"
    # )
    # with open(path, "rb") as f:
    #     transpiled_circuits = qpy.load(f)

    # print(transpiled_circuits[7].draw())

    # nairobi_qubits = [0, 1, 3, 5, 6]
    # jakarta_qubits = [1, 2, 3, 5, 6]

    calculate_data_for_first_email()