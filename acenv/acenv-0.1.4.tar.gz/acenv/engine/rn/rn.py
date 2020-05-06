"""
Real numbers exact representation module

Getting various functions from func.py

classes to be defined:
    Ra, Ir (rational and irrational objects)
    RNU (Real Number Unit)
    LRN (Linear real number)
    RN (actual real number)

    _Lcl (local useful methods)
    Errors (local mathematical errors)
"""


from sys import version
from fractions import Fraction
from decimal import Decimal
from typing import Any, Callable
from functools import reduce
from .func import integer_factorization, GCD, LCM, \
    build_from_factorization, remove_none_from_list, radical_integer_reduction

__author__ = 'Viganò Andrea'
__version__ = 'rn module 1.7 for ACE 0.1.0 official release for Python {}'.format(version)


# Local errors class
class Error:
    class ArgumentError(Exception):
        pass

    @staticmethod
    def raise_argument_error(cls: str, arg_name: str, possible_arg: list, arg: Any):
        raise Error.ArgumentError('Bad user argument, must be either {} for {} parameter in {} class, got {}'.format(
            possible_arg, arg_name, cls, type(arg)
        ))

    class MissingImplementationError(Exception):
        pass

    class InvalidRootError(Exception):
        pass

    class OperationError(Exception):
        pass

    @staticmethod
    def raise_operation_error(operation: str, a: Any, b: Any):
        raise Error.OperationError('Unable to operate {} with {} and {} instances'.format(operation, type(a), type(b)))


# Operations / Comparisons decorator
def assert_other(func: Callable) -> Callable:
    def wrapper(self: Any, other: Any) -> Any:
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            return NotImplemented
        return func(self, other)

    return wrapper


def assert_rn_other(func: Callable) -> Callable:
    def wrapper(self: Any, other: Any) -> Any:
        try:
            assert any(isinstance(other, tp) for tp in [RN, LRN, RNU, int, float, Fraction, Decimal])
        except AssertionError:
            Error.raise_operation_error(func.__name__, self, other)
        return func(self, other)

    return wrapper


