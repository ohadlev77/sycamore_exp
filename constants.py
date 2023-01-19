"""
Package's constants definitions.
"""

from qiskit_aer import AerSimulator

# Backend to run the experiments upon
BACKEND = AerSimulator()

# Maximun number of operands for each gate in the random circuit generation
MAX_OPERANDS = 2

# Number of iterations to run each quantum circuit
SHOTS = 20000

# A path to the directory that experiments data is saved into (From the main directory of the package)
PATH_TO_DATA = "data/"

# Number of digits to keep after the decimal point for each computed probability
DATA_PRECISION = 10