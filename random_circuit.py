# This code is part of Qiskit.
#
# (C) Copyright IBM 2017.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Utility functions for generating random circuits."""

import numpy as np

from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit import Reset
from qiskit.circuit.library.standard_gates import (
    IGate,
    XGate,
    SXGate,
    RZGate,
    CXGate
)
from qiskit.circuit.exceptions import CircuitError


def random_circuit_modified(
    num_qubits, depth, max_operands=3, measure=False, conditional=False, reset=False, seed=None
):
    """
    A modified version of qiski.circuit.random_circuit.
    This version generates circuits only with the native gates of IBM's backends,
    that is: 'id', 'x', 'sx', 'rz', 'cx'.
    From here the original docstrings are presented.

    Generate random circuit of arbitrary size and form.

    This function will generate a random circuit by randomly selecting gates
    from the set of standard gates in :mod:`qiskit.extensions`. For example:

    .. jupyter-execute::

        from qiskit.circuit.random import random_circuit

        circ = random_circuit(2, 2, measure=True)
        circ.draw(output='mpl')

    Args:
        num_qubits (int): number of quantum wires
        depth (int): layers of operations (i.e. critical path length)
        max_operands (int): maximum operands of each gate (between 1 and 3)
        measure (bool): if True, measure all qubits at the end
        conditional (bool): if True, insert middle measurements and conditionals
        reset (bool): if True, insert middle resets
        seed (int): sets random seed (optional)

    Returns:
        QuantumCircuit: constructed circuit

    Raises:
        CircuitError: when invalid options given
    """
    if max_operands < 1 or max_operands > 3:
        raise CircuitError("max_operands must be between 1 and 3")

    one_q_ops = [
        IGate,
        XGate,
        SXGate,
        RZGate,
    ]
    one_param = [RZGate]
    two_param = []
    three_param = []
    two_q_ops = [CXGate]
    three_q_ops = []

    qr = QuantumRegister(num_qubits, "q")
    qc = QuantumCircuit(num_qubits)

    if measure or conditional:
        cr = ClassicalRegister(num_qubits, "c")
        qc.add_register(cr)

    if reset:
        one_q_ops += [Reset]

    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)
    rng = np.random.default_rng(seed)

    # apply arbitrary random operations at every depth
    for _ in range(depth):
        # choose either 1, 2, or 3 qubits for the operation
        remaining_qubits = list(range(num_qubits))
        rng.shuffle(remaining_qubits)
        while remaining_qubits:
            max_possible_operands = min(len(remaining_qubits), max_operands)
            num_operands = rng.choice(range(max_possible_operands)) + 1
            operands = [remaining_qubits.pop() for _ in range(num_operands)]
            if num_operands == 1:
                operation = rng.choice(one_q_ops)
            elif num_operands == 2:
                operation = rng.choice(two_q_ops)
            elif num_operands == 3:
                operation = rng.choice(three_q_ops)
            if operation in one_param:
                num_angles = 1
            elif operation in two_param:
                num_angles = 2
            elif operation in three_param:
                num_angles = 3
            else:
                num_angles = 0
            angles = [rng.uniform(0, 2 * np.pi) for x in range(num_angles)]
            register_operands = [qr[i] for i in operands]
            op = operation(*angles)

            # with some low probability, condition on classical bit values
            if conditional and rng.choice(range(10)) == 0:
                value = rng.integers(0, np.power(2, num_qubits))
                op.condition = (cr, value)

            qc.append(op, register_operands)

    if measure:
        qc.measure(qr, cr)

    return qc