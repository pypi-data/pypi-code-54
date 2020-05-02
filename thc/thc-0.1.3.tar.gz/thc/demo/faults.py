import random
from .. import THC
from ..utils import prime
from ..crypto.trivial import Trivial
from ..crypto.rsa import RSA
from ..crypto.paillier import Paillier
from ..crypto.he1 import HE1
from ._computations import Product, RandomPolynomial

if __name__ ==  '__main__':

    ### Trivial

    p = prime(512)
    q = prime(512)
    r = prime(32)
    nums = random.sample(range(2**8), 5)
    rp = RandomPolynomial(5, 2**8)

    print('p =', p)
    print('q =', q)
    print('r =', r)
    print('random numbers =', nums)
    print('random polynomial P(x) =', rp)

    print('')

    thc = THC(Trivial(m=p), rp, r)
    print('> P in F_p:')
    for n in nums:
        print('P(' + str(n) + ') =', thc.compute([n]))

    print('')

    ### RSA

    thc = THC(RSA(p=p, q=q, e=(1<<16)+1), Product(), r)
    print('> Multiplications with RSA:')
    print(' * '.join([str(n) for n in nums]) + ' =', thc.compute(nums))

    print('')

    ### Paillier

    thc = THC(Paillier(p=p, q=q), Product(), r)
    print('> Additions with Paillier:')
    print(' + '.join([str(n) for n in nums]) + ' =', thc.compute(nums))

    print('')

    ### HE1

    thc = THC(HE1(p=p, q=q), rp, r)
    print('> P with HE1:')
    for n in nums:
        print('P(' + str(n) + ') =', thc.compute([n]))
