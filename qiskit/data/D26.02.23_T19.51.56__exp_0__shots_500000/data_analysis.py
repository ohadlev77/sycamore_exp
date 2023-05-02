import json

path = "src/data/D26.02.23_T19.51.56__exp_0__shots_500000/"

ideal_12 = f"{path}circuit_0__num_qubits_12__depth_500/circuit_0__num_qubits_12__" \
    "depth_500__noise_model_ideal__nonzero_rate_0.99.json"
noisy_12 = f"{path}circuit_0__num_qubits_12__depth_500/circuit_0__num_qubits_12__" \
    "depth_500__noise_model_basic_depolarization_model__nonzero_rate_1.0.json"

ideal_14 = f"{path}circuit_1__num_qubits_14__depth_500/circuit_1__num_qubits_14__" \
    "depth_500__noise_model_ideal__nonzero_rate_0.97.json"
noisy_14 = f"{path}circuit_1__num_qubits_14__depth_500/circuit_1__num_qubits_14__" \
    "depth_500__noise_model_basic_depolarization_model__nonzero_rate_1.0.json"

ideal_16 = f"{path}circuit_2__num_qubits_16__depth_501/circuit_2__num_qubits_16__" \
    "depth_501__noise_model_ideal__nonzero_rate_0.89.json"
noisy_16 = f"{path}circuit_2__num_qubits_16__depth_501/circuit_2__num_qubits_16__" \
    "depth_501__noise_model_basic_depolarization_model__nonzero_rate_1.0.json"

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

print(f"F_xeb_12 = {compute_f_xeb(12, ideal_12, noisy_12)}")
print(f"F_xeb_14 = {compute_f_xeb(14, ideal_14, noisy_14)}")
print(f"F_xeb_16 = {compute_f_xeb(16, ideal_16, noisy_16)}")

print()
print(f"F_xeb_12_ideal = {compute_f_xeb(12, ideal_12, ideal_12)}")
print(f"F_xeb_14_ideal = {compute_f_xeb(14, ideal_14, ideal_14)}")
print(f"F_xeb_16_ideal = {compute_f_xeb(16, ideal_16, ideal_16)}")