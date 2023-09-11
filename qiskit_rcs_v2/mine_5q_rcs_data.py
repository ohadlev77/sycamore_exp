""" Mining data by random circuit sampling (RCS) of 5 linearly-connected qubits,
using real IBM superconducting devices."""


import json
from typing import List

from qiskit import QuantumCircuit
from qiskit_ibm_provider import IBMProvider, least_busy
from qiskit_aer import StatevectorSimulator

from mine_data_core_funs import gen_circuits, export_metadata


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