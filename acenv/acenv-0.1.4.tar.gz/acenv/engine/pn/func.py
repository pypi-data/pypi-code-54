
# Imports
from math import gcd
from functools import reduce
from typing import List, Dict


def GCD(int_list: List[int]) -> int:
    x = reduce(gcd, int_list)
    return x


def LCM(int_list: List[int]) -> int:
    lcm = int_list[0]
    for i in int_list[1:]:
        lcm = int(lcm * i / gcd(lcm, i))
    return int(lcm)


def integer_factorization(n: int):
    prime_fac, factorization = [], {}
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            prime_fac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
        prime_fac.append(n)
    for n in set(prime_fac):
        factorization[n] = prime_fac.count(n)
    return factorization


def build_from_factorization(factorization: Dict):
    n = 1
    for factor in factorization:
        n *= (factor ** factorization[factor])
    return n


def radical_integer_reduction(num: int, index):
    prime_factors, ra, ir = integer_factorization(num), 1, num
    for factor in prime_factors:
        if prime_factors[factor] >= index:
            while prime_factors[factor] >= index:
                ra *= int(factor)
                ir //= int(factor ** index)
                prime_factors[factor] -= index
    return ra, ir


# used in every data_parsing method
def remove_none_from_list(l: list) -> list:
    return [item for item in l if item]


def char_indexes(s: str, char: str) -> list:
    assert len(char) == 1
    return [index for index in range(len(s)) if s[index] == char]
