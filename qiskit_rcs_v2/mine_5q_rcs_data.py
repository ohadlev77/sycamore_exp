""" Mining data by random circuit sampling (RCS) of 5 linearly-connected qubits,
using real IBM superconducting devices."""


import json
from typing import List, Tuple
from copy import deepcopy

from qiskit import transpile, qpy, QuantumCircuit
from qiskit_ibm_provider import IBMProvider, least_busy
from qiskit_aer import StatevectorSimulator

from gen_haar_random_circuit import gen_haar_random_circuit


def gen_circuits(
    num_circuits: int,
    num_qubits: int,
    num_cycles: int,
    backend
) -> Tuple[List[QuantumCircuit], List[QuantumCircuit]]:
    """Generates `num_circuits` Haar-random quantum circuits, with `num_qubits` qubits and `num_cycles`
    cycles in each circuit. A 'cycle' is a contraction of a layer with a column of single qubit
    Haar-random unitary rotations, with a layer of CNOT gates between a selected subset of adjacent
    qubits. The selected subset of adjacent qubits is alternating back and forth between cycles.
    
    Returns:
        (Tuple[List[QuantumCircuit], List[QuantumCircuit]]): a list with the Haar-random circuits
        generated without measurements at the end, and a list with the same circuits transpiled
        with respect to `backend`, with measurements at the end."""

    circuits = []
    transpiled_circuits = []

    for _ in range(num_circuits):

        qc_no_meas = gen_haar_random_circuit(num_qubits, num_cycles)
        circuits.append(qc_no_meas)

        qc = deepcopy(qc_no_meas)
        qc.measure_all()
        tpqc = transpile(
            qc,
            backend=backend,
            optimization_level=3
        )
        transpiled_circuits.append(tpqc)

    return circuits, transpiled_circuits

def export_metadata(
    circuits: List[QuantumCircuit],
    transpiled_circuits: List[QuantumCircuit],
    path: str,
    num_qubits: int,
    num_cycles: int,
    backend,
    job_id: str
) -> None:
    """Exports `circuits` and `transpiled_circuits` into serialized QPY files,
    and documents all other arguments into a metadata JSON file.
    Saves all files into the `path` directory."""

    with open(f"{path}/circuits.qpy", "wb") as f:
        qpy.dump(circuits, f)

    with open(f"{path}/transpiled_circuits.qpy", "wb") as f:
        qpy.dump(transpiled_circuits, f)

    with open(f"{path}/metadata.json", "w") as f:
        circuits_metadata = {
            "num_circuits": len(circuits),
            "num_qubits": num_qubits,
            "num_cycles": num_cycles,
            "circuit_depth": circuits[0].depth(),
            "transpiled_circuit_depth": transpiled_circuits[0].depth(),
            "backend": backend.name,
            "job_id": job_id
        }

        json.dump(circuits_metadata, f, indent=4)

def execute(
    circuits: List[QuantumCircuit],
    transpiled_circuits: List[QuantumCircuit],
    ideal_probs_filepath: str,
    backend
) -> str:
    """Executes `circuits` on the ideal, noiseless `StatevectorSimulator()`,
    and executes `transpiled_circuits` on `backend`.
    
    Returns:
        (str): the job ID of the execution job on the `backend`."""

    # Ideal statevector simulation of `circuits`
    print("Ideally simulating all circuits..")
    ideal_job = StatevectorSimulator().run(circuits)
    print("Done.")
    export_execution_res(ideal_job, ideal_probs_filepath)

    # Execution of `transpiled_circuits` on `backend`
    shots = backend.configuration().max_shots
    print(f"Executing all circuits on {backend}, shots={shots}..")
    job = backend.run(transpiled_circuits, shots=shots)
    job_id = job.job_id()
    print(f"Job ID = {job_id}")

    return job_id

def export_execution_res(job, filepath: str) -> None:
    """Exports the counts/probability distribution of `job` into a JSON file (`filepath`)."""
    
    with open(filepath, "w") as f:
        json.dump(job.result().get_counts(), f, indent=4)


if __name__ == "__main__":

    provider = IBMProvider()
    backend = least_busy(
        provider.backends(
            filters=lambda backend: not backend.configuration().simulator and \
            backend.configuration().num_qubits >= 7
        )
    )

    NUM_CIRCUITS = 10
    NUM_QUBITS = 5
    NUM_CYCLES = 9

    circuits, transpiled_circuits = gen_circuits(NUM_CIRCUITS, NUM_QUBITS, NUM_CYCLES, backend)
    path = "/home/ohad/work/sycamore_exp_project/src/qiskit_rcs_v2/exp_data"

    job_id = execute(
        circuits,
        transpiled_circuits,
        ideal_probs_filepath=f"{path}/ideal_probs.json",
        backend=backend
    )

    export_metadata(
        circuits,
        transpiled_circuits,
        path=path,
        num_qubits=NUM_QUBITS,
        num_cycles=NUM_CYCLES,
        backend=backend,
        job_id=job_id
    )