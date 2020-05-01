from Crypto.Util.number import getPrime, getStrongPrime

###
### Utils
###

def Prime (bits):
    if bits >= 512 and bits % 128 == 0:
        return getStrongPrime(bits)
    return getPrime(bits)

class Mod:

    def __init__ (self, m):
        self._mod = m

    def inv (self, a):
        prev_r, r = abs(a), abs(self._mod)
        x, prev_x, y, prev_y = 0, 1, 1, 0
        while r:
            prev_r, (q, r) = r, divmod(prev_r, r)
            x, prev_x = prev_x - q * x, x
            y, prev_y = prev_y - q * y, y
        x = prev_x * (-1 if a < 0 else 1)
        y = prev_y * (-1 if self._mod < 0 else 1)
        if prev_r != 1:
            raise ValueError
        return x % self._mod

    def exp (self, b, e):
        res = 1
        b = b % self._mod
        while e != 0:
            if e & 1 == 1:
                res = (res * b) % self._mod
            b = (b * b) % self._mod
            e >>= 1
        return res
