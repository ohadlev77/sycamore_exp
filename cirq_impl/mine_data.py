"""
Functions for mining data according to Google's 2019 quantum supremacy Sycamore experiment:
    * `mine_data`.
"""

from typing import List, Optional, Iterable, Any, Dict
from collections import Counter

import numpy as np
import pandas as pd
import cirq
import cirq_google
import qsimcirq

GOOGLE_DATA_PATH = "google_chosen_data/"

def _gen_bitstring(bits: Iterable[Any]) -> str:
    """TODO COMPLETE."""

    return "".join([str(bit) for bit in bits])

def mine_data(
    num_bits: int,
    circuit_obj: cirq.Circuit,
    qubit_order: List[str], # TODO not str?
    # google_raw_data_path: str,
    noisy_circuit_objs: Dict[str, cirq.Circuit], # TODO not cirq.Circuit?
    backend: qsimcirq.QSimSimulator, # TODO another type?
    shots: Optional[int] = 500_000,
    meas_error: Optional[float] = None,
    weber_nm: Optional[bool] = False
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

    # google_data = pd.read_csv(google_raw_data_path, sep="\s+", dtype={"bitstring": str})
    # google_data_counter = Counter(google_data["bitstring"])
    # google_noisy_probs = [google_data_counter[bitstring] / shots for bitstring in bitstrings]

    df = pd.DataFrame(
        {
            "bitstring": bitstrings,
            # "ideal_real_amp": ideal_statevector.real,
            # "ideal_imag_amp": ideal_statevector.imag,
            "ideal_prob": ideal_statevector.real**2 + ideal_statevector.imag**2
            # "google_noisy_prob": google_noisy_probs,
        }
    )

    if not circuit_obj.has_measurements():

        cmap = None
        
        # Setting readout error for all qubits - `meas_error` chance for bit-flip upon measurement
        if meas_error is not None:
            single_qubit_cmap = [
                [1 - meas_error, meas_error],
                [meas_error, 1 - meas_error]
            ]
            cmap = {(i, ): single_qubit_cmap for i in range(num_bits)}

        circuit_obj.append(cirq.measure(qubit_order, confusion_map=cmap))

    noise_models_probs = {}
    for _, noisy_circuit_obj in noisy_circuit_objs.items(): # TODO CONSIDER HOW TO STRUCTURE NOISE MODELS AND EXPS

        if not noisy_circuit_obj.has_measurements():
            noisy_circuit_obj.append(cirq.measure(qubit_order))

        noisy_sim_res = backend.run(noisy_circuit_obj, repetitions=shots)
        noisy_sim_counter = noisy_sim_res.histogram(key=qubit_order, fold_func=_gen_bitstring)

        noise_models_probs[f"depolarize_single_0.0016_prob"] = [
            noisy_sim_counter[bitstring] / shots for bitstring in bitstrings
        ]

    df = pd.concat([df, pd.DataFrame(noise_models_probs)], axis=1)

    if weber_nm:
        cal = cirq_google.engine.load_median_device_calibration("weber")
        noise_props = cirq_google.noise_properties_from_calibration(cal)
        noise_model = cirq_google.NoiseModelFromGoogleNoiseProperties(noise_props)
        weber_qvm_sim = qsimcirq.QSimSimulator(noise=noise_model)

        weber_run_res = weber_qvm_sim.run(circuit_obj, repetitions=shots)
        weber_run_hist = weber_run_res.histogram(key=qubit_order)

        qvm_weber_prob = pd.Series(
            [weber_run_hist[num] / shots for num in range(2**num_bits)],
            name="qvm_weber_prob"
        )
        
        df = pd.concat([df, qvm_weber_prob], axis=1)

    return df