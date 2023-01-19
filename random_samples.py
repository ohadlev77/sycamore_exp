"""
RandomSamples object class.
"""

import os
from datetime import datetime
import json
from typing import List, Dict, Union, Optional
from hashlib import sha256
import numpy as np

from qiskit.result.counts import Counts
from qiskit_aer.noise.noise_model import NoiseModel

from random_circuit import random_circuit_modified
from util import timer_dec, timestamp
from constants import BACKEND, MAX_OPERANDS, SHOTS, PATH_TO_DATA, DATA_PRECISION
from experiment import Experiment

class RandomSamples:
    """
    An infrastructure for mining data of probability distributions out of
    random quantum circuits simulations, with various circuits and noise models.
    """

    def __init__(
        self,
        circuits: Optional[List[Dict[str, int]]] = None,
        noise_models: Optional[List[NoiseModel]] = None
    ) -> None:
        """
        Args:
            circuits (Optional[List[Dict[str, int]]): a list of circuits to simulate,
            while every element of the list is a dictionary of the following format:
            `{'num_qubits': (int), 'depth': (int)}`.
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

        # By default, building exp_0 which combines all circuits with all noise models
        self.experiments = []
        self.build_exp()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object. for details use `details` method>"
    
    def details(self) -> None:
        """
        Prints the important details of each instance - that is the list of circuits, noise models
        and defined experiments.
        """

        # Defining details to print
        details_map = {
            "Circuits": self.circuits,
            "Noise Models": self.noise_models,
            "Experiments ({circuit_id: List[noise_model_ids]})": self.experiments
        }

        # Iterating over the details and printing it
        for detail_name, detail in details_map.items():

            # Caption
            print()
            print(f"{detail_name}:")

            # Content (only noise models have `name` attributes)
            if not detail:
                print('EMPTY')
            else:
                for index, item in enumerate(detail):
                    try:
                        print(f"{index}. {item.name}")
                    except AttributeError:
                        print(f"{index}. {item}")

    def add_circuits(self, circuits: List[Dict[str, int]]) -> None:
        """
        Appends circuit definitions (one or more) to `self.circuits`.

        Args:
            circuits (List[Dict[str, int]]): a list of circuit definitions,
            while each circuit definition should be a dictionary in a format defined
            in the `__init__` docstrings.
        """
        
        # Appending circuit definitions
        self.circuits += circuits

        # Build `QuantumCircuit` objects
        self.build_circuits()

    def add_noise_model(self, noise_models: List[NoiseModel]) -> None:
        """
        Appends noise models (one or more) to `self.noise_models`.

        Args:
            noise_models (List[NoiseModel]): a list of `NoiseModel` object,
            see the `__init__` docstrings for more details.
        """

        self.noise_models += noise_models

    def build_circuits(self, circuit_ids: Optional[List[int]] = None) -> None:
        """
        Creates random `QuantumCircuit` objects from circuit definitions, and adds them to the
        dictionary of each circuit definition under the key 'circuit_object'.

        Args:
            circuit_ids (Optional[List[int]]):
                - A list of circuit IDs to build objects for.
                - If None (default) - `QuantumCircuit` objects are built for every circuit that
                doesn't have the 'circuit_object' key yet.            
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
        Prepares `Experiment` objects and appends them to `self.experiments`.

        Args:
            combinations (Optional[Dict[int, List[int]]]):
                - a dictionary with circuit IDs as keys and lists of noise models' IDs
                 as values for each circuit ID.
                - If None (default) - that's a flag to this method that indicates -
                build an experiment such that each circuit will run with all noise models.
        """

        # If `combinations` is None, assign to each circuit all noise models
        if combinations is None:
            combinations = {}

            all_noise_models_ids = list(range(len(self.noise_models)))
            number_of_circuits = len(self.circuits)

            for circuit_id in range(number_of_circuits):
                combinations[circuit_id] = all_noise_models_ids

        # If `combinations == {}`, that means there are no circuits and noise models (both) defined
        if combinations != {}:
            self.experiments.append(Experiment(combinations))

    @timer_dec("Total execution time = ")
    def run(self, exp_ids: Optional[List[int]] = None) -> None:
        """
        Runs experiments and saves each experiment's data to a unique folder.

        Args:
            exp_ids: Optional[List[int]]):
                - A list of all experiments' IDs to run.
                - If None - runs all experiments.
        """

        # In that case, running all experiments
        if exp_ids is None:
            exp_ids = [id for id in range(len(self.experiments))]
    
        # Iterating over the experiments
        for exp_id in exp_ids:

            # Creating a unique data folder for the experiment
            exp_dir_path = f"{PATH_TO_DATA}{timestamp(datetime.now())}__exp_{exp_id}__shots_{SHOTS}/"
            os.mkdir(exp_dir_path)
            print()
            print(f"Runs experiment {exp_id} and saves data to '{exp_dir_path}':")

            # Generating metadata for the experiment's noise models
            print()
            print(f"    Generating and saving noise models' metadata.")
            noise_models_metadata_dir_path = f"{exp_dir_path}noise_models_metadata/"
            os.mkdir(noise_models_metadata_dir_path)
            self.generate_noise_models_metadata(exp_id, noise_models_metadata_dir_path)

            # For each experiment, iterating over its combinations of circuits with noise models
            for circuit_id, noise_models_ids in self.experiments[exp_id].combinations.items():

                print()
                print(f"    Circuit {circuit_id}:")

                # Creating a unique data folder for the specific circuit
                circuit_dir_path = f"{exp_dir_path}circuit_{circuit_id}__num_qubits_" \
                                   f"{self.circuits[circuit_id]['num_qubits']}" \
                                   f"__depth_{self.circuits[circuit_id]['depth']}/"
                os.mkdir(circuit_dir_path)

                # Creating a `circuit_properties` folder and exporting circuit data into it
                circuit_properties_path = f"{circuit_dir_path}circuit_properties/"
                os.mkdir(circuit_properties_path)
                self.export_single_circuit_data(circuit_id, circuit_properties_path)

                # Generating a data file for each noise model
                for noise_model_id in noise_models_ids:
                    self.generate_single_data_file(circuit_id, noise_model_id, circuit_dir_path)

    @timer_dec("    Metadata processing time = ")
    def generate_noise_models_metadata(self, exp_id: int, dir_path: str) -> None:
        """
        Generates metadata for the experiment's defined noise models, and saves it to `dir_path`.

        Args:
            exp_id (int): ID of the experiment.
            dir_path (str): a path to a directoy for saving the metadata into.
        """

        for noise_model_id in self.experiments[exp_id].noise_models:

            # Just setting a pointer for convenience
            noise_model = self.noise_models[noise_model_id]

            # Creating a directory for the metadata
            noise_model_metadata_dir_path = f"{dir_path}{noise_model.name}/"
            os.mkdir(noise_model_metadata_dir_path)

            # Writing metadata to files
            with open(f"{noise_model_metadata_dir_path}id.txt", "w") as id_file:
                id_file.write(noise_model.__str__())
            with open(f"{noise_model_metadata_dir_path}to_dict.json", "w") as to_dict_file:
                json.dump(noise_model.to_dict(True), to_dict_file)

    @timer_dec("        Circuit data exporting time = ")
    def export_single_circuit_data(self, circuit_id: int, dir_path: str) -> None:
        """
        For a given quantum circuit (identified by its `circuit_id`), this method generates
        and saves the following files to `dir_path`:
            - A .qasm file that contains the QASM 2.0 representation of the circuit.
            - A circuit diagram (PNG file).
            - A .json file contains the following data:
                - circuit_id.
                - num_qubits.
                - depth.
                - gates_count.
                - qasm_hash_sha256hex - hex representation of sha256 encoding
                of the circuit's QASM 2.0 code.

        Args:
            circuit_id (int): ID number of the quantum circuit to be exported.
            dir_path (str): a path to the directory to save the data in.
        """

        print(f"        Exporting circuit {circuit_id} data into '{dir_path}'.")

        # Just setting a pointer for convenience
        qc = self.circuits[circuit_id]['circuit_object']

        # Saving a QASM file of the circuit
        qc_qasm = qc.qasm()
        with open(f"{dir_path}circuit_{circuit_id}.qasm", "w") as qasm_file:
            qasm_file.write(qc_qasm)

        # Saving the circuit diagram
        qc.draw(output="mpl", filename=f"{dir_path}circuit_{circuit_id}_diagram.png", fold=-1)

        # Collecting properties and saving them to a JSON file
        circuit_data = {
            'circuit_id': circuit_id,
            'num_qubits': qc.num_qubits,
            'depth': qc.depth(),
            'gates_count': qc.count_ops(),
            'qasm_hash_sha256hex': sha256(b"{qc_qasm}").hexdigest()
        }
        with open(f"{dir_path}circuit_{circuit_id}_data.json", "w") as data_file:
            json.dump(circuit_data, data_file, indent=4)

    @timer_dec("        Circuit simulation execution time = ")
    def generate_single_data_file(
        self,
        circuit_id: int,
        noise_model_id: int,
        dir_path: str
    ) -> None:
        """
        Runs a simulation for a single circuit combined with a single noise model,
        and saves the data to a JSON file.

        Args:
            circuit_id (int): ID number of the circuit to simulate.
            noise_model_id (int): ID number of the noise model to simulate the circuit with.
            dir_path (str): a path to the directory to save the simulation results in.
        """

        # Just setting pointers for convenience
        qc = self.circuits[circuit_id]['circuit_object']
        num_qubits = self.circuits[circuit_id]['num_qubits']
        depth = self.circuits[circuit_id]['depth']
        noise_model = self.noise_models[noise_model_id]

        print()
        print(f"        Simulating circuit {circuit_id} with noise model {noise_model_id}.")

        job = BACKEND.run(qc, shots=SHOTS, noise_model=noise_model)
        counts = job.result().get_counts()

        # The percentage of non-zero samples out of the 2^num_qubits possible samples
        nonzero_rate = round(len(counts) / (2 ** num_qubits), 2)

        file_name = f"circuit_{circuit_id}__num_qubits_{num_qubits}__depth_{depth}__noise_model_" \
                    f"{noise_model.name}__nonzero_rate_{nonzero_rate}.json"
        print(f"        Saving data to {file_name}.")

        # Transforming counts into a probability distribution
        p_dist = RandomSamples.counts_to_p_dist(counts, SHOTS, num_qubits)

        # Saving the results into a JSON file
        with open(f"{dir_path}{file_name}", 'w') as file_to_write:
            json.dump(p_dist, file_to_write)

    @staticmethod
    def counts_to_p_dist(
        counts: Counts,
        shots: int,
        num_qubits: Optional[int] = None,
        precision: Optional[int] = DATA_PRECISION
    )-> Dict[str, float]:
        """
        Transforms a `Counts` object into a probability distribution dictionary (that contains all
        the 2^num_qubits possible bitstrings outcomes, also those that have beem sampled 0 times).
        
        Args:
            counts (Counts): the `Counts` object, i.e the sampled results.
            shots (int): number of shots, i.e number of repeated runs of a circuit.
            num_qubits (Optional[int]): number of qubits (default=None).
                - If specfied, all 2^n bitstrings will be included in
                the returned dictionary, otherwise only those with more
                than 0 samples.
            precision (Optional[int]): number of digits to keep after the decimal point (default=`DATA_PRECISION` constant),
            for each probability.
                
        Returns:
            (Dict[str, float]): a dictionary of the results' probability distribution.
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
                    p_dist[bitstring] = np.format_float_positional(round(counts[bitstring] / shots, precision))
                else:
                    p_dist[bitstring] = 0
            
        return p_dist