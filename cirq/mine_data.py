"""
Functions for mining data according to Google's 2019 quantum supremacy Sycamore experiment:
    * `mine_data`.
"""

from typing import List, Optional, Iterable, Any, Dict
from collections import Counter

import pandas as pd
import cirq
import qsimcirq

GOOGLE_DATA_PATH = "google_chosen_data/"

def _gen_bitstring(bits: Iterable[Any]) -> str:
    """TODO COMPLETE."""

    return "".join([str(bit) for bit in bits])

def mine_data(
    num_bits: int,
    circuit_obj: cirq.Circuit,
    qubit_order: List[str], # TODO not str?
    google_raw_data_path: str,
    noisy_circuit_objs: Dict[str, cirq.Circuit], # TODO not cirq.Circuit?
    backend: qsimcirq.QSimSimulator, # TODO another type?
    shots: Optional[int] = 500_000,
):
    """
    TODO VERIFY.
    Simulates a quatum circuit `circuit_obj` with every noise model
    listed in `noise_models`, combines it with data from Google's Sycamore
    experiment and saves new analyzed data into `targert_data_path`.

    Args:
        TODO COMPLETE.

    Returns:
        TODO COMPLETE.
    """

    hilbert_dim = 2**num_bits
    ideal_statevector = circuit_obj.final_state_vector()
    bitstrings = pd.Series([format(num, "b").zfill(num_bits) for num in range(hilbert_dim)])

    google_data = pd.read_csv(google_raw_data_path, sep="\s+", dtype={"bitstring": str})
    google_data_counter = Counter(google_data["bitstring"])
    google_noisy_probs = [google_data_counter[bitstring] / shots for bitstring in bitstrings]

    df = pd.DataFrame(
        {
            "bitstring": bitstrings,
            "ideal_real_amp": ideal_statevector.real,
            "ideal_imag_amp": ideal_statevector.imag,
            "ideal_prob": ideal_statevector.real**2 + ideal_statevector.imag**2,
            "google_noisy_prob": google_noisy_probs,
        }
    )

    if not circuit_obj.has_measurements():
        circuit_obj.append(cirq.measure(qubit_order))

    noise_models_probs = {}
    for noise_model_name, noisy_circuit_obj in noisy_circuit_objs.items():

        if not noisy_circuit_obj.has_measurements():
            noisy_circuit_obj.append(cirq.measure(qubit_order))

        noisy_sim_res = backend.run(noisy_circuit_obj, repetitions=500_000)
        noisy_sim_counter = noisy_sim_res.histogram(key=qubit_order, fold_func=_gen_bitstring)

        noise_models_probs[f"{noise_model_name}_prob"] = [
            noisy_sim_counter[bitstring] / shots for bitstring in bitstrings
        ]

    return pd.concat([df, pd.DataFrame(noise_models_probs)], axis=1)

# if __name__ == "__main__":
    
#     from google_chosen_data.n12_m14_s0_e0.circuit_n12_m14_s0_e0_pEFGH import (
#         CIRCUIT as n12_m_14_circuit,
#         QUBIT_ORDER as n12_m14_qubit_order
#     )

#     md = mine_data(
#         num_bits=12,
#         circuit_obj=n12_m_14_circuit,
#         qubit_order = n12_m14_qubit_order,
#         google_raw_txt_data_path=f"{GOOGLE_DATA_PATH}n12_m14_s0_e0/amplitudes_n12_m14_s0_e0_pEFGH.txt",
#         noisy_circuit_objs={
#             "depolarize_single_0.0016": n12_m_14_circuit.with_noise(cirq.depolarize(0.0016))
#         },
#         backend=qsimcirq.QSimSimulator()
#     )

#     print(md)