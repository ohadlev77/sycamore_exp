"""
Noise models definitions to be used in this package.
`NoiseModel().name` is defined here as a hook in order to give name
attributes to `NoiseModel` instances conveniently.
"""

from qiskit_aer import noise
from qiskit_aer.noise import NoiseModel
from qiskit.providers.fake_provider import FakeKolkataV2

# Defining an ideal noise model
ideal_model = NoiseModel()
ideal_model.name = "ideal"

# Defining a basic depolarizng noise model, with error rates of 0.16% for single qubit gates
# and 0.62% for 2-qubits gates.
depolarizing_error_1 = noise.depolarizing_error(0.0016, 1)
depolarizing_error_2 = noise.depolarizing_error(0.0062, 2)
basic_model = NoiseModel()
basic_model.add_all_qubit_quantum_error(depolarizing_error_1, instructions=['rz', 'sx', 'x', 'id'])
basic_model.add_all_qubit_quantum_error(depolarizing_error_2, instructions=['cx'])
basic_model.name = "basic_depolarization_model"

# Defining the noise model of the fake backend `FakeKolkataV2`
fake_kolkata_model = NoiseModel.from_backend(FakeKolkataV2())
fake_kolkata_model.name = "fake_kolkata_model"