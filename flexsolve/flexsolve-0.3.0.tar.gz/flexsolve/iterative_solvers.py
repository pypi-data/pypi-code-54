# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:56:59 2020

@author: yoelr
"""
import numpy as np
from collections import deque
from .exceptions import SolverError, InfeasibleRegion
from copy import copy
from numpy import linalg
from . import utils

__all__ = ('fixed_point',
           'conditional_fixed_point',
           'wegstein',
           'conditional_wegstein',
           'aitken',
           'conditional_aitken',
           'LeastSquaresIteration',
           'LstSqIter',
) 


class LeastSquaresIteration:
    __slots__ = ('guess_history', 'error_history', 'N_activate',
                 '_counter', '_b')
    
    def __init__(self, N_history=5, N_activate=20):
        self.guess_history = deque(maxlen=N_history)
        self.error_history = deque(maxlen=N_history)
        self.N_activate = N_activate
        self._counter = 0
        self._b = None

    def __call__(self, x, fx):
        guess_history = self.guess_history
        error_history = self.error_history
        guess_history.append(x)
        error_history.append(fx - x)
        x_guess = None
        if self.active:
            A = np.array(error_history)
            A = A.transpose()
            try:
                weights = linalg.lstsq(A, self._get_b(), None)[0]
                weights /= weights.sum()
            except:
                pass
            else:
                xs = np.array(guess_history).transpose()
                x_guess = xs @ weights
        return x_guess
    
    def reset(self):
        self.guess_history.clear()
        self.error_history.clear()
        self._counter = 0
        self._b = None
    
    @property
    def active(self):
        active = self._counter == self.N_activate
        if not active: self._counter += 1
        return active
    
    def _get_b(self):
        b = self._b
        if b is None:
            self._b = b = 1e-16 * np.ones_like(self.guess_history[0])
        return b

LstSqIter = LeastSquaresIteration

def fake_least_squares(x, fx):
    return fx

def as_least_squares(lstsq):
    if lstsq: 
        if not isinstance(lstsq, LstSqIter):
            lstsq = LstSqIter()
    else:
        lstsq = fake_least_squares
    return lstsq

def fixed_point(f, x, xtol=1e-8, args=(), maxiter=50, lstsq=None):
    """Iterative fixed-point solver. If `lstsq` is True, the least-squares 
    solution of a matrix of prior iterations may be partially used to
    iteratively esmitate the root."""
    lstsq = as_least_squares(lstsq)
    x0 = x1 = x
    for iter in range(maxiter):
        if x0 is None:
            x0 = x1
            x1 = f(x0)
        else:
            try: x1 = f(x0)
            except InfeasibleRegion:
                x0 = x1
                x1 = f(x0)
        if (np.abs(x1 - x0) < xtol).all(): return x1
        x0 = lstsq(x0, x1)
    raise SolverError(maxiter, x1)

def conditional_fixed_point(f, x, lstsq=None):
    """Conditional iterative fixed-point solver. If `lstsq` is True, the
    least-squares solution of a matrix of prior iterations may be partially used
    to iteratively esmitate the root."""
    lstsq = as_least_squares(lstsq)
    x0 = x1 = x
    condition = True
    while condition:
        if x0 is None:
            x0 = x1
            x1, condition = f(x0)
        else:
            try: x1, condition = f(x0)
            except InfeasibleRegion:
                x0 = x1
                x1, condition = f(x0)
        x0 = lstsq(x0, x1)
    return x

def wegstein(f, x, xtol=1e-8, args=(), maxiter=50):
    """Iterative Wegstein solver."""
    x0 = x
    x1 = g0 = f(x0, *args)
    wegstein_iter = utils.get_wegstein_iter_function(x)
    for iter in range(maxiter):
        dx = x1-x0
        try: g1 = f(x1, *args)
        except InfeasibleRegion:
            x1 = g0
            g1 = f(x1, *args)
        if (np.abs(g1-x1) < xtol).all(): return g1
        x0 = x1
        x1 = wegstein_iter(x1, dx, g1, g0)
        g0 = g1
    raise SolverError(maxiter, g1)

def conditional_wegstein(f, x):
    """Conditional iterative Wegstein solver."""
    x0 = x
    g0, condition = f(x0)
    g1 = x1 = g0
    wegstein_iter = utils.get_wegstein_iter_function(x)
    while condition:
        try: g1, condition = f(x1)
        except InfeasibleRegion:
            x1 = g1
            g1, condition = f(x1)
        g1 = g1
        dx = x1-x0
        x0 = x1
        x1 = wegstein_iter(x1, dx, g1, g0)
        g0 = g1

def aitken(f, x, xtol=1e-8, args=(), maxiter=50):
    """Iterative Aitken solver."""
    gg = x
    x = copy(x)
    aitken_iter = utils.get_aitken_iter_function(x)
    for iter in range(maxiter):
        try: g = f(x, *args)
        except InfeasibleRegion:
            x = gg.copy()
            g = f(x, *args)
        dxg = x - g
        if (np.abs(dxg) < xtol).all(): return g
        gg = f(g, *args)
        dgg_g = gg - g
        if (np.abs(dgg_g) < xtol).all(): return gg
        x = aitken_iter(x, gg, dxg, dgg_g)
    raise SolverError(maxiter, gg)
    
def conditional_aitken(f, x):
    """Conditional iterative Aitken solver."""
    condition = True
    x = copy(x)
    gg = x
    aitken_iter = utils.get_aitken_iter_function(x)
    while condition:
        try:
            g, condition = f(x)
        except InfeasibleRegion:
            x = gg.copy()
            g, condition = f(x)
        if not condition: return g
        gg, condition = f(g)
        x = aitken_iter(x, gg, x - g, gg - g)