"""Updating metadata in fake_guadalupe data with expected circuit fidelities."""


import json

from qiskit import qpy
from qiskit.providers.fake_provider import FakeGuadalupeV2

from compute_expected_circuit_fidelity import compute_expected_fidelity


if __name__ == "__main__":

    DATA_PATH = "src/qiskit_rcs_v2/exp_data__12q__fake_guadalupe__v2"

    with open(f"{DATA_PATH}/transpiled_circuits.qpy", "rb") as f:
        transpiled_circuits = qpy.load(f)

    backend_props_json = f"{FakeGuadalupeV2.dirname}/{FakeGuadalupeV2.props_filename}"

    expected_fidelities = {}
    for index, circuit in enumerate(transpiled_circuits):
        expected_fidelities[f"circuit_{index}"] = compute_expected_fidelity(circuit, backend_props_json)

    with open(f"{DATA_PATH}/metadata.json", "r") as f:
        metadata = json.load(f)

    metadata["expected_circuit_fidelities"] = expected_fidelities

    with open(f"{DATA_PATH}/metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)