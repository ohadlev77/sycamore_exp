"""
This module contains the RandomSamples class that provides an infrastructure for mining statistical
data from simulations of quantum circuits.
"""

import os
import time
import json
from typing import List, Dict, Union, Optional

from qiskit.result.counts import Counts
from qiskit_aer import AerSimulator
from qiskit_aer.noise.noise_model import NoiseModel

from random_circuit import random_circuit_modified
from decorators import timer_dec

# Constants
BACKEND = AerSimulator()
MAX_OPERANDS = 2
SHOTS = 1024
PATH_TO_DATA = "data/"

class RandomSamples:
    """
    An infrastructure for mining probability distributions out of quantum circuits simulations.
    """

    def __init__(
        self,
        circuits: Optional[List[Dict[str, List[Union[int, str]]]]] = None,
        noise_models: Optional[List[NoiseModel]] = None
    ) -> None:
        """
        Args:
            circuits (Optional[List[Dict[str, List[Union[int, str]]]]]): a list of circuits to simulate,
            while every element of the list is a dictionary of the following format:
            `{'num_qubits': int, 'depth': (int)}`.

            noise_models (Optional[List[NoiseModel]]): a list of `NoiseModel` objects.
        """

        if circuits is None:
            self.circuits = []
        else:
            self.circuits = circuits
            self.build_circuits()

        if noise_models is None:
            self.noise_models = []
        else:
            self.noise_models = noise_models

        self.experiments = []
        self.build_exp()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object. for details use `details` method>"
    
    def details(self) -> str:
        """
        Prints the important details of each instance - that is the list of circuits, noise models
        and defined experiments.
        """

        details_map = {
            "Circuits": self.circuits,
            "Noise Models": self.noise_models,
            "Experiments ({circuit_id: List[noise_model_ids]})": self.experiments
        }

        for detail_name, detail in details_map.items():
            print()
            print(f"{detail_name}:")

            for index, item in enumerate(detail):
                try:
                    print(f"{index}. {item.name}")
                except AttributeError:
                    print(f"{index}. {item}")

    def add_circuit(self, circuits: List[Dict[str, List[Union[int, str]]]]) -> None:
        """
        Appends circuit definitions (one or more) to `self.circuits`.

        Args:
            circuit (List[Dict[str, List[Union[int, str]]]]): see `__init__` docstrings.
        """

        self.circuits += circuits
        self.build_circuits()

    def add_noise_model(self, noise_models: List[NoiseModel]):
        """
        Appends noise models (one or more) to `self.noise_models`.

        Args:
            noise_models (List[NoiseModel]): see `__init__` docstrings.
        """

        self.noise_models += noise_models

    def build_circuits(self, circuit_ids: Optional[List[int]] = None):
        """
        Creates random `QuantumCircuit` objects from circuits definitions.

        Args:
            circuit_ids (Optional[List[int]]): list of circuit IDs.
        """

        if circuit_ids is None:
            circuit_ids = [id for id in range(len(self.circuits))]

        for circuit_id in circuit_ids:
            if 'circuit_object' not in self.circuits[circuit_id]:
                self.circuits[circuit_id]['circuit_object'] = random_circuit_modified(
                    num_qubits=self.circuits[circuit_id]['num_qubits'],
                    depth=self.circuits[circuit_id]['depth'],
                    max_operands=MAX_OPERANDS,
                    measure=True
                )

    def build_exp(self, combinations: Optional[Dict[int, List[int]]] = None) -> None:
        """
        Preparing experiments (= a combination of circuits and noise models) and appends them
        to `self.experiments`.

        Args:
            combinations (Optional[Dict[int, List[int]]]):
                - a dictionary with the keys as circuit IDs and the value as a list of
                noise models' IDs for each circuit ID.
                - If None - that's a flag to this method that indicates - build an experiment
                such that each circuit will run with all noise models.
                
        """

        # If combinations is None, assign to each circuit all noise models
        if combinations is None:
            combinations = {}
            all_noise_models_ids = list(range(len(self.noise_models)))
            for circuit_id in range(len(self.circuits)):
                combinations[circuit_id] = all_noise_models_ids

        self.experiments.append(combinations)

    @timer_dec
    def run(self, exp_ids: Optional[List[int]] = None) -> None:
        """
        Runs experiments and saves each experiment's data to a unique folder.

        Args:
            exp_ids: Optional[List[int]]):
                - A list of all experiments' IDs to run.
                - If None - runs all experiments.
        """

        if exp_ids is None:
            exp_ids = [id for id in range(len(self.experiments))]
    
        for exp_id in exp_ids:
            dir_path = f"{PATH_TO_DATA}{time.time()}_exp_{exp_id}/"
            os.mkdir(dir_path)
            print(f"Runs experiment {exp_id} and saves data to {dir_path}..")

            for circuit_id, noise_models_ids in self.experiments[exp_id].items():
                for noise_model_id in noise_models_ids:
                    self.generate_single_data_file(circuit_id, noise_model_id, dir_path)

    def generate_single_data_file(self, circuit_id: int, noise_model_id: int, dir_path: str) -> None:
        """
        Runs a simulation for a sicngle circuit and saves the data to a JSON file.
        """

        file_name = f"circuit_{circuit_id}__num_qubits_{self.circuits[circuit_id]['num_qubits']}" \
                    f"__depth_{self.circuits[circuit_id]['depth']}" \
                    f"__noise_model_{self.noise_models[noise_model_id].name}.json"

        print(f"    Simulating and saving data to {file_name}..")

        # TODO IMPROVE THAT HOOK WITH IDEAL NOISE MODEL
        if self.noise_models[noise_model_id].name == 'ideal':
            job = BACKEND.run(
                self.circuits[circuit_id]['circuit_object'],
                shots=SHOTS
            )
        else:
            job = BACKEND.run(
                self.circuits[circuit_id]['circuit_object'],
                shots=SHOTS,
                noise_model=self.noise_models[noise_model_id]
            )
        counts = job.result().get_counts()

        # Transforming counts into probability distributions
        p_dist = RandomSamples.counts_to_p_dist(counts, SHOTS, self.circuits[circuit_id]['num_qubits'])

        #Saving the results into JSON files
        with open(f"{dir_path}{file_name}", 'w') as file_to_write:
            json.dump(p_dist, file_to_write)

    @staticmethod
    def counts_to_p_dist(
        counts: Counts,
        shots: int,
        num_qubits: int = None,
        precision: int = 10
    )-> Dict[str, float]:
        """
        Transforms a `Counts` object into a probability distribution dictionary.
        
        Args:
            counts (Counts) - the `Counts` object, i.e the sampled results.
            shots (int) - number of shots, i.e number of repeated runs of a circuit.
            num_qubits (int) - number of qubits (default=None).
                - If specfied, all 2^n bitstrings will be included in
                the returned dictionary, otherwise only those with more
                than 0 samples.
            precision (int) - number of digits to keep after the decimal point (default=10),
            for each probability.
                
        Returns:
            (Dict[str, float]) - a dictionary of the results' probability distribution.
        """
        
        # A dictionary for storing the probability distribution
        p_dist = {}
        
        # Case 1 - saving data only for bitstrings with more than 0 samples
        if num_qubits is None:        
            for binary_string, num_samples in counts.items():
                p_dist[binary_string] = round(num_samples / shots, precision)
        
        # Case 2 - saving data only for all bitstrings, even those with 0 samples (i.e with probability=0)
        else:
            for i in range(2**num_qubits):
                bitstring = bin(i)[2:].zfill(num_qubits)

                if bitstring in counts:
                    p_dist[bitstring] = round(counts[bitstring] / shots, precision)
                else:
                    p_dist[bitstring] = 0
            
        return p_dist