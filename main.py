from noise_models import ideal_model, basic_model, fake_kolkata_model
from random_samples import RandomSamples

if __name__ == "__main__":

    # Defining circuits
    circuits = [
        {'num_qubits': 12, 'depth': 10},
        {'num_qubits': 12, 'depth': 12},
        {'num_qubits': 12, 'depth': 14},
        {'num_qubits': 14, 'depth': 10},
        {'num_qubits': 14, 'depth': 12},
        {'num_qubits': 14, 'depth': 14},
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

    # A list of all noise models
    noise_models = [ideal_model, basic_model, fake_kolkata_model]

    # Creating experiment infrastructure
    samples_generator = RandomSamples(
        circuits=circuits,
        noise_models=noise_models,
        default_shots=50000
    )

    # Adding experiments
    samples_generator.build_exp(shots=100000)
    samples_generator.build_exp(shots=500000)

    # Displaying infrastructure and experiments details
    samples_generator.details()

    # Running experiments
    samples_generator.run()