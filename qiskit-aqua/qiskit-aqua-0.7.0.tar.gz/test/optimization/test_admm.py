# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests of the ADMM algorithm."""
from test.optimization import QiskitOptimizationTestCase

import numpy as np
from docplex.mp.model import Model
from qiskit.aqua.algorithms import NumPyMinimumEigensolver
from qiskit.optimization.algorithms import CplexOptimizer, MinimumEigenOptimizer
from qiskit.optimization.algorithms.admm_optimizer import ADMMOptimizer, ADMMParameters, \
    ADMMOptimizationResult, ADMMState
from qiskit.optimization.problems import QuadraticProgram


class TestADMMOptimizer(QiskitOptimizationTestCase):
    """ADMM Optimizer Tests"""

    def test_admm_maximization(self):
        """Tests a simple maximization problem using ADMM optimizer"""
        try:
            mdl = Model('simple-max')
            c = mdl.continuous_var(lb=0, ub=10, name='c')
            x = mdl.binary_var(name='x')
            mdl.maximize(c + x * x)
            op = QuadraticProgram()
            op.from_docplex(mdl)

            admm_params = ADMMParameters()

            qubo_optimizer = MinimumEigenOptimizer(NumPyMinimumEigensolver())
            # qubo_optimizer = CplexOptimizer()
            continuous_optimizer = CplexOptimizer()

            solver = ADMMOptimizer(qubo_optimizer=qubo_optimizer,
                                   continuous_optimizer=continuous_optimizer,
                                   params=admm_params)
            solution: ADMMOptimizationResult = solver.solve(op)
            self.assertIsNotNone(solution)
            self.assertIsInstance(solution, ADMMOptimizationResult)

            self.assertIsNotNone(solution.x)
            np.testing.assert_almost_equal([10, 0], solution.x, 3)
            self.assertIsNotNone(solution.fval)
            np.testing.assert_almost_equal(10, solution.fval, 3)
            self.assertIsNotNone(solution.state)
            self.assertIsInstance(solution.state, ADMMState)
        except NameError as ex:
            self.skipTest(str(ex))

    def test_admm_ex4(self):
        """Example 4 as a unit test. Example 4 is reported in:
        Gambella, C., & Simonetto, A. (2020).
        Multi-block ADMM Heuristics for Mixed-Binary Optimization on Classical
        and Quantum Computers.
        arXiv preprint arXiv:2001.02069."""
        try:
            mdl = Model('ex4')

            v = mdl.binary_var(name='v')
            w = mdl.binary_var(name='w')
            # pylint:disable=invalid-name
            t = mdl.binary_var(name='t')

            # b = 1
            b = 2

            mdl.minimize(v + w + t)
            mdl.add_constraint(2 * v + 10 * w + t <= 3, "cons1")
            mdl.add_constraint(v + w + t >= b, "cons2")

            op = QuadraticProgram()
            op.from_docplex(mdl)

            # qubo_optimizer = MinimumEigenOptimizer(NumPyMinimumEigensolver())
            qubo_optimizer = CplexOptimizer()
            continuous_optimizer = CplexOptimizer()

            admm_params = ADMMParameters(
                rho_initial=1001, beta=1000, factor_c=900,
                max_iter=100, three_block=False
            )

            solver = ADMMOptimizer(params=admm_params, qubo_optimizer=qubo_optimizer,
                                   continuous_optimizer=continuous_optimizer, )
            solution = solver.solve(op)
            self.assertIsNotNone(solution)
            self.assertIsInstance(solution, ADMMOptimizationResult)
            self.assertIsNotNone(solution.x)
            np.testing.assert_almost_equal([1., 0., 1.], solution.x, 3)
            self.assertIsNotNone(solution.fval)
            np.testing.assert_almost_equal(2., solution.fval, 3)
            self.assertIsNotNone(solution.state)
            self.assertIsInstance(solution.state, ADMMState)

        except NameError as ex:
            self.skipTest(str(ex))

    def test_admm_ex5(self):
        """Example 5 as a unit test. Example 5 is reported in:
        Gambella, C., & Simonetto, A. (2020).
        Multi-block ADMM Heuristics for Mixed-Binary Optimization on Classical
        and Quantum Computers.
        arXiv preprint arXiv:2001.02069."""
        try:
            mdl = Model('ex5')

            # pylint:disable=invalid-name
            v = mdl.binary_var(name='v')
            w = mdl.binary_var(name='w')
            t = mdl.binary_var(name='t')

            mdl.minimize(v + w + t)
            mdl.add_constraint(2 * v + 2 * w + t <= 3, "cons1")
            mdl.add_constraint(v + w + t >= 1, "cons2")
            mdl.add_constraint(v + w == 1, "cons3")

            op = QuadraticProgram()
            op.from_docplex(mdl)

            qubo_optimizer = CplexOptimizer()

            continuous_optimizer = CplexOptimizer()

            admm_params = ADMMParameters(
                rho_initial=1001, beta=1000, factor_c=900,
                max_iter=100, three_block=False
            )

            solver = ADMMOptimizer(params=admm_params, qubo_optimizer=qubo_optimizer,
                                   continuous_optimizer=continuous_optimizer, )
            solution = solver.solve(op)

            self.assertIsNotNone(solution)
            self.assertIsInstance(solution, ADMMOptimizationResult)
            self.assertIsNotNone(solution.x)
            np.testing.assert_almost_equal([1., 0., 1.], solution.x, 3)
            self.assertIsNotNone(solution.fval)
            np.testing.assert_almost_equal(2., solution.fval, 3)
            self.assertIsNotNone(solution.state)
            self.assertIsInstance(solution.state, ADMMState)
        except NameError as ex:
            self.skipTest(str(ex))

    def test_admm_ex6(self):
        """Example 6 as a unit test. Example 6 is reported in:
        Gambella, C., & Simonetto, A. (2020).
        Multi-block ADMM Heuristics for Mixed-Binary Optimization on Classical
        and Quantum Computers.
        arXiv preprint arXiv:2001.02069."""
        try:
            mdl = Model('ex6')

            # pylint:disable=invalid-name
            v = mdl.binary_var(name='v')
            w = mdl.binary_var(name='w')
            t = mdl.binary_var(name='t')
            u = mdl.continuous_var(name='u')

            mdl.minimize(v + w + t + 5 * (u - 2) ** 2)
            mdl.add_constraint(v + 2 * w + t + u <= 3, "cons1")
            mdl.add_constraint(v + w + t >= 1, "cons2")
            mdl.add_constraint(v + w == 1, "cons3")

            op = QuadraticProgram()
            op.from_docplex(mdl)

            qubo_optimizer = CplexOptimizer()
            continuous_optimizer = CplexOptimizer()

            admm_params = ADMMParameters(
                rho_initial=1001, beta=1000, factor_c=900,
                max_iter=100, three_block=True, tol=1.e-6
            )

            solver = ADMMOptimizer(params=admm_params, qubo_optimizer=qubo_optimizer,
                                   continuous_optimizer=continuous_optimizer)
            solution = solver.solve(op)

            self.assertIsNotNone(solution)
            self.assertIsInstance(solution, ADMMOptimizationResult)
            self.assertIsNotNone(solution.x)
            np.testing.assert_almost_equal([1., 0., 0., 2.], solution.x, 3)
            self.assertIsNotNone(solution.fval)
            np.testing.assert_almost_equal(1., solution.fval, 3)
            self.assertIsNotNone(solution.state)
            self.assertIsInstance(solution.state, ADMMState)
        except NameError as ex:
            self.skipTest(str(ex))

    def test_admm_ex6_max(self):
        """Example 6 as maximization"""
        try:
            mdl = Model('ex6-max')

            # pylint:disable=invalid-name
            v = mdl.binary_var(name='v')
            w = mdl.binary_var(name='w')
            t = mdl.binary_var(name='t')
            u = mdl.continuous_var(name='u')

            # mdl.minimize(v + w + t + 5 * (u - 2) ** 2)
            mdl.maximize(- v - w - t - 5 * (u - 2) ** 2)
            mdl.add_constraint(v + 2 * w + t + u <= 3, "cons1")
            mdl.add_constraint(v + w + t >= 1, "cons2")
            mdl.add_constraint(v + w == 1, "cons3")

            op = QuadraticProgram()
            op.from_docplex(mdl)

            qubo_optimizer = CplexOptimizer()
            continuous_optimizer = CplexOptimizer()

            admm_params = ADMMParameters(
                rho_initial=1001, beta=1000, factor_c=900,
                max_iter=100, three_block=True, tol=1.e-6
            )

            solver = ADMMOptimizer(params=admm_params, qubo_optimizer=qubo_optimizer,
                                   continuous_optimizer=continuous_optimizer)
            solution = solver.solve(op)

            self.assertIsNotNone(solution)
            self.assertIsInstance(solution, ADMMOptimizationResult)
            self.assertIsNotNone(solution.x)
            np.testing.assert_almost_equal([1., 0., 0., 2.], solution.x, 3)
            self.assertIsNotNone(solution.fval)
            np.testing.assert_almost_equal(-1., solution.fval, 3)
            self.assertIsNotNone(solution.state)
            self.assertIsInstance(solution.state, ADMMState)
        except NameError as ex:
            self.skipTest(str(ex))

    def test_equality_constraints_with_continuous_variables(self):
        """Simple example to test equality constraints with continuous variables."""
        try:
            mdl = Model("eq-constraints-cts-vars")

            # pylint:disable=invalid-name
            v = mdl.binary_var(name='v')
            w = mdl.continuous_var(name='w', lb=0.)
            t = mdl.continuous_var(name='t', lb=0.)

            mdl.minimize(v + w + t)
            mdl.add_constraint(2 * v + w >= 2, "cons1")
            mdl.add_constraint(w + t == 1, "cons2")

            op = QuadraticProgram()
            op.from_docplex(mdl)

            # qubo_optimizer = MinimumEigenOptimizer(NumPyMinimumEigensolver())
            qubo_optimizer = CplexOptimizer()

            continuous_optimizer = CplexOptimizer()

            admm_params = ADMMParameters(
                rho_initial=1001, beta=1000, factor_c=900,
                max_iter=100, three_block=True,
            )

            solver = ADMMOptimizer(params=admm_params, qubo_optimizer=qubo_optimizer,
                                   continuous_optimizer=continuous_optimizer, )
            solution = solver.solve(op)

            self.assertIsNotNone(solution)
            self.assertIsInstance(solution, ADMMOptimizationResult)
            self.assertIsNotNone(solution.x)
            np.testing.assert_almost_equal([0., 1., 0.], solution.x, 3)
            self.assertIsNotNone(solution.fval)
            np.testing.assert_almost_equal(1., solution.fval, 3)
            self.assertIsNotNone(solution.state)
            self.assertIsInstance(solution.state, ADMMState)
        except NameError as ex:
            self.skipTest(str(ex))

    def test_quad_constraints(self):
        """Simple example to test quadratic constraints."""

        try:
            mdl = Model('quad-constraints')

            v = mdl.binary_var(name='v')
            w = mdl.continuous_var(name='w', lb=0.)

            mdl.minimize(v + w)
            mdl.add_constraint(v + w >= 1, "cons2")
            mdl.add_constraint(v ** 2 + w ** 2 <= 1, "cons2")

            op = QuadraticProgram()
            op.from_docplex(mdl)

            # qubo_optimizer = MinimumEigenOptimizer(NumPyMinimumEigensolver())
            qubo_optimizer = CplexOptimizer()

            continuous_optimizer = CplexOptimizer()

            admm_params = ADMMParameters(
                rho_initial=1001, beta=1000, factor_c=900,
                max_iter=100, three_block=True,
            )

            solver = ADMMOptimizer(params=admm_params, qubo_optimizer=qubo_optimizer,
                                   continuous_optimizer=continuous_optimizer, )
            solution = solver.solve(op)

            self.assertIsNotNone(solution)
            self.assertIsInstance(solution, ADMMOptimizationResult)
            self.assertIsNotNone(solution.x)
            np.testing.assert_almost_equal([0., 1.], solution.x, 3)
            self.assertIsNotNone(solution.fval)
            np.testing.assert_almost_equal(1., solution.fval, 3)
            self.assertIsNotNone(solution.state)
            self.assertIsInstance(solution.state, ADMMState)

        except NameError as ex:
            self.skipTest(str(ex))
