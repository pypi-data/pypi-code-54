from ..interfaces import HomomorphicCryptosystem
from ..utils import Mod

class RSA (HomomorphicCryptosystem):

    def __init__ (self, **kwargs):
        self._p = kwargs['p']
        self._q = kwargs['q']

        self._N = self._p * self._q

        self._e = kwargs['e']

        self._d = Mod((self._p - 1) * (self._q - 1)).inv(self._e)

    def get_modulus (self):
        return self._N

    def encrypt (self, m):
        return Mod(self._N).exp(m, self._e)

    def decrypt (self, c):
        return Mod(self._N).exp(c, self._d)
