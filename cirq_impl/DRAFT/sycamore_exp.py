"""TODO COMPLETE."""

from typing import Tuple, Optional, List, Union
from dataclasses import dataclass
import collections

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cirq
import qsimcirq

from google_chosen_data.n12_m14_s0_e0.circuit_n12_m14_s0_e0_pEFGH import CIRCUIT, QUBIT_ORDER

@dataclass
class SimulationOutcomes:
    """TODO COMPLETE."""

    results: cirq.study.result.ResultDict
    counts: collections.Counter
    probs_vector: np.ndarray

class SycamoreExpDataEng:
    """TODO COMPLETE."""

    def __init__(self, name: str, num_qubits: int, num_cycles: int) -> None:
        """
        Args:
            name (str): the name of the experiment.
            num_qubits (int): number of qubits ("n") in the experiment's circuit.
            num_cycles (int): numbe of cycles ("m") in the experiment's circuit.
        """

        self.name = name
        self.num_qubits = num_qubits
        self.num_cycles = num_cycles

        self.hilbert_dim = 2**num_qubits

    def data_file_to_df(self, data_file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Processes a raw data file from the Sycamore experiment into pandas' DataFrame objects.

        Args:
            data_file_path (str): path to data file.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]:
                #1 DataFrame is just the raw data in a DataFrame object form.
                #2 DataFrame is the same data but sorted by bitstring value and without duplicates.
        """

        raw_df = pd.read_csv(data_file_path, sep="\s+", dtype={"bitstring": str})

        curated_df = raw_df.drop_duplicates("bitstring")
        curated_df = curated_df.sort_values("bitstring")
        curated_df.loc[:, "data_probs"] = curated_df["real_amp"]**2 + curated_df["imag_amp"]**2

        return raw_df, curated_df
    
    def simulate(
        self,
        circuit: cirq.Circuit,
        qubits_order: List[Union[cirq.GridQubit, cirq.LineQubit, cirq.NamedQubit]],
        backend,
        reps: Optional[int] = 500_000
    ) -> SimulationOutcomes:
        """
        Simulates `circuit` on `backend`.

        Args:
            circuit (cirq.Circuit): circuit to simulate.
            qubits_order (List[Union[cirq.GridQubit, cirq.LineQubit, cirq.NamedQubit]]): the order
            of the qubits in `circuit`.
            backend: backend to simulate the circuit upon.
            reps (Optional[int] = 500_000): repetitions, number of shots.

        Returns: SimulationOutcomes(results, counts, probs_vector):
            See `SimulationOutcomes` docstrings.
        """

        if not circuit.has_measurements():
            circuit.append(cirq.measure(qubits_order))

        results = backend.run(circuit, repetitions=reps)
        counts = results.histogram(key=qubits_order)
        probs_vector = np.array([counts[num] / reps for num in range(self.hilbert_dim)])

        return SimulationOutcomes(results, counts, probs_vector)

class SycamoreExpDataAnalysis:
    """TODO COMPLETE."""

    def __init__(self, name: str, num_qubits: int, num_cycles: int) -> None:
        """
        Args:
            name (str): the name of the experiment.
            num_qubits (int): number of qubits ("n") in the experiment's circuit.
            num_cycles (int): numbe of cycles ("m") in the experiment's circuit.
        """

        self.name = name
        self.num_qubits = num_qubits
        self.num_cycles = num_cycles

        self.hilbert_dim = 2**num_qubits

    def draw_scaled_prb_dist(
        self,
        probs: np.ndarray,
        num_bins: Optional[int] = 70,
        exp_decay_plot: Optional[bool] = False,
        fig_title: Optional[str] = None,
    ) -> None:
        """
        TODO COMPLETE.
        """

        scaled_probs = self.hilbert_dim * probs
        plt.figure(figsize=(12, 5))
        plt.hist(scaled_probs, num_bins, density=True, rwidth=0.9)

        plt.xlabel("Scaled probabilities")
        plt.ylabel("Density")

        if fig_title is not None:
            plt.title(fig_title)

        if exp_decay_plot:
            x = np.linspace(0, max(scaled_probs))
            plt.plot(x, np.e**-x)

    def compute_f_xeb(self, p_1: np.ndarray, p_2: np.ndarray) -> float:
        """
        Computes the linear cross-entropy fidelty (F_XEB) between two probability distributions
        over the same sample space.

        Args:
            p_1 (np.ndarray): probability distribution 1.
            p_2 (np.ndarray): probability distribution 2.

        Returns:
            (float): F_XEB(p_1, p_2).
        """

        return (self.hilbert_dim * p_1.dot(p_2)) - 1

# TODO DELETE
if __name__ == "__main__":

    num_qubits = 12
    num_cycles = 14
    data_file_path = "/home/ohad/work/sycamore_exp_project/src/CIRQ/n12_m14_s0_eo/amplitudes_n12_m14_s0_e0_pEFGH.txt"
    reps = 500_000
    interface = SycamoreExp(name="try", num_qubits=num_qubits, num_cycles=num_cycles)

    psi_1 = interface.circuit_ideal_amps(CIRCUIT)
    raw_df, curated_df = interface.data_file_to_df(data_file_path)
    ideal_sim_data = interface.simulate_ideally(
        CIRCUIT,
        QUBIT_ORDER,
        backend=qsimcirq.QSimSimulator(),
        reps=reps
    )

    print()
    print(f"Ideal simulated probabilities ({reps} reps) = {ideal_sim_data.probs_vector}")

    print()
    print(f"Ideal simulated statevector = {psi_1}")

    print()
    print("Google (curated) data:")
    print(curated_df)

    print()
    print(np.allclose(ideal_sim_data.probs_vector, curated_df["probs"], rtol=0.001, atol=0.001))

    print()
    f_xeb_psim_pvec = interface.compute_f_xeb(p_1=ideal_sim_data.probs_vector, p_2=np.abs(psi_1)**2)
    print(f"f_xeb_psim_pvec = {f_xeb_psim_pvec}")