import random
from ..interfaces import *
from ..utils import Mod

from functools import reduce
from operator import mul

class Paillier (HomomorphicCryptosystem):

    def __init__ (self, **kwargs):
        self._p = kwargs['p']
        self._q = kwargs['q']

        self._N = self._p * self._q
        self._Nsqr = self._N * self._N
        self._phi_N = (self._p - 1) * (self._q - 1)
        self._g = self._N + 1

        self._lambda = self._phi_N
        self._mu = Mod(self._N).inv(self._phi_N)

    def get_modulus (self):
        return self._N * self._N

    def encrypt (self, m):
        r = random.randint(0, self._N)
        N2 = Mod(self._Nsqr)
        return N2.exp(self._g, m) * N2.exp(r, self._N) % self._Nsqr

    def decrypt (self, c):
        L = (Mod(self._N * self._N).exp(c, self._lambda) - 1) // self._N
        return L * self._mu % self._N

class Sum (Computation):

    def local (self, mod, args):
        return reduce(mul, args) % mod

    def remote (self, mod, args):
        pass

class Product (Computation):

    def local (self, mod, args):
        return (args[0] ** args[1]) % mod

    def remote (self, mod, args):
        pass
