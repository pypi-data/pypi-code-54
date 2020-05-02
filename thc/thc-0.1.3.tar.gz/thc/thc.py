###
### Trustable Homomorphic Computation
###

class THC:

    def __init__ (self, hc, comp, modext_param):
        self._hc = hc
        self._comp = comp
        self._orig_mod = hc.get_modulus()
        self._modext_param = modext_param
        self._mod = self._orig_mod * self._modext_param

    def compute (self, args):
        args_enc = [self._hc.encrypt(a) % self._mod for a in args]
        args_residue = [a % self._modext_param for a in args_enc]
        result_enc = self._comp.remote(self._mod, args_enc)
        return self.verify(result_enc, args_residue)

    def verify (self, result_enc, args):
        result_residue = self._comp.local(self._modext_param, args)
        if result_residue == result_enc % self._modext_param:
            return self._hc.decrypt(result_enc % self._orig_mod)
        return False
