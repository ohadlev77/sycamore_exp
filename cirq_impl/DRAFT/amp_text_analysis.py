import pandas as pd
import numpy as np
import cirq
import qsimcirq
from n12_m14_s0_eo.circuit_n12_m14_s0_e0_pEFGH import CIRCUIT

shots = 500_000
file_path = "/home/ohad/work/sycamore_exp_project/src/CIRQ/n12_m14_s0_eo/amplitudes_n12_m14_s0_e0_pEFGH.txt"
data = pd.read_csv(file_path, delim_whitespace=True)
num_qubits = 12
hilbert_dim = 2 ** num_qubits

data.sort_values('bitstring', inplace=True)
data['probs_p'] = data['imag_amp'] ** 2 + data['real_amp'] ** 2
counts = data['bitstring'].value_counts(sort=False).to_frame(name="XXX")
data.drop_duplicates(inplace=True)
data['probs_q'] = np.array(counts['XXX']) / shots

print(CIRCUIT.has_measurements())
fsv = qsimcirq.qsim_simulator.QSimSimulator().simulate(CIRCUIT).final_state_vector

CIRCUIT_m = CIRCUIT
CIRCUIT_m.append(cirq.measure(CIRCUIT.all_qubits()))
results = qsimcirq.qsim_simulator.QSimSimulator().run(CIRCUIT_m, repetitions=5_000_000)
ideal_simulated_counts = results.data.value_counts(normalize=True, sort=False).rename_axis(
    "bitstrings_values"
).reset_index(name="probs_p_simulated")
data['probs_p_simulated'] = np.zeros((hilbert_dim, 1))

l = list(ideal_simulated_counts['bitstrings_values'])
for i in range(hilbert_dim):
    if i not in l:
        new_line = pd.DataFrame({"bitstrings_values": [i], "probs_p_simulated": [0]})
        ideal_simulated_counts = ideal_simulated_counts.append(new_line, ignore_index=True)

ideal_simulated_counts.sort_values("bitstrings_values", inplace=True)

def f_xeb(probs_p: np.ndarray, probs_q: np.ndarray, num_qubits: int) -> float:
    return ((hilbert_dim) * sum(probs_p * probs_q)) - 1

# print(counts)
print(data)

print(ideal_simulated_counts)
print(type(ideal_simulated_counts))
# print(ideal_simulated_counts.loc[4])
# print(ideal_simulated_counts.loc[4] == 4)

print()
print(f"Original data F_XEB = {f_xeb(data['probs_p'], data['probs_q'], num_qubits)}")

print()
pps = np.array(ideal_simulated_counts['probs_p_simulated'])
print(f"Ideal simulated data F_XEB = {f_xeb(data['probs_p'], pps, num_qubits)}")

print(pps)
print(sum(pps))
print(fsv)