# Local methods
class _Lcl:
    @staticmethod
    def convert_to_fraction(value: Fraction or int or float or Decimal) -> Fraction or None:
        if isinstance(value, Fraction):
            return value
        elif isinstance(value, int):
            return Fraction(value)
        elif isinstance(value, float):
            return Fraction.from_float(value)
        elif isinstance(value, Decimal):
            return Fraction.from_decimal(value)
        return ''

    @staticmethod
    def validate_irrational_instance(value: Fraction, index: Fraction):
        # rational or negative index
        if not index.denominator == 1:
            raise Error.MissingImplementationError('Got {} as root index, Non-integer indexes are yet to be implemented'
                                                   .format(str(index)))
        elif index == 0:
            raise Error.InvalidRootError('A root with index 0 has no meaning')
        elif index < 0:
            raise Error.MissingImplementationError('Got {} as root index, Negative indexes are yet to be implemented'
                                                   .format(str(index)))
        # even index and negative value
        if not index % 2 and value < 0:
            raise Error.InvalidRootError('Got {} as value of an even-index root'.format(str(value)))

    @staticmethod
    def ir_str(value, index):
        # if index == 2 -> √value
        if index == 2:
            return '√' + str(value)
        else:
            return '[' + str(index) + ']√' + str(value)

    @staticmethod
    def _get_fraction_data(string):
        num, den = 0, 1
        if '/' in string:
            num, den = string.split('/')
        elif '.' in string:
            num = float(string)
            while int(num) != num:
                num *= 10
                den *= 10
        else:
            num = int(string)
        return Fraction(int(num), int(den))

    @staticmethod
    def parse_rnu_string(string: str):
        """
        get string representation of and RNU instance and return Ra and Ir objects
        -> string should be like:
            -> rational: 3, -4, 3/2, -4/5, 7.09, +6, -8.5
            -> irrational: √2, [5]√-8, [6]√5/3, [3]√-7.53
        """
        # if unit contains an irrational part -> contains '√'
        if '√' in string:
            # irrational or mix
            data = string.split('[')
            # data is [rational string, index string + ']√' +  radicand string] if index is not 2
            # else -> [string]
            if len(data) != 1:
                ra, index, value = data[0], data[1].split(']')[0], data[1].split('√')[1]
            # else index = 2
            else:
                data = string.split('√')
                ra, index, value = data[0], 2, data[1]
            return Ra(_Lcl._get_fraction_data(ra) if ra else 1), Ir(_Lcl._get_fraction_data(value), float(index))
        else:
            # only rational
            return Ra(_Lcl._get_fraction_data(string)), Ir(1, 1)

    @staticmethod
    def parse_rnu_data(ra, ir):
        """
        get ra and ir to be written in canonic form:
            -> rationalize
            -> bring negative sign out of the root
            -> reduce radical
        """
        assert isinstance(ra, Ra) and isinstance(ir, Ir)
        # mutable values (can't set attributes for Fraction class)
        i_num, i_den = ir.value.numerator, ir.value.denominator
        r_num, r_den = ra.value.numerator, ra.value.denominator
        index = ir.index.numerator
        # rationalize
        # -> get denominator of ir to be 1
        # -> multiply ra.denominator for ir.denominator
        # -> multiply ir.numerator for ir.denominator elevated to the power of (index - 1)
        # -> ir.denominator will always be equal to ONE
        if i_den != 1:
            r_den, i_num = r_den * i_den, i_num * int(i_den ** (index - 1))
        # if ir < 0 (it means that index must be odd) -> bring sign out of the root
        # -> multiply ra.numerator and ir.numerator for -1
        if i_num < 0:
            r_num, i_num = r_num * -1, i_num * -1
        i = i_num
        # radical reduction
        # -> factorize i
        factorization = integer_factorization(i)
        # -> loop through every item in factorization and decide if it can be reduced
        #    -> if the exponent of the prime factor if ge that the index
        #       -> will bring factor out of the root and leave factor ** (exp - index) in
        for prime_factor in factorization:
            if factorization[prime_factor] >= index:
                factorization[prime_factor] -= index
                r_num *= int(prime_factor)
        # reset
        # if i is equal to zero, must not use build... function, as it will return 1 if empty dict is passed,
        # but both ONE and ZERO have a factorization equal to an empty dict...
        i = build_from_factorization(factorization) if i else 0
        # get GCD of every exp of factorization and index
        # -> if GCD is greater than ONE
        #    -> divide index and every exp for GCD
        gcd = GCD([index] + [factorization[factor] for factor in factorization])
        if gcd > 1:
            index //= gcd
            for factor in factorization:
                factorization[factor] //= gcd
        # if i is equal to zero, must not use build... function, as it will return 1 if empty dict is passed,
        # but both ONE and ZERO have a factorization equal to an empty dict...
        i = build_from_factorization(factorization) if i else 0
        # bring factors out of the root
        _r_num, i = radical_integer_reduction(i, index)
        r_num *= _r_num
        # parse any eventual particular case
        # -> index = 1 then r_num *= i, i = 1
        if index == 1:
            index = 1
            r_num *= i
            i = 1
        # -> i = 1 then index = 1
        if i == 1:
            index = 1
        # -> i = 0 then index = 1, i = 1
        # -> r_num = 0 then index = 1, i = 1
        if i == 0 or r_num == 0:
            index, i = 1, 1
            r_num = 0
        return Ra(Fraction(r_num, r_den)), Ir(Fraction(i, 1), Fraction(index))

    @staticmethod
    def rnu_str(rational, irrational):
        # if not irrational -> ra
        if irrational == Ir(1, 1):
            return str(rational)
        # if rational == 1 -> ir
        if rational == Ra(1):
            return '+' + str(irrational)
        if rational == Ra(-1):
            return '-' + str(irrational)
        else:
            return str(rational) + str(irrational)

    @staticmethod
    def parse_lin_rn_data(units: list):
        """
        simplify units if possible:
        -> sort units list (must have specific comparision functions to pass as key parameters)
        -> sum units near to each other if possible (must set up __gt__ method to RNU class)
        -> sum is possible only if it will return a RNU-representable number
        """
        assert all(isinstance(i, RNU) for i in units)
        # sort units
        units.sort()
        # loop through units and check if near items are compatible -> must set up compatibility checker for RNU objects
        for p, unit in enumerate(units):
            try:
                if unit.is_compatible(units[p + 1]):
                    units[p + 1] += unit
                    units[p] = None
            except IndexError:
                continue
        return remove_none_from_list(units)

    @staticmethod
    def _validate_rn_argument(arg):
        # either num or den
        if isinstance(arg, LRN):
            return arg
        elif isinstance(arg, RNU):
            return LRN([arg])
        elif any(isinstance(arg, tp) for tp in [int, float, Fraction, Decimal]):
            return LRN([RNU(Ra(arg), Ir(1, 1))])
        return ''

    @staticmethod
    def validate_rn(num, den):
        return _Lcl._validate_rn_argument(num), _Lcl._validate_rn_argument(den)

    @staticmethod
    def rationals_reduction(num, den):
        # rationals reduction
        # get GCD of rationals part
        ra_integers = [unit.ra.value.numerator for unit in num.units + den.units]
        ra_GCD = GCD(ra_integers)
        # proceed to reduction if GCD is not one
        if ra_GCD != 1:
            num, den = LRN(list(RNU(Ra(unit.ra.value.numerator / ra_GCD), unit.ir) for unit in num.units)), \
                       LRN(list(RNU(Ra(unit.ra.value.numerator / ra_GCD), unit.ir) for unit in den.units))
        return num, den

    @staticmethod
    def irrationals_reduction(num, den):
        # irrational reduction
        # proceed if all units are irrational and they have the same index
        if all(not unit.is_rational for unit in num.units + den.units) and \
                reduce(lambda a, b: b if a.ir.index == b.ir.index else RNU(s='1'), num.units + den.units):
            # get GCD of irrational parts
            ir_integers = [unit.ir.value.numerator for unit in num.units + den.units]
            ir_GCD = GCD(ir_integers)
            # proceed to reduction if GCD is not one
            if ir_GCD != 1:
                num, den = LRN(list(RNU(unit.ra, Ir(unit.ir.value.numerator / ir_GCD, unit.ir.index))
                                    for unit in num.units)), LRN(list(RNU(unit.ra, Ir(unit.ir.value.numerator / ir_GCD,
                                                                                      unit.ir.index)) for unit in
                                                                      den.units))
        return num, den

    @staticmethod
    def num_den_reduction(num, den):
        num, den = _Lcl.rationals_reduction(num, den)
        num, den = _Lcl.irrationals_reduction(num, den)
        return num, den

    @staticmethod
    def parse_rn_data(num, den):
        """
        RN parsing:
        -> reduce denominators in num and den units
        -> get LCM of all the denominators (of num and den)
        -> replace each unit of num and den with the product of the numerator and the quotient of the LCM and the
           denominator
        -> get denominators LCM for num and den
        -> get a factor for each unit for num and den with LCM / denominator of the unit
        -> get reduced num and den by multiplying each unit for its factor and for the LCM for the other element

        -> get GCD of num and den, as num and den rational parts must be integers
        -> get Ra elements of each unit in num and den
        -> get GCD of all of them
        -> divide each unit for that GCD

        -> check if there is a GCD of the irrational parts
        -> check if all unit are irrational
        -> check if they all have the same index
        -> check if the ir values have a GCD
        -> divide every ir value for that GCD

        -> rationalize whenever possible
            -> single IR unit in denominator
            -> sum / difference of two square roots
            -> any other case: leave as it is

        -> move negative sign to the numerator
        """
        assert isinstance(num, LRN) and isinstance(den, LRN)
        # reduce num and den units denominators
        # get LCM of num and den denominators
        ra_LCM = LCM([unit.ra.value.denominator for unit in num.units + den.units])
        # replace each unit with its simplification
        num = LRN(list(RNU(Ra(unit.ra.value.numerator * (ra_LCM // unit.ra.value.denominator)), unit.ir)
                       for unit in num.units))
        den = LRN(list(RNU(Ra(unit.ra.value.numerator * (ra_LCM // unit.ra.value.denominator)), unit.ir)
                       for unit in den.units))
        # assert reduction has gone as expected
        assert all(unit.ra.value.denominator == 1 for unit in num.units + den.units)
        # rationals and irrationals reduction -> only done after every parsing and just before returning
        # num, den = _Lcl.num_den_reduction(num, den)
        _num, _den = num, den
        # rationalize
        # case 1: single ir unit in denominator
        # -> multiply numerator for den.units[0] ** (its index - 1)
        # -> replace denominator with den ** (its index)
        # IF IN TESTING THIS DOES NOT WORK, REPLACE WITH PURE RATIONALIZATION PROCESS...
        if len(den.units) == 1 and not den.units[0].is_rational:
            factor = LRN([RNU(Ra(den.units[0].ir.index - 1), Ir(1, 1))])
            _den = den ** factor
            _num = num * _den
            _den = den ** (factor + LRN([RNU(s='1')]))
        # case 2: sum / difference of two square roots
        # -> get the values of the two units and build a LRN from the first one and the second with changed sign
        elif len(den.units) == 2 and all(not unit.is_rational for unit in den.units) and \
                all(unit.ir.index == 2 for unit in den.units):
            factor = LRN([den.units[0], -den.units[1]])
            _num = num * factor
            _den = den * factor
        # move negative sign to the numerator
        num, den = _num, _den
        if den < LRN([RNU(s='0')]):
            num *= LRN([RNU(s='-1')])
            den *= LRN([RNU(s='-1')])
        # reduce num and den
        return _Lcl.num_den_reduction(num, den)

    @staticmethod
    def is_integer(fr: Fraction):
        if not isinstance(fr, Fraction):
            raise Error.ArgumentError('Bad user argument, must be Fraction for _Lcl.is_integer')
        return fr.denominator == 1

    @staticmethod
    def mutual(a):
        assert isinstance(a, Ra) or isinstance(a, Ir)
        if not a:
            raise ZeroDivisionError('Impossible to divide by zero, unable to get mutual of {}'.format(str(a)))
        if isinstance(a, Ra):
            return Ra(Fraction(a.value.denominator, a.value.numerator))
        elif isinstance(a, Ir):
            return Ir(Fraction(a.value.denominator, a.value.numerator), a.index)

    @staticmethod
    def rn_str(numerator, denominator):
        # return readable string of num / den
        # if den == 1 -> num
        if denominator == LRN([RNU(s='1')]):
            return str(numerator)
        # if num == 0 -> 0
        if not numerator:
            return '0'
        else:
            return str(numerator) + '/' + str(denominator)

    @staticmethod
    def validate_limits(lower_limit, upper_limit):
        if not any(isinstance(upper_limit, tp) for tp in [RN, LRN, RNU, int, float, Fraction, Decimal]):
            Error.raise_argument_error('SI', 'upper limit',
                                       [RN, LRN, RNU, int, float, Fraction, Decimal], upper_limit)
        if not any(isinstance(lower_limit, tp) for tp in [RN, LRN, RNU, int, float, Fraction, Decimal]):
            Error.raise_argument_error('SI', 'lower limit',
                                       [RN, LRN, RNU, int, float, Fraction, Decimal], lower_limit)
        if any(isinstance(upper_limit, tp) for tp in [LRN, RNU]):
            upper_limit = RN(upper_limit)
        if any(isinstance(lower_limit, tp) for tp in [LRN, RNU]):
            lower_limit = RN(lower_limit)
        if upper_limit < lower_limit:
            raise Error.ArgumentError('Invalid limits for SI class, upper limit cannot be grater than lower limit')

    @staticmethod
    def validate_equals(lower_equal, upper_equal):
        if not isinstance(lower_equal, bool) or not isinstance(upper_equal, bool):
            raise Error.ArgumentError('Invalid equals for SI class, lower equal and upper equal must be bool')

    @staticmethod
    def validate_int_units(units: list) -> None:
        if not isinstance(units, list):
            Error.raise_argument_error('Interval', 'units', [list], units)
        for unit in units:
            if not isinstance(unit, SI):
                Error.ArgumentError('Bad user argument, each item in units list of class Interval must be SI object, '
                                    'got {}'.format(type(unit)))

    @staticmethod
    def parse_int_units(units: list) -> list:
        # reduce units -> check for intersections between units
        # -> sort list (order by size of their lower limit)
        units.sort()
        for p, unit in enumerate(units):
            try:
                if unit.intersect(units[p + 1]):
                    units[p + 1] = unit | units[p + 1]
                    units[p] = None
            except IndexError:
                continue
        return remove_none_from_list(units)


class Ra:
    """
    rational entity
    """

    def __init__(self, value):
        self.value = _Lcl.convert_to_fraction(value)
        # cannot use None value because self.value could be Fraction(0) and would raise an error
        if self.value == '':
            Error.raise_argument_error(self.__class__.__name__, 'value', [int, float, Fraction, Decimal], value)

    def __str__(self):
        return str(self.value) if self.value < 0 else '+' + str(self.value)

    def __repr__(self):
        return 'Ra(Fraction(' + str(self.value.numerator) + ', ' + str(self.value.denominator) + '))'

    # enable conversion to float
    def __float__(self):
        return float(self.value)

    __eq__ = assert_other(lambda a, b: a.value == b.value)
    __bool__ = lambda a: a.value != 0

    # get RNU to be sortable
    __gt__ = assert_other(lambda a, b: a.value > b.value)

    # operations
    __neg__ = lambda a: Ra(-a.value)
    mutual = _Lcl.mutual
    __mul__ = assert_other(lambda a, b: Ra(a.value * b.value))


class Ir:
    """
    irrational entity
    Existence conditions needed
    """

    def __init__(self, value, index):
        self.value = _Lcl.convert_to_fraction(value)
        # cannot use None value because self.value could be Fraction(0) and would raise an error
        if self.value == '':
            Error.raise_argument_error(self.__class__.__name__, 'value', [int, float, Fraction, Decimal], value)
        self.index = _Lcl.convert_to_fraction(index)
        if self.value == '':
            Error.raise_argument_error(self.__class__.__name__, 'index', [int, float, Fraction, Decimal], value)
        # assert instance can exist
        _Lcl.validate_irrational_instance(self.value, self.index)

    def __str__(self):
        return _Lcl.ir_str(self.value, self.index)

    def __repr__(self):
        return 'Ir(Fraction(' + str(self.value.numerator) + ', ' + str(self.value.denominator) + '), Fraction(' + \
               str(self.index.numerator) + '))'

    # enable conversion to float
    def __float__(self):
        # if self.value is negative -> could get complex because of floating point imprecision
        # when the result of a root is a complex number, its distance from the origin (its module) is equal to the
        # value we were be getting if the operations were exact
        rv = self.value ** (self.index ** -1)
        if isinstance(rv, complex):
            # self.value must be negative
            rv = -abs(rv)
        return float(rv)

    # get RNU objects to be sortable
    # get RNU objects to be compatibility check-able
    __eq__ = assert_other(lambda a, b: a.index == b.index and a.value == b.value)

    @assert_other
    def __gt__(self, other):
        if self.index == other.index:
            return self.value > other.value
        return self.index > other.index

    # operations
    mutual = _Lcl.mutual

    @assert_other
    def __mul__(self, other):
        # index is always an integer, but it is a Fraction object
        lcm = LCM([self.index.numerator, other.index.numerator])
        if not lcm:
            raise Error.ArgumentError('Unable to multiply {} and {}'.format(str(self), str(other)))
        return Ir((self.value ** (lcm // self.index)) * (other.value ** (lcm // other.index)), lcm)


class RNU:
    """
    Real Number Unit
    At this level are the first reduction methods (parse_rnu_data)
    """

    def __init__(self, ra=Ra(1), ir=Ir(1, 1), s=''):
        if not isinstance(ra, Ra):
            Error.raise_argument_error(self.__class__.__name__, 'ra', [Ra], ra)
        if not isinstance(ir, Ir):
            Error.raise_argument_error(self.__class__.__name__, 'ir', [Ir], ir)
        if s != '':
            # rnu repr string passed
            if ra != Ra(1) or ir != Ir(1, 1):
                raise Error.ArgumentError('Cannot pass ra, ir and string as RNU class arguments, must be one of them')
            ra, ir = _Lcl.parse_rnu_string(s)
        self.ra, self.ir = _Lcl.parse_rnu_data(ra, ir)

    def __str__(self):
        return _Lcl.rnu_str(self.ra, self.ir)

    def __repr__(self):
        return 'RNU(' + repr(self.ra) + ', ' + repr(self.ir) + ')'

    def __hash__(self):
        return 0

    # properties
    @property
    def is_rational(self):
        """irrational part equal to one"""
        return self.ir.value == 1

    @property
    def is_integer(self):
        """is rational and ra.value is integer"""
        return self.is_rational and _Lcl.is_integer(self.ra.value)

    @property
    def is_irrational(self):
        """rational part equal to one"""
        return self.ra.value in (1, -1) and self.ir.value != 1

    @property
    def numerator(self):
        """ra.numerator + ir"""
        return RNU(Ra(self.ra.value.numerator), self.ir)

    @property
    def denominator(self):
        """ra.denominator"""
        return RNU(Ra(self.ra.value.denominator), Ir(1, 1))

    @property
    def mutual(self):
        return RNU(self.ra.mutual(), self.ir.mutual())

    # enable conversion to float and int
    def __float__(self):
        return float(self.ra) * float(self.ir)

    def __int__(self):
        return int(float(self))

    def __bool__(self):
        return self.ra.value != 0

    __eq__ = assert_other(lambda a, b: a.ra == b.ra and a.ir == b.ir)

    # get RNU object to be sortable
    @assert_other
    def __gt__(self, other):
        """
        comparison protocol:
            @ irrational values are greater than rational one
            @ if both values are rational the greater is the one with the biggest ra -> ra comparison protocol
            @ if both values are irrational the greater is the one with the biggest ir -> ir comparison protocol
            @ the methods will always check for the irrationals first, if they end up being the same, it will move on
              to parse the rationals
        """
        if self.ir > other.ir:
            return True
        elif self.ir == other.ir:
            return self.ra > other.ra
        return False

    # compatibility checker
    @assert_other
    def is_compatible(self, other):
        """
        Two RNU objects are compatible if, when summed, they can be represented as another RNU object.
        -> rational parts are always compatible with each other
        -> irrational parts are compatible with each other only when they are the same
        """
        return self.ir == other.ir

    # operations
    def __neg__(self):
        return RNU(-self.ra, self.ir)

    @assert_other
    def __add__(self, other):
        if self.is_compatible(other):
            return RNU(Ra(self.ra.value + other.ra.value), self.ir)
        raise Error.MissingImplementationError('Addition between non-compatible RNU objects is yet to be implemented')

    __mul__ = assert_other(lambda a, b: RNU(a.ra * b.ra, a.ir * b.ir))
    __truediv__ = assert_other(lambda a, b: a * b.mutual())

    def sqrt(self):
        if self < RNU(s='0'):
            raise Error.OperationError('Unable to get square root of a negative RNU {}'.format(str(self)))
        ra = self.ra.value ** self.ir.index
        ir = self.ir.value
        return RNU(Ra(1), Ir(ra * ir, self.ir.index * 2))

    def cbrt(self):
        ra = self.ra.value ** self.ir.index
        ir = self.ir.value
        return RNU(Ra(1), Ir(ra * ir, self.ir.index * 3))


class LRN:
    """
    Real Number
    should be able to represent any real number possible with this
    """

    def __init__(self, arg):
        # passing list of RNU objects
        if isinstance(arg, list):
            self.units = _Lcl.parse_lin_rn_data(arg)
        else:
            Error.raise_argument_error(self.__class__.__name__, 'arg', [list], arg)
        self.units.sort()

    def __str__(self):
        return ''.join(list(map(lambda i: str(i), self.units)))

    def __repr__(self):
        return 'LRN([' + ', '.join(list(map(lambda i: repr(i), self.units))) + '])'

    # properties
    @property
    def is_rational(self):
        return all(unit.is_rational for unit in self.units)

    @property
    def is_integer(self):
        return all(unit.is_integer for unit in self.units)

    @property
    def is_irrational(self):
        return all(unit.is_irrational for unit in self.units)

    # enable conversion to float, int, bool and iterable
    def __float__(self):
        return float(sum(list(map(lambda i: float(i), self.units))))

    def __int__(self):
        return int(float(self))

    def __bool__(self):
        return not round(float(self), 5) == 0

    def __iter__(self):
        # only if self is integer
        if not self.is_integer:
            raise Error.OperationError('Unable to iterate through {} LRN object, must be integer'.format(str(self)))
        for i in range(int(self)):
            yield i

    # comparison methods
    @assert_other
    def __eq__(self, other):
        # self.units is a sorted list
        return self.units == other.units

    @staticmethod
    def _compare(a, b, operator):
        _ = a, b
        return eval('float(a)' + operator + 'float(b)')

    @assert_other
    def __gt__(self, other):
        return self._compare(self, other, '>')

    @assert_other
    def __ge__(self, other):
        return self._compare(self, other, '>=')

    @assert_other
    def __lt__(self, other):
        return self._compare(self, other, '<')

    @assert_other
    def __le__(self, other):
        return self._compare(self, other, '<=')

    # algebraic operations
    def __neg__(self):
        return LRN([-unit for unit in self.units])

    __add__ = assert_other(lambda a, b: LRN(a.units + b.units))
    __sub__ = assert_other(lambda a, b: LRN(a.units + (-b).units))

    @assert_other
    def __mul__(self, other):
        units = []
        for unit_a in self.units:
            for unit_b in other.units:
                units += [unit_a * unit_b]
        return LRN(units)

    def __pow__(self, power, modulo=None):
        if not isinstance(power, LRN):
            return NotImplemented
        if not power.is_integer:
            raise Error.MissingImplementationError('Powers to non-integer LRN is yet to be implemented')
        n = LRN([RNU(Ra(1), Ir(1, 1))])
        for _ in power:
            n *= self
        return n

    def sqrt(self):
        # only if mono unit
        if self < LRN([RNU(s='0')]):
            raise Error.OperationError('Unable to get square root of a negative LRN {}'.format(str(self)))
        if len(self.units) == 1:
            return LRN([self.units[0].sqrt()])
        return NotImplemented

    def cbrt(self):
        # only if mono unit
        if len(self.units) == 1:
            return LRN([self.units[0].cbrt()])
        return NotImplemented


class RN:
    """
    overcomes representability issues with some real numbers:
    -> open truediv
    -> open roots
    -> open mutual

    will put up a simple parser to enable the user to pass RNU objects as num and den (instead of LRN objects)
    this limits the amount of RN representable but also introduce an easier way to assign simple values
    """

    def __init__(self, numerator, denominator=LRN([RNU(Ra(1), Ir(1, 1))])):
        """
        arguments can be any of these types:
            -LRN
            -RNU
            -int
            -float
            -Fraction
            -Decimal
        needless to say that only by passing LRN objects you are able to represent every real number possible,
        but the other types enable an easier usage and faster creation of Real Numbers like integers or simple fractions
        """
        self.args = [numerator, denominator]
        data = _Lcl.validate_rn(numerator, denominator)
        if any(i == '' for i in data):
            Error.raise_argument_error(self.__class__.__name__, '[num, den]', [LRN, RNU, int, float, Fraction, Decimal],
                                       data)
        self.numerator, self.denominator = _Lcl.parse_rn_data(*data)

    def __str__(self):
        return _Lcl.rn_str(self.numerator, self.denominator)

    def __repr__(self):
        return 'RN(' + repr(self.numerator) + ', ' + repr(self.denominator) + ')'

    def __bool__(self):
        return bool(self.numerator)

    def __iter__(self):
        # only if self is integer
        if not self.is_integer:
            raise Error.OperationError('Unable to iterate through {} RN object, must be integer'.format(str(self)))
        for i in range(int(self)):
            yield i

    def __hash__(self):
        return 0

    def __int__(self):
        return int(float(self))

    def __float__(self):
        return float(self.numerator) / float(self.denominator)

    # properties
    @property
    def mutual(self):
        return RN(self.denominator, self.numerator)

    @property
    def is_rational(self):
        return self.numerator.is_rational and self.denominator.is_rational

    @property
    def is_irrational(self):
        """true if every element is irrational, not if one element is..."""
        return self.numerator.is_irrational and self.denominator.is_irrational

    @property
    def is_integer(self):
        """if integer it means that reducing to float value it should simplify to around integer value"""
        return round(float(self), 5) == int(self)

    @property
    def has_denominator(self):
        """denominator is none if it is equal to ONE (its standard value if not specified)"""
        return self.denominator != LRN([RNU(Ra(1), Ir(1, 1))])

    @property
    def has_numerator(self):
        """numerator if none if not LRN.__bool__(numerator)"""
        return bool(self.numerator)

    @property
    def is_rationalized(self):
        """rationalized if denominator is rational"""
        return self.denominator.is_rational

    # comparisons
    def __eq__(self, other):
        # if other is int, float, Fraction or Decimal -> turn to RN and compare
        if any(isinstance(other, tp) for tp in [int, float, Fraction, Decimal, LRN, RNU]):
            other = RN(other)

        # if other is RN -> compare num and den
        if isinstance(other, RN):
            return self.numerator == other.numerator and self.denominator == other.denominator
        # else -> NotImplemented
        return NotImplemented

    # pure numerical comparison
    def _compare(self, other, op):
        # var to not get static method warning
        _ = self
        # if other is RN, LRN, RNU -> use float property
        if any(isinstance(other, tp) for tp in [RN, LRN, RNU]):
            return eval('float(self)' + op + 'float(other)')
        # if other is int, float, Fraction, Decimal -> compare
        elif any(isinstance(other, tp) for tp in [int, float, Fraction, Decimal]):
            return eval('float(self)' + op + 'other')
        # else -> NotImplemented
        return NotImplemented

    def __gt__(self, other):
        return self._compare(other, '>')

    def __ge__(self, other):
        return self._compare(other, '>=')

    def __lt__(self, other):
        return self._compare(other, '<')

    def __le__(self, other):
        return self._compare(other, '<=')

    # operate
    # first -> ensure other is instance of RN, if not convert to it
    # to operate sum and subtraction we must get a common denominator for self and other
    # -> denominator = self.denominator * other.denominator
    # adjust numerators
    # -> numerator = self.num * other.den + other.num * self.den
    def __neg__(self):
        return RN(-self.numerator, self.denominator)

    def __add__(self, other):
        # if other is LRN -> faster to add it to the numerator and multiply it for denominator
        if isinstance(other, LRN):
            return RN(self.numerator + other * self.denominator, self.denominator)
        # if other is RNU -> assign as LRN
        elif isinstance(other, RNU):
            return RN(self.numerator + LRN([other]) * self.denominator, self.denominator)
        # everything else -> create RN obj and get parsers to handle it
        elif any(isinstance(other, tp) for tp in [int, float, Fraction, Decimal]):
            other = RN(other)

        # if other is RN -> sum
        if isinstance(other, RN):
            return RN(self.numerator * other.denominator + other.numerator * self.denominator,
                      self.denominator * other.denominator)
        # else -> NotImplemented
        return NotImplemented

    def __sub__(self, other):
        # self + (-other)
        if any(isinstance(other, tp) for tp in [RN, LRN, int, float, Fraction, Decimal]):
            return self + (-other)
        # else -> NotImplemented
        return NotImplemented

    def __mul__(self, other):
        # if other is LRN -> faster to multiply it to the numerator
        if isinstance(other, LRN):
            return RN(self.numerator * other, self.denominator)
        # if other is RNU -> assign as LRN
        elif isinstance(other, RNU):
            return RN(self.numerator * LRN(other), self.denominator)
        # everything else -> create RN obj and get parsers to handle it
        elif any(isinstance(other, tp) for tp in [int, float, Fraction, Decimal]):
            other = RN(other)

        # if other is RN -> mul
        if isinstance(other, RN):
            return RN(self.numerator * other.numerator, self.denominator * other.denominator)
        # else -> NotImplemented
        return NotImplemented

    def __truediv__(self, other):
        if self == 0:
            return self
        # if other is LRN -> turn to RN
        if isinstance(other, LRN):
            other = RN(other)

        # self * other.mutual if mutual property defined (LRN and RNU)
        if any(isinstance(other, tp) for tp in [LRN, RNU]):
            return self * other.mutual
        # if other is int, float, Fraction, Decimal -> use 1 / other to get mutual
        elif any(isinstance(other, tp) for tp in [int, float, Fraction, Decimal]):
            return self * (1 / other)
        # if other is RN -> turn to mutual
        elif isinstance(other, RN):
            return self * other.mutual
        # else -> NotImplemented
        return NotImplemented

    def __floordiv__(self, other):
        return RN(int(self / other))

    def __mod__(self, other):
        # result of the expression should be RN
        return self - (self // other) * other

    def __pow__(self, power, modulo=None):
        # must assert power is integer
        # and then loop through it
        # if power is RN, LRN, RNU -> use is integer property
        if any(isinstance(power, tp) for tp in [RN, LRN, RNU]):
            if not power.is_integer:
                raise Error.MissingImplementationError('Powers of non-integer real numbers is yet to be implemented,'
                                                       'unable to get {} elevated to the power of {}'
                                                       .format(str(self), str(power)))
            n = RN(1)
            for _ in power:
                n *= self
            return n
        # if power is int, float, Fraction, Decimal -> use int(power) == power to assert is integer
        elif any(isinstance(power, tp) for tp in [int, float, Fraction, Decimal]):
            if not int(power) == power:
                raise Error.MissingImplementationError('Powers of non-integer real numbers is yet to be implemented,'
                                                       'unable to get {} elevated to the power of {}'
                                                       .format(str(self), str(power)))
            n = RN(1)
            power = int(power)
            for _ in range(power):
                n *= self
            return n
        return NotImplemented

    def sqrt(self):
        # for now
        # will be defined only for mono unit num / den RN
        if self < 0:
            raise Error.OperationError('Unable to get square root of a negative real number {}'.format(str(self)))
        if len(self.numerator.units) == 1 and len(self.denominator.units) == 1:
            num = self.numerator.sqrt()
            den = self.denominator.sqrt()
            return RN(num, den)
        return NotImplemented

    def cbrt(self):
        # for now
        # will be defined only for mono unit num / den RN
        if len(self.numerator.units) == 1 and len(self.denominator.units) == 1:
            num = self.numerator.cbrt()
            den = self.denominator.cbrt()
            return RN(num, den)
        return NotImplemented

    def __abs__(self):
        """if self < 0 -> return -self"""
        return self if self > 0 else -self

    # Reflected operations
    # Will work with LRN, RNU, int, float, Fraction, Decimal
    # Will return RN and turn other to RN when possible
    @assert_rn_other
    def __radd__(self, other):
        return RN(other) + self

    @assert_rn_other
    def __rsub__(self, other):
        return RN(other) - self

    @assert_rn_other
    def __rmul__(self, other):
        return RN(other) * self

    @assert_rn_other
    def __rtruediv__(self, other):
        return RN(other) / self

    @assert_rn_other
    def __rfloordiv__(self, other):
        return RN(other) // self

    @assert_rn_other
    def __rmod__(self, other):
        return RN(other) % self

    @assert_rn_other
    def __rpow__(self, other):
        return RN(other) ** self


# Real numbers simple intervals class
class SI:
    """
    Simple Interval
    """

    def __init__(self, lower_limit=0, upper_limit=0, lower_equal=False, upper_equal=False):
        _Lcl.validate_limits(lower_limit, upper_limit)
        _Lcl.validate_equals(lower_equal, upper_equal)
        if any(isinstance(lower_limit, tp) for tp in [RNU, LRN]):
            lower_limit = RN(lower_limit)
        if any(isinstance(upper_limit, tp) for tp in [RNU, LRN]):
            upper_limit = RN(upper_limit)
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.equals = [lower_equal, upper_equal]
        # build string
        self.string = ('[' if lower_equal else '(') + str(self.lower_limit) + '; ' \
                      + str(self.upper_limit) + (']' if upper_equal else ')')

    def __str__(self):
        return self.string

    def __repr__(self):
        return 'SI(' + repr(self.lower_limit) + ', ' + repr(self.upper_limit) + ', ' \
               + repr(self.equals[0]) + ', ' + repr(self.equals[1]) + ')'

    def __bool__(self):
        return not self.is_empty()

    # get to sortable
    def __gt__(self, other):
        if isinstance(other, SI):
            return True if self.lower_limit > other.lower_limit else False
        return NotImplemented

    def __contains__(self, item):
        if any(isinstance(item, tp) for tp in [RN, LRN, RNU, int, float, Fraction, Decimal]):
            if self.lower_limit < item < self.upper_limit:
                return True
            elif item == self.lower_limit and self.equals[0]:
                return True
            elif item == self.upper_limit and self.equals[1]:
                return True
            return False
        return NotImplemented

    def is_empty(self):
        if self.lower_limit == 0 and self.upper_limit == 0 and not self.equals[0] and not self.equals[1]:
            return True
        return False

    def intersect(self, other):
        if isinstance(other, SI):
            if self.upper_limit == other.lower_limit:
                if self.equals[1] is True and other.equals[0] is True:
                    return True
                return False
            if other.upper_limit == self.lower_limit:
                if other.equals[1] is True and self.equals[0] is True:
                    return True
                return False
            # if a limit of self / other is in other / self
            if self.upper_limit in other or self.lower_limit in other \
                    or other.lower_limit in self or other.upper_limit in self:
                return True
            return False
        return NotImplemented

    def __and__(self, other):
        if isinstance(other, SI):
            if not self.intersect(other):
                # return empty
                return SI()
            # possible cases
            # ONE
            # 0------0
            #     0------0
            # TWO
            #     0------0
            # 0------0
            # THREE
            # 0----------0
            #     0--0
            # FOUR
            #     0--0
            # 0----------0
            # result -> greater lower limit and smaller upper limit
            lower, from_self_lower = (self.lower_limit, True) if self.lower_limit > other.lower_limit \
                else (other.lower_limit, False)
            upper, from_self_upper = (self.upper_limit, True) if self.upper_limit < other.upper_limit \
                else (other.upper_limit, False)
            # set equals
            equals = [True, True]
            if (from_self_lower and not self.equals[0]) or (not from_self_lower and not other.equals[0]):
                equals[0] = False
            if (from_self_upper and not self.equals[1]) or (not from_self_upper and not other.equals[1]):
                equals[1] = False
            return SI(lower, upper, equals[0], equals[1])
        return NotImplemented

    # able to perform union only if there is an intersection between self and other
    def __or__(self, other):
        if isinstance(other, SI):
            if not self.intersect(other):
                return NotImplemented
            # result -> smaller lower limit and greater upper limit
            lower, from_self_lower = (self.lower_limit, True) if self.lower_limit < other.lower_limit \
                else (other.lower_limit, False)
            upper, from_self_upper = (self.upper_limit, True) if self.upper_limit > other.upper_limit \
                else (other.upper_limit, False)
            # set equals
            equals = [True, True]
            if (from_self_lower and not self.equals[0]) or (not from_self_lower and not other.equals[0]):
                equals[0] = False
            if (from_self_upper and not self.equals[1]) or (not from_self_upper and not other.equals[1]):
                equals[1] = False
            return SI(lower, upper, equals[0], equals[1])
        return NotImplemented


# Real numbers complex intervals class
# -> expecting list of SI objects
# -> set like object
class Interval:
    def __init__(self, units):
        _Lcl.validate_int_units(units)
        self.units = _Lcl.parse_int_units(units)
        self.string = ' + '.join([unit.string for unit in self.units])

    def __str__(self):
        return self.string

    def __repr__(self):
        return 'Interval([' + ', '.join([repr(unit) for unit in self.units]) + '])'

    def __contains__(self, item):
        for unit in self.units:
            if item in unit:
                return True
        return False

    def __and__(self, other):
        if isinstance(other, Interval):
            units = []
            for unit in self.units:
                for UNIT in other.units:
                    if unit.intersect(UNIT):
                        units += [unit & UNIT]
            if not units:
                return Interval([SI()])
            return Interval(units)
        return NotImplemented

    def __or__(self, other):
        if isinstance(other, Interval):
            return Interval(self.units + other.units)
        return NotImplemented
