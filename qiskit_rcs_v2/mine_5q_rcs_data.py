""" Mining data by random circuits sampling of 5 linearly-connected qubits,
using real IBM superconducting devices."""

import json

from qiskit import transpile
from qiskit.tools import job_monitor
from qiskit_ibm_provider import IBMProvider, least_busy

from gen_haar_random_circuit import gen_haar_random_circuit


DATA_PATH = "src/qiskit_rcs_v2/exp_data/"


# Choosing a suitable backend
provider = IBMProvider()
backends = provider.backends(
    filters=lambda backend: not backend.configuration().simulator and \
    backend.configuration().num_qubits >= 7
)

print(f"Available 7-qubits backends: {backends}.")
print()

chosen_backend = least_busy(backends)
print(f"Least busy backend: {chosen_backend}")
print()


# Generating a circuit for the chosen backend
num_qubits = 5
num_cycles = 9

qc = gen_haar_random_circuit(num_qubits, num_cycles)
qc.measure_all()

tpqc = transpile(
    qc,
    backend=chosen_backend,
    optimization_level=3
)

print(f"Number of qubits (n) = {num_qubits}")
print(f"Number of cycles (m) = {num_cycles}")
print(f"Circuit depth = {tpqc.depth()}")
print("Circuit diagram:")
print(tpqc.draw())
print()


# Executing
shots = chosen_backend.configuration().max_shots
print(f"Executing on {chosen_backend}, shots={shots}..")
job = chosen_backend.run(tpqc, shots=shots)
job_monitor(job)


# Exporting data
execution_res = job.result()
with open(f"{DATA_PATH}metadata.json", "w") as metadata_file:
    json.dump(execution_res.to_dict(), metadata_file, indent=4)

execution_counts = execution_res.get_counts()
with open(f"{DATA_PATH}exp_data.json", "w") as exp_data_file:
    json.dump(execution_counts, exp_data_file)