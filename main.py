from qiskit_aer import noise
from qiskit_aer.noise import NoiseModel

from random_samples import RandomSamples

if __name__ == "__main__":

    # Defining circuits
    circuits = [
        {'num_qubits': 12, 'depth': 10},
        {'num_qubits': 12, 'depth': 12},
        {'num_qubits': 12, 'depth': 14},
        {'num_qubits': 16, 'depth': 10},
        {'num_qubits': 16, 'depth': 12},
        {'num_qubits': 16, 'depth': 14}
        # THE FOLLOWING CIRCUITS GENERATE HEAVY JSON FILES
        # {'num_qubits': 20, 'depth': 10},
        # {'num_qubits': 20, 'depth': 12},
        # {'num_qubits': 20, 'depth': 14},
        # {'num_qubits': 24, 'depth': 10},
        # {'num_qubits': 24, 'depth': 12},
        # {'num_qubits': 24, 'depth': 14}
    ]
    
    # Defining basic depolarizng noise model
    depolarizing_error_1 = noise.depolarizing_error(0.001, 1)
    depolarizing_error_2 = noise.depolarizing_error(0.01, 2)
    basic_model = NoiseModel()
    basic_model.add_all_qubit_quantum_error(depolarizing_error_1, instructions=['rz', 'sx', 'x'])
    basic_model.add_all_qubit_quantum_error(depolarizing_error_2, instructions=['cx'])
    basic_model.name = "basic_depolarization_model"

    # Defining an ideal noise model
    ideal_model = NoiseModel()
    ideal_model.name = "ideal"

    # A list of all noise models
    noise_models = [ideal_model, basic_model]

    # Creating experiment infrastructure and running it
    samples_generator = RandomSamples(
        circuits=circuits,
        noise_models=noise_models,
    )
    print(samples_generator.details())
    samples_generator.run()