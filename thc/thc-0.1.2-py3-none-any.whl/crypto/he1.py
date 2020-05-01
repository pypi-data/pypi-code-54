import random
from ..interfaces import HomomorphicCryptosystem

class HE1 (HomomorphicCryptosystem):

    def __init__ (self, **kwargs):
        self._p = kwargs['p']
        self._q = kwargs['q']
        self._mod = self._p * self._q

    def get_modulus (self):
        return self._mod

    def encrypt (self, m):
        r = random.randint(1, self._q)
        return (m + self._p * r) % self._mod

    def decrypt (self, c):
        return c % self._p

    # Gives the desired size of q in bits given the size of p in bits.
    @staticmethod
    def eta (lam):
        return lam ** 2 // 32 - lam
