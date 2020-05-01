# Copyright 2019-2020 Cambridge Quantum Computing
#
# Licensed under a Non-Commercial Use Software Licence (the "Licence");
# you may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence, but note it is strictly for non-commercial use.

from .operators import (
    _qubit_operator_to_qubit_pauli_tensor_list,
    _get_coeff_from_qubit_operator,
)
from pytket import Circuit, Qubit
from pytket.circuit import Pauli, PauliExpBox, CircBox
from pytket.partition import (
    QubitPauliTensor,
    term_sequence,
    PauliPartitionStrat,
    GraphColourMethod,
)
from typing import Optional


def gen_term_sequence_circuit(
    operator: "QubitOperator",
    reference_state: Circuit,
    partition_strat: PauliPartitionStrat = PauliPartitionStrat.CommutingSets,
    colour_method: GraphColourMethod = GraphColourMethod.Lazy,
) -> Circuit:
    """Sequences QubitOperator terms to generate a circuit made of CircBoxes.
    Each CircBox contains a sequence of PauliExpBox objects.

    :param operator: The operator terms to sequence
    :type operator: QubitOperator
    :param reference_state: reference state to add sequenced terms to.
    :type reference_state: Circuit
    :param partition_strat: a Partition strategy
    :type partition_strat: PauliPartitionStrat, optional
    """
    qpt_list = _qubit_operator_to_qubit_pauli_tensor_list(operator)
    qpt_list_list = term_sequence(qpt_list, partition_strat, colour_method)
    n_qbs = reference_state.n_qubits
    circ = reference_state.copy()
    qbs = circ.qubits
    for out_qpt_list in qpt_list_list:
        circ_to_box = Circuit(n_qbs)
        for qpt in out_qpt_list:
            coeff = _get_coeff_from_qubit_operator(operator, qpt)
            paulis_to_box = []
            i = 0
            for qb in qpt:
                while Qubit(i) < qb:
                    i += 1
                    paulis_to_box.append(Pauli.I)
                pauli = qpt[qb]
                paulis_to_box.append(pauli)
                i += 1
            while i < n_qbs:
                paulis_to_box.append(Pauli.I)
                i += 1
            pbox = PauliExpBox(paulis_to_box, coeff)
            circ_to_box.add_pauliexpbox(pbox, qbs)
        cbox = CircBox(circ_to_box)
        circ.add_circbox(cbox, qbs)
    return circ
