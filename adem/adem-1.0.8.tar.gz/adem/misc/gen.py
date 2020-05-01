
from . import *

from adem.fundamentals.primary import Num

def whole(lst):
    den = [Fraction(lsts).limit_denominator().denominator for lsts in lst]
    return [lsts * Num(den).LCM() for lsts in lst]
def intable(num):
    try:
        return True if int(float(num)) == float(num) else False
    except Exception:
        return False
def con(dic):
    res = ''
    for key, value in dic.items():
        res += f'{key}^{value}'
    return res
