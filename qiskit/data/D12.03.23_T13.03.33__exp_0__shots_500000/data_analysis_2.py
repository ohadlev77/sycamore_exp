import json
from qiskit import QuantumCircuit

path = "/home/ohad/work/sycamore_exp_project/src/data/D12.03.23_T13.03.33__exp_0__shots_500000/"

ideal_12 = "/home/ohad/work/sycamore_exp_project/src/data/D12.03.23_T13.03.33__exp_0__shots_500000/circuit_0__num_qubits_12__depth_500/circuit_0__num_qubits_12__depth_500__noise_model_ideal__nonzero_rate_0.99.json"
noisy_12 = "/home/ohad/work/sycamore_exp_project/src/data/D12.03.23_T13.03.33__exp_0__shots_500000/circuit_0__num_qubits_12__depth_500/circuit_0__num_qubits_12__depth_500__noise_model_basic_depolarization_model__nonzero_rate_1.0.json"

def compute_f_xeb(n: int, ideal_p_dist_path: str, noisy_q_dist_path: str):
    """
    """
    
    with open(ideal_p_dist_path, "r") as ideal_file:
        ideal_data = json.load(ideal_file)

    with open(noisy_q_dist_path, "r") as noisy_file:
        noisy_data = json.load(noisy_file)

    ideal_p_dist = [float(p) for p in ideal_data.values()]
    noisy_q_dist = [float(q) for q in noisy_data.values()]

    f_xeb = (2 ** n) * sum([p * q for p, q in zip(ideal_p_dist, noisy_q_dist)]) - 1
    return f_xeb

print()
f_xeb_12 = compute_f_xeb(12, ideal_12, noisy_12)
print(f"F_xeb_12 = {f_xeb_12}")
# print(f"F_xeb_14 = {compute_f_xeb(14, ideal_14, noisy_14)}")
# print(f"F_xeb_16 = {compute_f_xeb(16, ideal_16, noisy_16)}")

print()
print(f"F_xeb_12_ideal = {compute_f_xeb(12, ideal_12, ideal_12)}")
# print(f"F_xeb_14_ideal = {compute_f_xeb(14, ideal_14, ideal_14)}")
# print(f"F_xeb_16_ideal = {compute_f_xeb(16, ideal_16, ideal_16)}")

qc = QuantumCircuit.from_qasm_file("/home/ohad/work/sycamore_exp_project/src/data/D12.03.23_T13.03.33__exp_0__shots_500000/circuit_n12_m14_s0_e0_pEFGH.qasm")
ops = qc.count_ops()
print(ops)
nonlocal_ops = ops['cx']
local_ops = sum(ops.values()) - nonlocal_ops
F_est = ((1 - 0.0016) ** local_ops) * ((1 - 0.0062) ** nonlocal_ops)
print(f"F_est = {F_est}")

print()
print(f_xeb_12 / F_est)
