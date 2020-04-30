# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=no-member

"""Polynomially controlled Pauli-rotations."""

from typing import List, Optional, Dict, Sequence

from itertools import product
from sympy.ntheory.multinomial import multinomial_coefficients

from qiskit.circuit import QuantumRegister
from qiskit.circuit.exceptions import CircuitError

from .functional_pauli_rotations import FunctionalPauliRotations


class PolynomialPauliRotations(FunctionalPauliRotations):
    r"""A circuit implementing polynomial Pauli rotations.

    For a polynomial :math`p(x)`, a basis state :math:`|i\rangle` and a target qubit
    :math:`|0\rangle` this operator acts as:

    .. math::

        |i\rangle |0\rangle \mapsto \cos(p(i)) |i\rangle |0\rangle + \sin(p(i)) |i\rangle |1\rangle

    Let n be the number of qubits representing the state, d the degree of p(x) and q_i the qubits,
    where q_0 is the least significant qubit. Then for

    .. math::

        x = \sum_{i=0}^{n-1} 2^i q_i,

    we can write

    .. math::

        p(x) = \sum_{j=0}^{j=d} c_j x_j

    where :math:`c` are the input coefficients, ``coeffs``.
    """

    def __init__(self, num_state_qubits: Optional[int] = None,
                 coeffs: Optional[List[float]] = None,
                 basis: str = 'Y',
                 reverse: bool = False,
                 name: str = 'poly') -> None:
        """Prepare an approximation to a state with amplitudes specified by a polynomial.

        Args:
            num_state_qubits: The number of qubits representing the state.
            coeffs: The coefficients of the polynomial. ``coeffs[i]`` is the coefficient of the
                i-th power of x. Defaults to linear: [0, 1].
            basis: The type of Pauli rotation ('X', 'Y', 'Z').
            reverse: If True, apply the polynomial with the reversed list of qubits
                (i.e. q_n as q_0, q_n-1 as q_1, etc).
            name: The name of the circuit.
        """
        # set default internal parameters
        self._coeffs = coeffs or [0, 1]
        self._reverse = reverse

        # initialize super (after setting coeffs)
        super().__init__(num_state_qubits=num_state_qubits, basis=basis, name=name)

    @property
    def coeffs(self) -> List[float]:
        """The multiplicative factor in the rotation angle of the controlled rotations.

        The rotation angles are ``slope * 2^0``, ``slope * 2^1``, ... , ``slope * 2^(n-1)`` where
        ``n`` is the number of state qubits.

        Returns:
            The rotation angle common in all controlled rotations.
        """
        return self._coeffs

    @coeffs.setter
    def coeffs(self, coeffs: List[float]) -> None:
        """Set the multiplicative factor of the rotation angles.

        Args:
            The slope of the rotation angles.
        """
        self._invalidate()
        self._coeffs = coeffs

        # the number of ancilla's depends on the number of coefficients, so update if necessary
        if coeffs and self.num_state_qubits:
            self._reset_registers(self.num_state_qubits)

    @property
    def degree(self) -> int:
        """Return the degree of the polynomial, equals to the number of coefficients minus 1.

        Returns:
            The degree of the polynomial. If the coefficients have not been set, return 0.
        """
        if self.coeffs:
            return len(self.coeffs) - 1
        return 0

    @property
    def reverse(self) -> bool:
        """Whether to apply the rotations on the reversed list of qubits.

        Returns:
            True, if the rotations are applied on the reversed list, False otherwise.
        """
        return self._reverse

    @reverse.setter
    def reverse(self, reverse: bool) -> None:
        """Set to True to reverse the list of qubits.

        Args:
            reverse: If True, the rotations are applied on the reversed list. If False, then not.
        """
        if self._reverse is None or reverse != self._reverse:
            self._invalidate()
            self._reverse = reverse

    @property
    def num_ancilla_qubits(self) -> int:
        """The number of ancilla qubits in this circuit.

        Returns:
            The number of ancilla qubits.
        """
        return max(1, self.degree - 1)

    def _reset_registers(self, num_state_qubits):
        if num_state_qubits:
            # set new register of appropriate size
            qr_state = QuantumRegister(num_state_qubits, name='state')
            qr_target = QuantumRegister(1, name='target')
            qr_ancilla = QuantumRegister(self.num_ancilla_qubits, name='ancilla')
            self.qregs = [qr_state, qr_target, qr_ancilla]
        else:
            self.qregs = []

    def _check_configuration(self, raise_on_failure: bool = True) -> bool:
        valid = True

        if self.num_state_qubits is None:
            valid = False
            if raise_on_failure:
                raise AttributeError('The number of qubits has not been set.')

        if self.num_qubits < self.num_state_qubits + 1:
            valid = False
            if raise_on_failure:
                raise CircuitError('Not enough qubits in the circuit, need at least '
                                   '{}.'.format(self.num_state_qubits + 1))

        return valid

    def _get_rotation_coefficients(self) -> Dict[Sequence[int], float]:
        """Compute the coefficient of each monomial.

        Returns:
            A dictionary with pairs ``{control_state: rotation angle}`` where ``control_state``
            is a tuple of ``0`` or ``1`` bits.
        """
        # determine the control states
        all_combinations = list(product([0, 1], repeat=self.num_state_qubits))
        valid_combinations = []
        for combination in all_combinations:
            if 0 < sum(combination) <= self.degree:
                valid_combinations += [combination]

        rotation_coeffs = {control_state: 0 for control_state in valid_combinations}

        # compute the coefficients for the control states
        for i, coeff in enumerate(self.coeffs[1:]):
            i += 1  # since we skip the first element we need to increase i by one

            # iterate over the multinomial coefficients
            for comb, num_combs in multinomial_coefficients(self.num_state_qubits, i).items():
                control_state = ()
                power = 1
                for j, qubit in enumerate(comb):
                    if qubit > 0:  # means we control on qubit i
                        control_state += (1,)
                        power *= 2 ** (j * qubit)
                    else:
                        control_state += (0,)

                # Add angle
                rotation_coeffs[control_state] += coeff * num_combs * power

        return rotation_coeffs

    def _build(self):
        super()._build()

        qr_state = self.qubits[:self.num_state_qubits]
        qr_target = self.qubits[self.num_state_qubits]
        qr_ancilla = self.qubits[self.num_state_qubits + 1:]

        rotation_coeffs = self._get_rotation_coefficients()

        if self.basis == 'x':
            self.rx(self.coeffs[0], qr_target)
        elif self.basis == 'y':
            self.ry(self.coeffs[0], qr_target)
        else:
            self.rz(self.coeffs[0], qr_target)

        for c in rotation_coeffs:
            qr_control = []
            if self.reverse:
                for i, _ in enumerate(c):
                    if c[i] > 0:
                        qr_control.append(qr_state[qr_state.size - i - 1])
            else:
                for i, _ in enumerate(c):
                    if c[i] > 0:
                        qr_control.append(qr_state[i])

            # apply controlled rotations
            if len(qr_control) > 1:
                if self.basis == 'x':
                    self.mcrx(rotation_coeffs[c], qr_control, qr_target, qr_ancilla)
                elif self.basis == 'y':
                    self.mcry(rotation_coeffs[c], qr_control, qr_target, qr_ancilla)
                else:
                    self.mcrz(rotation_coeffs[c], qr_control, qr_target, qr_ancilla)

            elif len(qr_control) == 1:
                if self.basis == 'x':
                    self.crx(rotation_coeffs[c], qr_control[0], qr_target)
                elif self.basis == 'y':
                    self.cry(rotation_coeffs[c], qr_control[0], qr_target)
                else:
                    self.crz(rotation_coeffs[c], qr_control[0], qr_target)
