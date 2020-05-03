###
### Trustable Homomorphic Computation
###

class THC:

    def __init__ (self, hc, comp, modext_param):
        self._hc = hc
        self._comp = comp
        self._m = hc.get_modulus()
        self._r = modext_param
        self._mr = self._m * self._r

    def compute (self, args):
        args_enc = [self._hc.mod(self._hc.encrypt(a), self._mr) for a in args]
        args_residue = [self._hc.mod(a, self._r) for a in args_enc]
        result_enc = self._comp.remote(self._mr, args_enc)
        return self.verify(result_enc, args_residue)

    def verify (self, result_enc, args):
        result_residue = self._comp.local(self._r, args)
        if result_residue == self._hc.mod(result_enc, self._r):
            return self._hc.decrypt(self._hc.mod(result_enc, self._m))
        return False
