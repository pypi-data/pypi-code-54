from abc import *

###
### Interfaces
###

class HomomorphicCryptosystem (ABC):

    @abstractmethod
    def __init__ (self, **kwargs):
        pass

    @abstractmethod
    def get_modulus (self):
        pass

    @abstractmethod
    def encrypt (self, m):
        pass

    @abstractmethod
    def decrypt (self, c):
        pass

class Computation (ABC):

    @abstractmethod
    def local (self, mod, args):
        pass

    @abstractmethod
    def remote (self, mod, args):
        pass
