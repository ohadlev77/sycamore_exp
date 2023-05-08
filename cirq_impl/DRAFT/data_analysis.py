from typing import List

import cirq
import qsimcirq

from n12_m14_s0_eo.circuit_n12_m14_s0_e0_pEFGH import CIRCUIT

class BasicDepolarizationModel(cirq.NoiseModel):
    """TODO COMPLETE"""

    def __init__(self, one_qubit_error: float = 0.0016, two_qubit_error: float = 0.0062) -> None:
        """TODO COMPLETE"""

        self.e1 = one_qubit_error
        self.e2 = two_qubit_error

    def noisy_operation(self, operation: cirq.Operation):
        """TODO COMPLETE"""

        num_qubits = len(operation.qubits)
        error_rate = self.e1 if num_qubits == 1 else self.e2
        depolarization_channel = cirq.depolarize(error_rate, n_qubits=num_qubits)

        return [operation, depolarization_channel.on(*operation.qubits)]

def f_xeb(counts_1, counts_2, num_samples: int, num_qubits: int):
    """TODO COMPLETE"""
    
    p_1 = map(lambda x: x / num_samples, counts_1)
    p_2 = map(lambda x: x / num_samples, counts_2)

    f_xeb = ((2 ** num_qubits) * sum([p * q for p, q in zip(p_1, p_2)])) - 1

    return f_xeb

if __name__ == "__main__":
    print('0000')
    CIRCUIT.append(cirq.measure(CIRCUIT.all_qubits()))
    shots=500_000
    num_qubits = 12

    ideal_results = qsimcirq.qsim_simulator.QSimSimulator().run(CIRCUIT, repetitions=shots)
    ideal_counts = ideal_results.data.value_counts()
    print('a')

    # noisy_circuit = CIRCUIT.with_noise(BasicDepolarizationModel())
    noisy_circuit = CIRCUIT.with_noise(cirq.NoiseModel.from_noise_model_like(cirq.depolarize(0.0016)))
    print('a1')
    print(len(noisy_circuit))
    noisy_results = qsimcirq.qsim_simulator.QSimSimulator().run(noisy_circuit, repetitions=500_000)
    print('a2')
    noisy_counts = noisy_results.data.value_counts()

    print('b')
    print(f_xeb(ideal_counts, noisy_counts, num_samples=shots, num_qubits=num_qubits))
    print('c')