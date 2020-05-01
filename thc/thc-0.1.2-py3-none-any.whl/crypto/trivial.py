from ..interfaces import HomomorphicCryptosystem

class Trivial (HomomorphicCryptosystem):

    def __init__ (self, **kwargs):
        self._mod = kwargs['m']

    def get_modulus (self):
        return self._mod

    def encrypt (self, m):
        return m % self._mod

    def decrypt (self, c):
        return c % self._mod
