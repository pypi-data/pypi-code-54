"""
Main module for literals objects and actual polynomials representations

Getting real numbers classes from rn.py
Getting interval objects from rn.py
Getting various functions from mathfunc.py

classes defined here:
    Li (unary literal representation object)
    ML (multi literals representation object)
    Tr (term representation object -> RN + ML)
    LPN (linear polynomial object)
    PN (actual polynomial object)

    _Lcl (local useful methods)
    Errors (local mathematical errors)
"""


from sys import version
from fractions import Fraction
from decimal import Decimal
from typing import Callable, Any, Iterable
from functools import reduce
from math import inf
from itertools import chain
from ..rn.rn import RN, SI, Interval
from ..rn.rn import Error as RnError
from .func import remove_none_from_list, GCD, LCM


__author__ = 'Viganò Andrea'
__version__ = 'pn module 1.7 for ACE 0.1.0 official release for Python {}'.format(version)


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

    class OperationError(Exception):
        pass


# Operations / Comparisons decorator
def assert_other(func: Callable) -> Callable:
    def wrapper(self: Any, other: Any) -> Any:
        try:
            assert isinstance(other, type(self))
        except AssertionError:
            return NotImplemented
        return func(self, other)

    return wrapper


def assert_tr_other(func: Callable) -> Callable:
    def wrapper(self: Any, other: Any) -> Any:
        try:
            assert any(isinstance(other, tp) for tp in [Tr, RN, int, float, Fraction, Decimal])
        except AssertionError:
            return NotImplemented
        return func(self, other)

    return wrapper


def assert_lpn_other(func: Callable) -> Callable:
    def wrapper(self: Any, other: Any) -> Any:
        try:
            assert any(isinstance(other, tp) for tp in [LPN, Tr, RN, int, float, Fraction, Decimal])
        except AssertionError:
            return NotImplemented
        return func(self, other)

    return wrapper


def assert_pn_other(func: Callable) -> Callable:
    def wrapper(self: Any, other: Any) -> Any:
        try:
            assert any(isinstance(other, tp) for tp in [PN, LPN, Tr, RN, int, float, Fraction, Decimal])
        except AssertionError:
            return NotImplemented
        return func(self, other)

    return wrapper


# local fast-assignment function
chars = 'qwertyuiopasdfghjklzxcvbnm'


def tr(string: str):
    """string type: coefficient (integer only) + letter + exp (len = 1 only)"""
    global chars
    coefficient, letters, exponents = '', [], []
    in_coefficient = True
    for ch in string:
        if ch in chars:
            in_coefficient = False
        if in_coefficient:
            coefficient += ch
        else:
            if ch in chars:
                letters += [ch]
            else:
                exponents += [ch]
    return Tr(int(coefficient), ML([Li(letter, int(exponent)) for letter, exponent in zip(letters, exponents)]))


def lpn(string: str):
    """string type: tr separated by a whitespace"""
    return LPN([tr(term) for term in string.split(' ')])


def pn(string: str):
    """string type: [lpn string]/[lpn string]"""
    num, den = string.split('/')[0], string.split('/')[1]
    return PN(lpn(num[1:-1]), lpn(den[1:-1]))


# Local methods
class _Lcl:
    @staticmethod
    def validate_letter(letter) -> None:
        if not isinstance(letter, str):
            Error.raise_argument_error(Li.__name__, 'letter', [str], letter)
        elif len(letter) != 1:
            raise Error.ArgumentError('Bad user argument, letter parameter in {} class must be a char, got {}'.format(
                Li.__name__, letter))
        elif letter not in 'qwertyuiopasdfghjklzxcvbnm':
            raise Error.ArgumentError('Bad user argument, letter parameter in {} class must be a letter'
                                      .format(Li.__name__))

    @staticmethod
    def convert_to_integer(value: RN or int or float or Fraction or Decimal):
        if isinstance(value, RN):
            if value.is_integer:
                return int(value)
            return ''
        elif any(isinstance(value, tp) for tp in [float, Fraction, Decimal]):
            if int(value) == round(value, 5):
                return int(value)
            return ''
        elif isinstance(value, int):
            return value
        return ''

    @staticmethod
    def convert_to_RN(value: RN or int or float or Fraction or Decimal):
        if isinstance(value, RN):
            return value
        elif any(isinstance(value, tp) for tp in [int, float, Fraction, Decimal]):
            return RN(value)
        return ''

    @staticmethod
    def validate_ml(literals: list or tuple) -> None:
        if not isinstance(literals, Iterable):
            Error.raise_argument_error(ML.__name__, 'literals', [list], literals)
        for i in literals:
            if not isinstance(i, Li):
                raise Error.ArgumentError('Bad user argument for {} class, each element in literals must be instance'
                                          ' of {} class'.format(ML.__name__, Li.__name__))

    @staticmethod
    def parse_ml_data(literals) -> list:
        """
        if any element of literals has exponent == 0 -> delete it
        if there are elements of literals that have the same letter -> mul them
        """
        literals.sort()
        for p, literal in enumerate(literals):
            try:
                if literal.is_compatible(literals[p + 1]):
                    # noinspection PyTypeChecker
                    literals[p] = None
                    literals[p + 1] = literal * literals[p + 1]
            except IndexError:
                continue
        return remove_none_from_list(literals)

    @staticmethod
    def validate_literals_dict(literals, literals_dict: dict, cls) -> None:
        # turn literals to set if ML is passed
        if isinstance(literals, ML):
            literals = set([literal.letter for literal in literals])
        # verify that there is not unexpected letter
        for literal in literals_dict:
            if literal not in [_literal for _literal in literals]:
                raise Error.ArgumentError('Bad user argument, literals_dict for eval_to of {} class can\'t contain'
                                          'letters that are not in the object it is referring to'.format(cls.__name__))
        # verify that there are not missing letters and that every value is a number
        for literal in literals:
            try:
                _ = literals_dict[literal]
                assert any(isinstance(_, tp) for tp in [int, float, Fraction, Decimal, RN])
            except KeyError:
                raise Error.ArgumentError('Bad user argument, literals_dict for eval_to of {} class must contain all'
                                          'all the letters contained in the object it is referring to'
                                          .format(cls.__name__))
            except AssertionError:
                raise Error.ArgumentError('Bad user argument, literals_dict values for eval_to of {} class must all'
                                          'be numbers'.format(cls.__name__))

    @staticmethod
    def validate_variable(parameters: set, variable):
        if not isinstance(variable, str):
            raise Error.ArgumentError('Bad user argument, variable parameter for {} of {} class must be {}, got {}'
                                      .format('variable_degree', Tr.__name__, str, variable))
        elif len(variable) != 1:
            raise Error.ArgumentError('Bad user argument, variable parameter for {} of {} class must be char, got {}'
                                      .format('variable_degree', Tr.__name__, variable))
        elif variable not in parameters:
            raise Error.ArgumentError('Bad user argument, variable parameter for {} of {} class must be a variable of'
                                      ' term'.format('variable_degree', Tr.__name__))

    @staticmethod
    def get_tr_GCD(a, b):
        # get coefficients GCD
        if not (a.coefficient.is_integer and b.coefficient.is_integer):
            coefficients_GCD = 1
        else:
            coefficients_GCD = GCD([int(a.coefficient), int(b.coefficient)])
        # get literals GCD
        common_parameters = set.intersection(a.parameters, b.parameters)
        literals_dict = {letter: inf for letter in common_parameters}
        if common_parameters:
            for term in [a, b]:
                for literal in term.literals:
                    try:
                        if literals_dict[literal.letter] > literal.exponent:
                            literals_dict[literal.letter] = literal.exponent
                    except KeyError:
                        continue
            return Tr(coefficients_GCD, ML([Li(letter, literals_dict[letter]) for letter in literals_dict]))
        else:
            return Tr(coefficients_GCD)

    @staticmethod
    def validate_lpn(terms: list):
        if not isinstance(terms, list):
            Error.raise_argument_error(LPN.__name__, 'terms', [list], terms)
        for term in terms:
            if not any(isinstance(term, tp) for tp in [Tr, RN, int, float, Fraction, Decimal]):
                raise Error.ArgumentError('Bad user argument, every element of terms for {} class must be {}, got {}'
                                          .format(LPN.__name__, [Tr, RN, int, float, Fraction, Decimal], term))

    @staticmethod
    def parse_lpn_data(terms: list) -> list:
        """
        parsing:
            - convert every item to Tr object
            - sort terms list -> two element which are compatible will be close to each other
            - loop through terms and check if a term is compatible with the one next
        """
        for p, term in enumerate(terms):
            if any(isinstance(term, tp) for tp in [RN, int, float, Fraction, Decimal]):
                terms[p] = Tr(term)
        terms.sort()
        for p, term in enumerate(terms):
            try:
                if term.is_compatible(terms[p + 1]):
                    terms[p] = None
                    terms[p + 1] = term + terms[p + 1]
            except IndexError:
                continue
        return remove_none_from_list(terms)

    @staticmethod
    def get_lpn_terms_GCD(terms: list):
        return reduce(_Lcl.get_tr_GCD, terms) if len(terms) != 1 else terms[0]

    # LPN floordiv methods
    @staticmethod
    def lpn_ordered_terms(terms: list, variable: str):
        """
        get ordered terms (relatively to one gaven variable)
        -> get a list (ordered like terms) containing the degrees of the terms relatively to var
        -> hook that list to a dict (way to get the correspondent terms)
        -> sort the list
        -> iter and index the dictionary to build the new ordered terms list
        """
        var_degrees = []
        for term in terms:
            try:
                var_degrees += [term.literals.literals_dict[variable]]
            except KeyError:
                var_degrees += [0]
        var_degree_dict = {exp: term for term, exp in zip(terms, var_degrees)}
        return [var_degree_dict[exp] for exp in reversed(sorted(var_degrees))]

    @staticmethod
    def get_lpn_completeness(terms: list, variable: str):
        # assert args[0] has already been ordered from var
        exp_list = []
        for term in terms:
            try:
                exp_list.append(term.literals.literals_dict[variable])
            except KeyError:
                exp_list.append(0)
        exp_list.reverse()
        missing = {_ for _ in range(exp_list[0])}.difference(set(exp_list))
        return (False, missing) if missing else (True, set())

    @staticmethod
    def lpn_complete_terms(ordered_terms: list, variable: str):
        # assert args[0] has already been ordered for var
        ordered_terms.reverse()
        for exp in _Lcl.get_lpn_completeness(ordered_terms, variable)[1]:
            ordered_terms.insert(exp, Tr(0, ML([Li(variable, exp)])))
        return list(reversed(ordered_terms))

    # to be re-seen
    @staticmethod
    def lpn_division_algorithm(dividend, divisor):
        """
        division with / without rest:
            to check use self % other -> if equal to 0: perfect division
                                         else: division with rest
        division algorithm:
            self.max_degree_term / other.max_degree_term --> A
            self - other.A --> B
            self = B ...
            until degree self (B) < degree other

        Preparation:
            get COMPLETE / ORDERED coefficients list of self and other
            -> from self / other completeness -> get_complete_coefficients(self / other) relatively to one variable
        """
        # work if divisor is LPN
        q, lcl, var = [], [], chr(min([ord(var) for var in dividend.parameters]))
        a = dividend.complete_and_ordered(var)
        b = divisor.complete_and_ordered(var)
        while a[0].variable_degree(var) >= b[0].variable_degree(var):
            q += [a[0] / b[0]]
            lcl = LPN([q[-1]]) * -divisor
            a = LPN(a) + lcl
            a = a.complete_and_ordered(var)
            if len(a) == 0:  # no rest
                break
        return LPN(q), LPN(a)

    @staticmethod
    def filter_lpn_literals_dict(literals_dict, unit):
        # return filtered literals_dict for passed term / LPN
        # build new dict using keys from the original dict
        return {letter: literals_dict[letter] for letter in unit.parameters}

    @staticmethod
    def convert_to_LPN(factor):
        # could get LPN, Tr, number
        if isinstance(factor, LPN):
            return factor
        elif isinstance(factor, Tr):
            return LPN([factor])
        elif any(isinstance(factor, tp) for tp in [RN, int, float, Fraction, Decimal]):
            return LPN([Tr(factor)])
        return ''

    @staticmethod
    def parse_pn_data(numerator, denominator):
        """
        parsing of PN data:
        - remove 'local' denominators
        - remove terms GCD
        """

        # remove local denominators
        # get LCM of denominators of num and den
        numerator_LCM, denominator_LCM = numerator.denominators_LCM, denominator.denominators_LCM
        # remove denominators
        # update numerators and denominators
        # num_terms = [term * (numerator_LCM / term.coefficient.denominator) * denominator_LCM
        #              for term in numerator.terms]
        # den_terms = [term * (denominator_LCM / term.coefficient.denominator) * numerator_LCM
        #              for term in denominator.terms]
        # numerator, denominator = LPN(num_terms), LPN(den_terms)
        num_terms = [Tr(term.coefficient.numerator * (numerator_LCM / term.coefficient.denominator), term.literals)
                     for term in numerator.terms]
        den_terms = [Tr(term.coefficient.numerator * (denominator_LCM / term.coefficient.denominator),
                        term.literals) for term in denominator.terms]
        # assign num and den to new values then multiply for other LCM
        numerator = LPN(num_terms) * denominator_LCM
        denominator = LPN(den_terms) * numerator_LCM

        # remove terms GCD
        # get terms_GCD of num and den
        # then get GCD of both
        terms_GCD = numerator.terms_GCD.GCD(denominator.terms_GCD)
        # divide every term for this GCD
        assert all(term.is_divisible(terms_GCD) for term in numerator.terms + denominator.terms)
        num_terms = [term / terms_GCD for term in numerator.terms]
        den_terms = [term / terms_GCD for term in denominator.terms]
        numerator, denominator = LPN(num_terms), LPN(den_terms)
        if numerator == 0:
            denominator = LPN([1])
        return numerator, denominator

    @staticmethod
    def reduce_pn(num, den):
        FACTORS = []
        # reduce num then den
        for elem in [num, den]:
            _factors = [elem]
            old = ()
            while _Lcl._factor_degree(_factors) > 1 and list(old) != _factors:
                # assign old to factors
                old = tuple(_factors)
                # reassign factors as a flat list of reduced items
                _factors = list(chain(*[_Lcl.reduce_pn_element(factor) for factor in _factors]))
            for p, factor in enumerate(_factors):
                if factor.degree == 1:
                    FACTOR = _Lcl._verify_case1_match(factor)
                    if FACTOR:
                        # insert N items in _factors list in a specific position
                        del(_factors[p])
                        for i in range(p, p + len(FACTOR)):
                            _factors.insert(i, FACTOR[i - p])
            FACTORS += [_factors]
        return _Lcl._reduce_decomposed_lists(*FACTORS)

    @staticmethod
    def _reduce_decomposed_lists(num_factors, den_factors):
        # may check if the change of sign can enable some more reduction
        # remove equal items from factors lists
        factors = [num_factors, den_factors]
        for p in [0, 1]:
            FACTORS = tuple(tuple(item) for item in factors)
            for i in range(len(FACTORS[p])):
                if FACTORS[p][i] in factors[abs(p - 1)]:
                    factors[0].remove(FACTORS[p][i])
                    factors[1].remove(FACTORS[p][i])
                    factors[p].append(LPN([1]))
                    factors[abs(p - 1)].append(LPN([1]))
                elif -FACTORS[p][i] in factors[abs(p - 1)]:
                    factors[p].remove(FACTORS[p][i])
                    factors[abs(p - 1)].remove(-FACTORS[p][i])
                    factors[p].append(LPN([-1]))
                    factors[abs(p - 1)].append(LPN([1]))
        # congregate constant terms
        # track were constant terms are -> congregate them in the first one
        for p in [0, 1]:
            constant_terms = []
            for i, factor in enumerate(factors[p]):
                if factor.is_constant:
                    constant_terms += [i]
            for _, P in enumerate(constant_terms):
                if _ != 0:
                    # noinspection PyTypeChecker
                    factors[p][constant_terms[0]] *= factors[p][P]
                    # noinspection PyTypeChecker
                    factors[p][P] = None
            factors[p] = remove_none_from_list(factors[p])
        # may check if the product with the eventual constant term can enable some more reduction
        # if a list is empty -> put '0' in it
        for l in factors:
            if len(l) == 0:
                l.append(LPN([0]))
            # clear eventual '1's in list
            elif l.count(LPN([1])) > 0 and len(l) != 1:
                a = [factor for factor in l if factor != LPN([1])]
                l.clear()
                l.extend(a)
        return factors

    @staticmethod
    def _factor_degree(factors: Iterable) -> int:
        return max([factor.degree for factor in factors])

    @staticmethod
    def reduce_pn_element(elem):
        # assert elem is LPN
        assert isinstance(elem, LPN)
        # get special type
        # special reduction or pure decomposition
        special_type = _Lcl.get_special_type(elem)
        factors = []
        if special_type == 'I degree':
            factors = [elem]
        elif special_type == 'II degree':
            factors = _Lcl._decompose_II_degree_element(elem)
        elif special_type == 'binomial square':
            factors = _Lcl._decompose_binomial_square(elem)
        elif special_type == 'binomial':
            factors = _Lcl._single_decompose_pn_element(elem)
        elif special_type == 'trinomial':
            factors = _Lcl._decompose_trinomial_element(elem)
        elif special_type == '':
            # pure decomposition
            factors = _Lcl._single_decompose_pn_element(elem)
        return factors

    # TESTED
    @staticmethod
    def get_special_type(elem):
        # I degree
        # II degree
        # binomial
        # trinomial
        # ''

        # assert elem is LPN
        assert isinstance(elem, LPN)
        # parse for binomial square first of all (also bi-variable)
        if len(elem.terms) == 3:
            # different parsing of mono or bi variable
            if elem.is_mono_variable:
                if elem.terms[0].is_perfect_square and elem.terms[2].is_perfect_square \
                   and elem.terms[2].literals.literals[0].exponent % 2 == 0:
                    # check for double product
                    if elem.terms[1] == Tr(2 * elem.terms[0].coefficient.sqrt() * elem.terms[2].coefficient.sqrt(),
                                           ML([Li(elem.terms[2].literals.literals[0].letter,
                                                  elem.terms[2].literals.literals[0].exponent // 2)])) \
                        or elem.terms[1] == Tr(-2 * elem.terms[0].coefficient.sqrt() * elem.terms[2].coefficient.sqrt(),
                                               ML([Li(elem.terms[2].literals.literals[0].letter,
                                                      elem.terms[2].literals.literals[0].exponent // 2)])):
                        return 'binomial square'
            else:
                # to be implemented
                pass
        # if not mono variable -> no special type exists
        if elem.is_mono_variable:
            if elem.degree == 1:
                return 'I degree'
            elif elem.degree == 2 and elem.has_constant_term:
                return 'II degree'
            else:
                # degree > 2 here
                # binomial -> term + CT
                if len(elem.terms) == 2 and elem.has_constant_term:
                    return 'binomial'
                # trinomial -> term degree + term degree // 2 + CT
                elif len(elem.terms) == 3 and all(term.is_constant or term.degree == elem.degree or
                                                  term.degree == elem.degree // 2 for term in elem.terms) \
                        and elem.degree % 2 == 0:
                    return 'trinomial'
                else:
                    # mutual -> reduce with ruffini...
                    return ''
        return ''

    # TESTED
    @staticmethod
    def _decompose_II_degree_element(elem):
        # assert elem is LPN
        assert isinstance(elem, LPN)
        # elem is a II degree special type
        # -> mono variable / second degree
        # -> reduce with ax2 + bx + c = a (x - root one) (x - root two)
        #    -> get delta = b2 - 4ac
        if len(elem.terms) == 2:
            a, b, c = elem.terms[1].coefficient, 0, elem.terms[0].coefficient
        else:
            a, b, c = elem.terms[2].coefficient, elem.terms[1].coefficient, elem.terms[0].coefficient
        delta = b ** 2 - 4 * a * c
        if delta < 0:
            # no roots
            return _Lcl._single_decompose_pn_element(elem)
        elif delta == 0:
            # one root
            root = -b / (2 * a)
            return [LPN([a]), LPN([Tr(1, ML([Li(elem.terms[1].literals.literals[0].letter, 1)])), Tr(-root)]),
                    LPN([Tr(1, ML([Li(elem.terms[1].literals.literals[0].letter, 1)])), Tr(-root)])]
        else:
            # two roots
            # may not decompose if delta is multi-unit real number
            if len(delta.numerator.units) > 1 or len(delta.denominator.units) > 1:
                return _Lcl._single_decompose_pn_element(elem)
            roots = [(-b + delta.sqrt()) / (2 * a), (-b - delta.sqrt()) / (2 * a)]
            return [LPN([a]), LPN([Tr(1, ML([Li(elem.terms[1].literals.literals[0].letter, 1)])), Tr(-roots[0])]),
                    LPN([Tr(1, ML([Li(elem.terms[1].literals.literals[0].letter, 1)])), Tr(-roots[1])])]

    @staticmethod
    def _decompose_binomial_square(elem):
        # already tested and verified as binomial square
        # if double product is negative -> opposite signs
        #                   is positive -> same sign (+)
        if elem.terms[1].coefficient > 0:
            factor = LPN([Tr(elem.terms[0].coefficient.sqrt(),
                             ML([Li(letter, elem.terms[0].literals.literals_dict[letter] // 2)
                                 for letter in elem.terms[0].literals.literals_dict])),
                          Tr(elem.terms[2].coefficient.sqrt(),
                             ML([Li(letter, elem.terms[2].literals.literals_dict[letter] // 2)
                                 for letter in elem.terms[2].literals.literals_dict]))])
        else:
            factor = LPN([Tr(elem.terms[0].coefficient.sqrt(),
                             ML([Li(letter, elem.terms[0].literals.literals_dict[letter] // 2)
                                 for letter in elem.terms[0].literals.literals_dict])),
                          Tr(-elem.terms[2].coefficient.sqrt(),
                             ML([Li(letter, elem.terms[2].literals.literals_dict[letter] // 2)
                                 for letter in elem.terms[2].literals.literals_dict]))])
        return [factor, factor]

    # TESTED
    @staticmethod
    def _decompose_trinomial_element(elem):
        # assert elem is LPN
        assert isinstance(elem, LPN)
        # get multiplication factor of exponents (exponent is divisible by two)
        exponent_factor = elem.terms[2].literals.literals[0].exponent // 2
        # get decomposed form like a (x - root one) (x - root two)
        factors = _Lcl._decompose_II_degree_element(LPN([Tr(elem.terms[2].coefficient,
                                                            ML([Li(elem.terms[2].literals.literals[0].letter,
                                                                   elem.terms[2].literals.literals[0].exponent //
                                                                   exponent_factor)])),
                                                         Tr(elem.terms[1].coefficient,
                                                            ML([Li(elem.terms[1].literals.literals[0].letter,
                                                                   elem.terms[1].literals.literals[0].exponent //
                                                                   exponent_factor)])), elem.terms[0]]))
        if len(factors) == 1:
            return _Lcl._single_decompose_pn_element(elem)
        factor_zero = factors[0]
        factor_one = LPN([Tr(1, ML([Li(factors[1].terms[1].literals.literals[0].letter, exponent_factor)])),
                          factors[1].terms[0]])
        factor_two = LPN([Tr(1, ML([Li(factors[2].terms[1].literals.literals[0].letter, exponent_factor)])),
                          factors[2].terms[0]])
        return [factor_zero, factor_one, factor_two]

    @staticmethod
    def _single_decompose_pn_element(elem):
        # decompose num / den -> elem
        # assert elem is LPN
        assert isinstance(elem, LPN)
        cases = [_Lcl._verify_case1_match, _Lcl._verify_case2_match, _Lcl._verify_case3_a_match,
                 _Lcl._verify_case3_b_match, _Lcl._verify_case3_c_match, _Lcl._verify_case4_match,
                 _Lcl._verify_case5_match, _Lcl._verify_case6_match]
        for case in cases:
            factors = case(elem)
            if factors:
                return factors
        return [elem]

    # TESTED
    @staticmethod
    def _verify_case1_match(elem):
        # case 1
        if elem.terms_GCD != Tr(1) and not elem.is_constant and len(elem.terms) > 1:
            assert all([term.is_divisible(elem.terms_GCD) for term in elem.terms])
            return [LPN([elem.terms_GCD]), LPN([term / elem.terms_GCD for term in elem.terms])]
        return None

    # TESTED
    @staticmethod
    def _verify_case2_match(elem):
        # look for pairs that have a GCD != 1
        # try group them and check if the remaining terms are both divisible by that same GCD
        # if it work, return, else, try with a new pair
        # number of pairs possible -> C(4,2) = (4! / 2!) = 12
        # numbers of double pairs:
        #    -> when a pair is determined, the other two terms build up the second pair,
        #       so the number of associations that can be done is less than 12
        #    -> 3 -> AB - CD, AC - DB, AD - BC
        # double loop
        if len(elem.terms) == 4:
            # build matches
            matches = [[[elem.terms[0], elem.terms[1]], [elem.terms[2], elem.terms[3]]],
                       [[elem.terms[0], elem.terms[2]], [elem.terms[1], elem.terms[3]]],
                       [[elem.terms[0], elem.terms[3]], [elem.terms[1], elem.terms[2]]]]
            for p in range(3):
                # get GCD of both pairs
                gcd_one = matches[p][0][0].GCD(matches[p][0][1])
                gcd_two = matches[p][1][0].GCD(matches[p][1][1])
                # build LPN for pairs and divide for GCDs
                pair_one = LPN(matches[p][0])
                pair_two = LPN(matches[p][1])
                # check if the quotients are equal (need to also check for sign
                if pair_one // gcd_one == pair_two // gcd_two:
                    # validation was successful
                    return [LPN([gcd_one, gcd_two]), pair_one // gcd_one]
                elif pair_one // -gcd_one == pair_two // gcd_two:
                    return [LPN([-gcd_one, gcd_two]), pair_one // -gcd_one]
        return None

    # TESTED
    @staticmethod
    def _verify_case3_a_match(elem):
        # case 3-a
        # possible if:
        #   - two terms
        #   - opposite signs (order in a new list without the sign)
        #   - perfect squares
        # check opposite sign
        if len(elem.terms) != 2:
            return None
        if (elem.terms[0].coefficient > 0) != (elem.terms[1].coefficient > 0):
            # build list
            terms = [elem.terms[0], -elem.terms[1]] if elem.terms[1].coefficient < 0 else \
                [elem.terms[1], -elem.terms[0]]
            # coefficients in terms are all positive
            # check if perfect squares
            for term in terms:
                if not term.is_perfect_square:
                    break
            # conditions matched -> proceed to reduction
            else:
                # build two new LPN objects
                # rooted terms list
                terms = [Tr(int(round(int(term.coefficient) ** 0.5, 6)), ML.build_from_dict({letter:
                         term.literals.literals_dict[letter] // 2 for letter in term.literals.literals_dict}))
                         for term in terms]
                # build reduced LPN objects
                return [LPN([terms[0], terms[1]]), LPN([terms[0], -terms[1]])]
        return None

    # TESTED
    @staticmethod
    def _verify_case3_b_match(elem):
        # case 3-b
        # possible if:
        #   - two terms
        #   - opposite signs (order in a new list without the sign)
        #   - perfect cubes
        # check opposite sign
        if len(elem.terms) != 2:
            return None
        if (elem.terms[0].coefficient > 0) != (elem.terms[1].coefficient > 0):
            # build list
            terms = [elem.terms[0], -elem.terms[1]] if elem.terms[1].coefficient < 0 else \
                [elem.terms[1], -elem.terms[0]]
            # coefficients in terms are all positive
            # check if perfect cubes
            for term in terms:
                if not term.is_perfect_cube:
                    break
            # conditions matched -> proceed to reduction
            else:
                # build two new LPN objects
                # terms of first LPN
                terms_one = [Tr(int(round(int(terms[0].coefficient) ** (1 / 3), 6)), ML.build_from_dict({letter:
                                terms[0].literals.literals_dict[letter] // 3
                                for letter in terms[0].literals.literals_dict})),
                             Tr(-int(round(int(terms[1].coefficient) ** (1 / 3), 6)), ML.build_from_dict({letter:
                                terms[1].literals.literals_dict[letter] // 3
                                for letter in terms[1].literals.literals_dict}))]
                terms_two = [terms_one[0] * terms_one[0], -terms_one[0] * terms_one[1],
                             terms_one[1] * terms_one[1]]
                return [LPN(terms_one), LPN(terms_two)]
        return None

    # TESTED
    @staticmethod
    def _verify_case3_c_match(elem):
        # case 3-c
        # possible if:
        #   - two terms
        #   - same signs (order in a new list without the sign)
        #   - perfect cubes
        # check same sign
        if len(elem.terms) != 2:
            return None
        if (elem.terms[0].coefficient > 0) == (elem.terms[1].coefficient > 0):
            # build list
            terms = elem.terms
            # check if perfect cubes -> coefficients must be positive
            # if negative change signs and store change
            changed_sign = False
            if elem.terms[0].coefficient < 0:
                changed_sign = True
                terms = [-term for term in terms]
            for term in terms:
                if not term.is_perfect_cube:
                    break
            # conditions matched -> proceed to reduction
            else:
                # build two new LPN objects
                # terms of first LPN
                terms_one = [Tr(int(round(int(terms[0].coefficient) ** (1 / 3), 6)), ML.build_from_dict({letter:
                                terms[0].literals.literals_dict[letter] // 3
                                for letter in terms[0].literals.literals_dict})),
                             Tr(int(round(int(terms[1].coefficient) ** (1 / 3), 6)), ML.build_from_dict({letter:
                                terms[1].literals.literals_dict[letter] // 3
                                for letter in terms[1].literals.literals_dict}))]
                terms_two = [terms_one[0] * terms_one[0], -terms_one[0] * terms_one[1],
                             terms_one[1] * terms_one[1]]
                return [LPN(terms_one), LPN(terms_two)] if not changed_sign else \
                    [LPN([-1]), LPN(terms_one), LPN(terms_two)]
        return None

    # TESTED
    @staticmethod
    def _verify_case4_match(elem):
        # try to rebuild the binomial cube formula
        #    -> +/- a3 +/- b3 +/- 3a2b -/+ 3ab2
        # 4 terms needed
        if len(elem.terms) == 4:
            # assign new terms value and generators terms (a, b) list with None values
            terms, term = list(tuple(elem.terms)), Tr()
            generators, p = [None, None], 0
            # loop terms and check
            # 1 - a3
            # 2 - b3
            # 3 - 3a2b
            # 4 - 3ab2
            # to be sure that the correct pattern is found, may as well do 4 test, with different orders in terms
            for _ in range(4):
                # rotate terms
                terms = [terms[-1]] + terms[:-1]
                for p in range(4):
                    # loop terms -> if not found -> break
                    for term in terms:
                        if p == 0:
                            if term.is_perfect_cube:
                                generators[0] = LPN([Tr(term.coefficient.cbrt(),
                                                     ML([Li(li.letter, li.exponent // 3) for li in term.literals]))])
                                break
                        elif p == 1:
                            if term.is_perfect_cube:
                                generators[1] = LPN([Tr(term.coefficient.cbrt(),
                                                     ML([Li(li.letter, li.exponent // 3) for li in term.literals]))])
                                break
                        elif p == 2:
                            # look for 3a2b
                            # can divide by 3, a, a, b
                            if term == 3 * generators[0] * generators[0] * generators[1]:
                                break
                        elif p == 3:
                            # look for 3ab2
                            # can divide by 3, a, b, b
                            if term == 3 * generators[0] * generators[1] * generators[1]:
                                break
                    else:
                        p = 4
                        break
                    terms.remove(term)
                if p == 3:
                    # successful validation
                    a, b = generators[0], generators[1]
                    return [a + b, a + b, a + b]
        return None

    @staticmethod
    def _verify_case5_match(elem):
        # try to rebuild the trinomial square formula
        #    -> a2 + b2 + c2 + 2ab + 2ac + 2bc
        # 6 terms needed
        if len(elem.terms) == 6:
            # assign new terms value and generators terms (a, b, c) list with None values
            terms, term = list(tuple(elem.terms)), Tr()
            generators, p = [None, None, None], 0
            products = [None, None, None]
            # loop terms and check
            # 1 - a2
            # 2 - b2
            # 3 - c2
            # 4 - 2ab
            # 5 - 2ac
            # 6 - 2bc
            # to be sure that the correct pattern is found, may as well do 6 test, with different orders in terms
            # when a, b and c are defined, their sign is still unknown, and it needs to be determined by the parsing of
            # the other three terms
            for _ in range(6):
                # rotate terms
                terms = [terms[-1]] + terms[:-1]
                for p in range(6):
                    # loop terms -> if not found -> break
                    for i, term in enumerate(terms):
                        if term:
                            if p == 0:
                                if term.is_perfect_square:
                                    generators[0] = LPN([Tr(term.coefficient.sqrt(),
                                                        ML([Li(li.letter, li.exponent // 2) for li in term.literals]))])
                                    break
                            elif p == 1:
                                if term.is_perfect_square:
                                    generators[1] = LPN([Tr(term.coefficient.sqrt(),
                                                        ML([Li(li.letter, li.exponent // 2) for li in term.literals]))])
                                    break
                            elif p == 2:
                                if term.is_perfect_square:
                                    generators[2] = LPN([Tr(term.coefficient.sqrt(),
                                                        ML([Li(li.letter, li.exponent // 2) for li in term.literals]))])
                                    break
                            elif p == 3:
                                # look for 2ab
                                # can divide by 2, a, b
                                if Tr(abs(term.coefficient), term.literals) == 2 * generators[0] * generators[1]:
                                    products[0] = term
                                    break
                            elif p == 4:
                                # look for 2ac
                                # can divide by 2, a, c
                                if Tr(abs(term.coefficient), term.literals) == 2 * generators[0] * generators[2]:
                                    products[1] = term
                                    break
                            elif p == 5:
                                # look for 2bc
                                # can divide by 2, b, c
                                if Tr(abs(term.coefficient), term.literals) == 2 * generators[1] * generators[2]:
                                    products[2] = term
                                    break
                    else:
                        p = 6
                        break
                    if p < 4:
                        terms.remove(term)
                        terms.insert(i, None)
                if p == 5:
                    # successful validation
                    a, b, c = generators[0], generators[1], generators[2]
                    # get signs by parsing products list
                    # if [+ + +] -> every generator positive (as it already is)
                    # if [- + -] -> b negative
                    if products[0].coefficient < 0 < products[1].coefficient and products[2].coefficient < 0:
                        b = -b
                    # if [- - +] -> a negative
                    elif products[0].coefficient < 0 < products[2].coefficient and products[1].coefficient < 0:
                        a = -a
                    # if [+ - -] -> c negative
                    elif products[1].coefficient < 0 < products[0].coefficient and products[2].coefficient < 0:
                        c = -c
                    # (actually in every one of these cases the signs could be inverted, but the result will always
                    # be the same one)
                    else:
                        return None
                    return [a + b + c, a + b + c]
        return None

    @staticmethod
    def integer_divisors(num):
        if not num.is_integer:
            raise Error.OperationError('Unable to get divisors of {} RN object, must be integer'.format(str(num)))
        for n in range(1, abs(int(num)) + 1):
            if not num % n:
                yield RN(n)

    @staticmethod
    def _get_possible_zeros(max_degree_term, constant_term):
        n = _Lcl.integer_divisors(constant_term)
        for num in n:
            for den in _Lcl.integer_divisors(max_degree_term):
                yield num / den
                yield -num / den

    @staticmethod
    def _apply_ruffini(coefficients, zero):
        # validate arguments
        if not all(isinstance(coefficient, RN) for coefficient in coefficients) and isinstance(zero, RN):
            raise Error.ArgumentError('Bad user argument, must be List[RN], RN for _Lcl._apply_ruffini method')
        r1 = coefficients
        r2, r3 = [0] + [0 for _ in range(len(r1) - 1)], [None for _ in r1]
        # iter
        for p, coefficient in enumerate(r1):
            # noinspection PyTypeChecker
            r3[p] = coefficient + r2[p]
            try:
                # noinspection PyTypeChecker
                r2[p + 1] = r3[p] * zero
            except IndexError:
                continue
        if r3[-1] != 0:
            raise Error.ArgumentError('Bad user argument, zero parameter is not a zero of coefficients LPN')
        return r3[:-1]

    # could get it to work with multi variable elements
    # TESTED
    @staticmethod
    def _verify_case6_match(elem):
        # verify and apply ruffini
        # -> if integer coefficients
        # -> if MONO VARIABLE
        if elem.is_mono_variable and all([term.coefficient.is_integer for term in elem.terms]):
            variable = [letter for letter in elem.parameters][0]
            # get possible zeros
            possible_zeros = _Lcl._get_possible_zeros(elem.terms[-1].coefficient,
                                                      (elem.terms[0].coefficient if elem.has_constant_term else RN(0)))
            # get actual zero
            for n in possible_zeros:
                # elem is MONO VARIABLE so parameters only contains one letter
                if elem.eval_to({variable: n}) == 0:
                    zero = n
                    break
            else:
                return None
            # apply ruffini
            reduced_coefficients = _Lcl._apply_ruffini([term.coefficient
                                                        for term in elem.complete_and_ordered(variable)], zero)
            reduced_literals = [ML([Li(variable, exp)]) for exp in range(elem.degree)]
            reduced_literals.reverse()
            return [LPN([Tr(1, ML([Li(variable, 1)])), -zero]),
                    LPN([Tr(coefficient, literal) for coefficient, literal in
                         zip(reduced_coefficients, reduced_literals)])]
        return None

    @staticmethod
    def get_pn_domain(reduced_denominator):
        # parent pn must be mono variable
        zeros = {}
        for factor in reduced_denominator:
            # x -> root = 0
            if len(factor.terms) == 1 and not factor.is_constant:
                zeros |= {RN(0)}
            # bx - a -> root = a/b
            elif len(factor.terms) == 2 and factor.degree == 1:
                zeros |= {-factor.terms[0].coefficient / factor.terms[1].coefficient}
            # bxN - a -> root = (a/b) ** 1/N
            elif len(factor.terms) == 2 and factor.terms[0].is_constant and factor.degree == 2:
                try:
                    zeros |= {(-factor.terms[0].coefficient / factor.terms[1].coefficient).sqrt()}
                except RnError.OperationError:
                    continue
                except NotImplementedError:
                    continue
            elif len(factor.terms) == 2 and factor.terms[0].is_constant and factor.degree == 3:
                try:
                    zeros |= {(-factor.terms[0].coefficient / factor.terms[1].coefficient).cbrt()}
                except RnError.OperationError:
                    continue
                except NotImplementedError:
                    continue
        zeros = list(zeros)
        zeros.sort()
        simple_intervals = [SI(-inf, zero) for zero in zeros] + [SI(zero, inf) for zero in zeros]
        domain = Interval([SI(-inf, inf)])
        for p in range(len(simple_intervals)):
            domain &= Interval([simple_intervals[p]])
        return domain


class Li:
    """
    unary literal -> letter + exponent
    """

    def __init__(self, letter, exponent=1):
        _Lcl.validate_letter(letter)
        self.letter = letter
        self.exponent = _Lcl.convert_to_integer(exponent)
        if self.exponent == '':
            Error.raise_argument_error(self.__class__.__name__, 'exponent', [RN, int, float, Fraction, Decimal],
                                       exponent)

    def __str__(self):
        return self.letter + '^(' + str(self.exponent) + ')'

    def __repr__(self):
        return 'Li(' + repr(self.letter) + ', ' + repr(self.exponent) + ')'

    def __bool__(self):
        return self.exponent != 0

    def __int__(self):
        return ord(self.letter) * abs(self.exponent)

    # comparisons
    @assert_other
    def is_compatible(self, other):
        """
        compatible if can be multiplied for other
        -> if they have the same letter
        """
        return self.letter == other.letter

    @assert_other
    def __eq__(self, other):
        return self.letter == other.letter and self.exponent == other.exponent

    @assert_other
    def __gt__(self, other):
        if self.letter > other.letter:
            return True
        elif self.letter == other.letter:
            return self.exponent > other.exponent
        return False

    # operations
    @assert_other
    def __mul__(self, other):
        if self.is_compatible(other):
            return Li(self.letter, self.exponent + other.exponent)
        return NotImplemented


class ML:
    """
    multiple literal -> list of literals
    """

    def __init__(self, literals):
        if literals is None:
            literals = []
        _Lcl.validate_ml(literals)
        self.literals = _Lcl.parse_ml_data(literals)

    def __str__(self):
        return ''.join(list(map(lambda i: str(i), self.literals)))

    def __repr__(self):
        return 'ML([' + ', '.join(list(map(lambda i: repr(i), self.literals))) + '])'

    def __bool__(self):
        return True if self.literals_dict else False

    def __iter__(self):
        for literal in self.literals:
            yield literal

    def __int__(self):
        return sum([int(literal) for literal in self.literals])

    # properties
    @property
    def degree(self):
        return sum([literal.exponent for literal in self.literals]) if self.literals else 0

    @property
    def literals_dict(self):
        return {literal.letter: literal.exponent for literal in self.literals}

    @staticmethod
    def build_from_dict(literals_dict):
        return ML([Li(letter, literals_dict[letter]) for letter in literals_dict])

    # comparisons
    @assert_other
    def __eq__(self, other):
        return self.literals == other.literals

    @assert_other
    def __gt__(self, other):
        return int(self) > int(other)

    # operations
    @assert_other
    def is_divisible(self, other):
        """divisible if every letter in self is also in other
        and each letter has a lower (or equal) exponent in other than in self"""
        # assert each letter of other is also in self
        for letter in other.literals_dict:
            try:
                _ = self.literals_dict[letter]
                # assert it has a lower (or equal) exponent than in self
                assert _ >= other.literals_dict[letter]
            except KeyError:
                return False
            except AssertionError:
                return False
        return True

    @assert_other
    def __mul__(self, other):
        return ML(self.literals + other.literals)

    @assert_other
    def __truediv__(self, other):
        if not self.is_divisible(other):
            raise Error.OperationError('Unable to divide {} for {}, they are not divisible'
                                       .format(str(self), str(other)))
        # divide
        LITERALS = []
        for letter in self.literals_dict:
            try:
                LITERALS += [Li(letter, self.literals_dict[letter] - other.literals_dict[letter])]
            except KeyError:
                LITERALS += [Li(letter, self.literals_dict[letter])]
        return ML(LITERALS)


class Tr:
    """
    term class -> coefficient (RN) + literal (ML)
    """

    def __init__(self, coefficient=RN(1), literals=ML([])):
        self.coefficient = _Lcl.convert_to_RN(coefficient)
        if self.coefficient == '':
            Error.raise_argument_error(self.__class__.__name__, 'coefficient',
                                       [RN, int, float, Fraction, Decimal], coefficient)
        if not isinstance(literals, ML):
            Error.raise_argument_error(self.__class__.__name__, 'literals', [ML], literals)
        self.literals = literals
        # no parsing is needed, both values should be already been reduced by their class parsers

    def __str__(self):
        return str(self.coefficient) + str(self.literals)

    def __repr__(self):
        return 'Tr(' + repr(self.coefficient) + ', ' + repr(self.literals) + ')'

    def __bool__(self):
        return bool(self.coefficient)

    def __iter__(self):
        # only if integer
        if not self.is_integer:
            raise Error.OperationError('Unable to iterate through {} Tr object, must be integer'.format(str(self)))
        for i in self.coefficient:
            yield i

    # properties
    @property
    def degree(self):
        return self.literals.degree

    def variable_degree(self, variable):
        if self.literals:
            _Lcl.validate_variable(self.parameters, variable)
            return self.literals.literals_dict[variable]
        return 0

    @property
    def is_constant(self):
        """constant if it is a number, without a literal part"""
        return not self.literals

    @property
    def is_integer(self):
        """integer if constant and coefficient is integer"""
        return self.is_constant and self.coefficient.is_integer

    # reduction properties
    @property
    def parameters(self):
        """return set of variables"""
        return {literal.letter for literal in self.literals}

    @property
    def has_rational_coefficient(self):
        return self.coefficient.is_rational

    @property
    def is_perfect_square(self):
        if self.coefficient.is_integer and self.coefficient > 0:
            if int(round(int(self.coefficient) ** 0.5, 6)) == round(int(self.coefficient) ** 0.5, 6):
                for letter in self.parameters:
                    if self.literals.literals_dict[letter] % 2 != 0:
                        return False
                return True
        return False

    @property
    def is_perfect_cube(self):
        if self.coefficient.is_integer:
            if int(round(int(abs(self.coefficient)) ** (1/3), 6)) == round(int(abs(self.coefficient)) ** (1/3), 6):
                for letter in self.parameters:
                    if self.literals.literals_dict[letter] % 3 != 0:
                        return False
                return True
        return False

    # comparisons
    @assert_other
    def __eq__(self, other):
        return self.coefficient == other.coefficient and self.literals == other.literals

    @assert_other
    def __gt__(self, other):
        if self.literals > other.literals:
            return True
        elif self.literals == other.literals:
            if self.coefficient.is_rational == other.coefficient.is_rational:
                # both rational or (not rational) irrational
                return self.coefficient > other.coefficient
            else:
                # either one rational and the other irrational or one irrational and the other rational
                # if self is rational -> other is irrational -> other is greater
                return not self.coefficient.is_rational
        return False

    # operations
    # will define operations and r-operations:
    # - Tr
    # - numbers: RN, int, float, Fraction, Decimal
    # use custom assert_other decorator
    @assert_tr_other
    def is_compatible(self, other):
        """compatible if self and other sum can be a Tr object
           if other is Term:
           -> if the have the same literals
           if other is number:
           -> if self is constant
        """
        if isinstance(other, Tr):
            return self.literals == other.literals
        elif any(isinstance(other, tp) for tp in [RN, int, float, Fraction, Decimal]):
            return self.is_constant
        return NotImplemented

    @assert_tr_other
    def is_divisible(self, other):
        """divisible if the literals of other are compatible"""
        if isinstance(other, Tr):
            return self.literals.is_divisible(other.literals)
        elif any(isinstance(other, tp) for tp in [RN, int, float, Fraction, Decimal]):
            return True
        return NotImplemented

    def __neg__(self):
        return Tr(-self.coefficient, self.literals)

    @assert_tr_other
    def __add__(self, other):
        # check for compatibility (will accept numbers too)
        if self.is_compatible(other):
            if isinstance(other, Tr):
                return Tr(self.coefficient + other.coefficient, self.literals)
            elif any(isinstance(other, tp) for tp in [RN, int, float, Fraction, Decimal]):
                return Tr(self.coefficient + other, self.literals)
        return NotImplemented

    @assert_tr_other
    def __sub__(self, other):
        # check for compatibility (will accept numbers too)
        if self.is_compatible(other):
            if isinstance(other, Tr):
                return Tr(self.coefficient - other.coefficient, self.literals)
            elif any(isinstance(other, tp) for tp in [RN, int, float, Fraction, Decimal]):
                return Tr(self.coefficient - other, self.literals)
        return NotImplemented

    @assert_tr_other
    def __mul__(self, other):
        # if other is term -> product of both coefficients and literals
        if isinstance(other, Tr):
            return Tr(self.coefficient * other.coefficient, self.literals * other.literals)
        # if other is number -> product only of coefficients
        elif any(isinstance(other, tp) for tp in [RN, int, float, Fraction, Decimal]):
            return Tr(self.coefficient * other, self.literals)
        return NotImplemented

    @assert_tr_other
    def __truediv__(self, other):
        if not self.is_divisible(other):
            raise Error.OperationError('Unable to divide {} for {}, they are not divisible'
                                       .format(str(self), str(other)))
        # divide
        # if other is Tr -> divide literals too
        if isinstance(other, Tr):
            return Tr(self.coefficient / other.coefficient, self.literals / other.literals)
        # if other is number -> divide only coefficients
        if any(isinstance(other, tp) for tp in [RN, int, float, Fraction, Decimal]):
            return Tr(self.coefficient / other, self.literals)
        return NotImplemented

    # r-operations
    # will get numbers -> turn to Tr
    @assert_tr_other
    def __radd__(self, other):
        return Tr(other) + self

    @assert_tr_other
    def __rsub__(self, other):
        return Tr(other) - self

    @assert_tr_other
    def __rmul__(self, other):
        return Tr(other) * self

    # evaluation method (still operation)
    def eval_to(self, literals_dict):
        """return the evaluation of the literals of self to the values specified"""
        _Lcl.validate_literals_dict(self.literals, literals_dict, self.__class__)
        value = 1
        for literal in self.literals:
            value *= literals_dict[literal.letter] ** literal.exponent
        return value * self.coefficient

    # GCD of another term
    def GCD(self, other):
        # only defined for other = Tr
        if not isinstance(other, Tr):
            Error.raise_argument_error(self.__class__.__name__, 'other', [Tr], other)
        return _Lcl.get_tr_GCD(self, other)


class LPN:
    """
    linear polynomial class
    """

    def __init__(self, terms):
        """
        will expect:
        - list of terms obj
        - string -> validator and parser
        """
        _Lcl.validate_lpn(terms)
        self.terms = _Lcl.parse_lpn_data(terms)
        if not self.terms:
            self.terms = [Tr(0)]

    def __str__(self):
        return ''.join(list(map(lambda i: str(i), self.terms)))

    def __repr__(self):
        # return 'LPN([' + ', '.join(list(map(lambda i: repr(i), self.terms))) + '])'
        return str(self)

    def __bool__(self):
        """self is none if terms list is empty (None items are deleted in parsing)"""
        return self.terms[0] != Tr(0)

    def __iter__(self):
        # only if integer
        if not self.is_integer:
            raise Error.OperationError('Unable to iterate through {} LPN object, must be integer'.format(str(self)))
        for i in self.terms[0]:
            yield i

    def __call__(self, other):
        return self * other

    # properties
    @property
    def degree(self):
        return max([term.degree for term in self.terms])

    def variable_degree(self, variable):
        if self.parameters:
            _Lcl.validate_variable(self.parameters, variable)
            return max([term.variable_degree(variable) for term in self.terms if variable in term.parameters])
        return 0

    @property
    def is_constant(self):
        """if constant -> only one term, which is constant"""
        return len(self.terms) == 1 and self.terms[0].is_constant

    @property
    def is_integer(self):
        """integer if constant and term is integer"""
        return self.is_constant and self.terms[0].is_integer

    # reduction related properties
    @property
    def parameters(self):
        """return set of all variables in terms"""
        parameters = set()
        for term in self.terms:
            parameters |= term.parameters
        return parameters

    @property
    def is_mono_variable(self):
        """true if only one variable in terms"""
        return len(self.parameters) == 1

    @property
    def has_rational_coefficients(self):
        for term in self.terms:
            if not term.has_rational_coefficient:
                return False
        return True

    @property
    def has_constant_term(self):
        for term in self.terms:
            if term.is_constant:
                return True
        return False

    @property
    def denominators_LCM(self):
        """return LCM of denominators of terms"""
        return RN(LCM([int(term.coefficient.denominator) for term in self.terms]))

    @property
    def terms_GCD(self):
        """return Greatest Common Divisor between the terms -> coefficients_GCD and literals_GCD"""
        return _Lcl.get_lpn_terms_GCD(self.terms)

    # method (but property-like)
    def complete_and_ordered(self, variable):
        """return list of complete / ordered terms in relation to a gaven variable"""
        if not (isinstance(variable, str) and len(variable) == 1):
            raise Error.ArgumentError('Bad user argument, variable must be a char, got {}'.format(variable))
        if variable not in self.parameters:
            return self.terms
        return _Lcl.lpn_complete_terms(_Lcl.lpn_ordered_terms(self.terms, variable), variable)

    # comparisons
    # will define eq for
    # - LPN
    # - Tr
    # - numbers -> RN, int, float, Fraction, Decimal
    @assert_lpn_other
    def __eq__(self, other):
        # if other is LPN -> same terms list (sorted)
        if isinstance(other, LPN):
            return self.terms == other.terms
        # if other is Tr -> same terms[0] if self has only one terms
        elif isinstance(other, Tr):
            return self.terms[0] == other and len(self.terms) == 1
        # if other is number -> same terms[0].coefficient and self is constant
        elif any(isinstance(other, tp) for tp in [RN, int, float, Fraction, Decimal]):
            return self.terms[0].coefficient == other and self.is_constant

    # operations
    # will define operations and r-operations of:
    # - LPN
    # - Tr
    # - numbers -> RN, int, float, Fraction, Decimal
    def __neg__(self):
        """-term for term in self.terms"""
        return LPN([-term for term in self.terms])

    @assert_lpn_other
    def __add__(self, other):
        # if other is LPN -> add terms list
        if isinstance(other, LPN):
            return LPN(self.terms + other.terms)
        # if other is Tr or number -> add to terms list
        elif any(isinstance(other, tp) for tp in [Tr, RN, int, float, Fraction, Decimal]):
            return LPN(self.terms + [other])
        return NotImplemented

    @assert_lpn_other
    def __sub__(self, other):
        # other should have __neg__ defined
        return self + (-other)

    @assert_lpn_other
    def __mul__(self, other):
        # if other is LPN -> double loop
        if isinstance(other, LPN):
            _terms = []
            for term in self.terms:
                for TERM in other.terms:
                    _terms += [term * TERM]
            return LPN(_terms)
        # if other is Tr or number -> mul every item in terms
        if any(isinstance(other, tp) for tp in [Tr, RN, int, float, Fraction, Decimal]):
            return LPN(list(map(lambda i: i * other, self.terms)))
        return NotImplemented

    # won't define truediv as it is representable only as a fraction of LPNs
    @assert_lpn_other
    def __floordiv__(self, other):
        # if other is LPN or Tr -> division algorithm
        if isinstance(other, Tr):
            if other.is_constant:
                other = other.coefficient
            elif all(term.is_divisible(other) for term in self.terms):
                return LPN([term / other for term in self.terms])
            else:
                other = LPN([other])
        if isinstance(other, LPN):
            return _Lcl.lpn_division_algorithm(self, other)[0]
        # if other is number -> divide each term of self for other
        elif any(isinstance(other, tp) for tp in [RN, int, float, Fraction, Decimal]):
            return LPN([term / other for term in self.terms])
        return NotImplemented

    @assert_lpn_other
    def __mod__(self, other):
        # if other is LPN or Tr -> division algorithm
        if isinstance(other, Tr):
            other = LPN([other])
        if isinstance(other, LPN):
            return _Lcl.lpn_division_algorithm(self, other)[1]
        # if other is number -> divide each term of self for other
        elif any(isinstance(other, tp) for tp in [RN, int, float, Fraction, Decimal]):
            return LPN([0])
        return NotImplemented

    @assert_lpn_other
    def __pow__(self, power, modulo=None):
        # power must be integer
        # if power is LPN or Tr or RN -> iter
        if any(isinstance(power, tp) for tp in [LPN, Tr, RN]):
            if not power.is_integer:
                raise Error.MissingImplementationError('Powers of non-integers polynomials is yet to be implemented, '
                                                       'unable to get {} elevated to the power of {}'.format(
                                                        str(self), str(power)))
            n = LPN([1])
            for _ in power:
                n *= self
            return n
        # if power is simple number -> assert is integer and then iter
        elif any(isinstance(power, tp) for tp in [int, float, Fraction, Decimal]):
            if not int(power) == power:
                raise Error.MissingImplementationError('Powers of non-integer polynomials is yet to be implemented,'
                                                       'unable to get {} elevated to the power of {}'
                                                       .format(str(self), str(power)))
            n = LPN([1])
            power = int(power)
            for _ in range(power):
                n *= self
            return n
        return NotImplemented

    # r-operations
    # won't define rfloordiv and rmod
    # - LPN
    # - Tr
    # - numbers -> RN, int, float, Fraction, Decimal
    @assert_lpn_other
    def __radd__(self, other):
        if any(isinstance(other, tp) for tp in [Tr, int, float, Fraction, Decimal, RN]):
            return LPN(self.terms + [other])
        return NotImplemented

    @assert_lpn_other
    def __rsub__(self, other):
        if any(isinstance(other, tp) for tp in [Tr, int, float, Fraction, Decimal, RN]):
            return LPN([-term for term in self.terms] + [other])
        return NotImplemented

    @assert_lpn_other
    def __rmul__(self, other):
        if any(isinstance(other, tp) for tp in [Tr, int, float, Fraction, Decimal, RN]):
            return self * LPN([other])
        return NotImplemented

    @assert_lpn_other
    def __rpow__(self, other):
        if any(isinstance(other, tp) for tp in [Tr, int, float, Fraction, Decimal, RN]):
            # assert power is integer
            if not self.is_integer:
                raise Error.MissingImplementationError('Powers of non-integers polynomials is yet to be implemented,'
                                                       'unable to get {} elevated to the power of {}'
                                                       .format(str(other), str(self)))
            return LPN([other]) ** self
        return NotImplemented

    # evaluation method (still operation)
    def eval_to(self, literals_dict):
        # for each term in terms -> filter literal dict, use Tr.eval_to method
        _Lcl.validate_literals_dict(self.parameters, literals_dict, self.__class__)
        value = RN(0)
        for term in self.terms:
            value += term.eval_to(_Lcl.filter_lpn_literals_dict(literals_dict, term))
        return value


class PN:
    """
    actual pn class -> LPN / LPN
    """

    def __init__(self, numerator, denominator=LPN([1]), domain_inheritance=Interval([SI(-inf, inf)])):
        # validate data
        # convert to LPN if possible
        numerator, denominator = _Lcl.convert_to_LPN(numerator), _Lcl.convert_to_LPN(denominator)
        if numerator == '':
            Error.raise_argument_error(self.__class__.__name__, 'numerator',
                                       [LPN, Tr, RN, int, float, Fraction, Decimal], numerator)
        if denominator == '':
            Error.raise_argument_error(self.__class__.__name__, 'denominator',
                                       [LPN, Tr, RN, int, float, Fraction, Decimal], denominator)
        # parse data
        # noinspection PyTypeChecker
        # num and den are LPN (else error is raised)
        self.numerator, self.denominator = _Lcl.parse_pn_data(numerator, denominator)
        # set instance domain inheritance
        self.domain_inheritance = domain_inheritance

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __bool__(self):
        return bool(self.numerator)

    @assert_pn_other
    def __call__(self, other):
        return self * other

    def __iter__(self):
        # only if integer
        if not self.is_integer:
            raise Error.OperationError('Unable to iterate through {} PN object, must be integer'.format(str(self)))
        for i in self.numerator:
            yield i

    # properties
    @property
    def degree(self):
        return max([self.numerator.degree, self.denominator.degree])

    def variable_degree(self, variable):
        _Lcl.validate_variable(self.parameters, variable)
        if variable not in self.numerator.parameters:
            return self.denominator.variable_degree(variable)
        elif variable not in self.denominator.parameters:
            return self.numerator.variable_degree(variable)
        return max([self.numerator.variable_degree(variable), self.denominator.variable_degree(variable)])

    @property
    def is_constant(self):
        """constant if no parameters"""
        return len(self.parameters) == 0

    @property
    def is_integer(self):
        """integer if constant and -> den == 1"""
        return self.numerator.is_integer and self.denominator == 1

    @property
    def parameters(self):
        """union of parameters of num and den"""
        return self.numerator.parameters | self.denominator.parameters

    @property
    def is_mono_variable(self):
        return len(self.parameters) == 1

    @property
    def has_rational_coefficients(self):
        return self.numerator.has_rational_coefficients and self.denominator.has_rational_coefficients

    @property
    def has_integer_coefficients(self):
        return all(term.coefficient.is_integer for term in self.numerator.terms + self.denominator.terms) \
            if self.has_rational_coefficients else False

    @property
    def has_numerator(self):
        """has numerator if num != 0"""
        return self.numerator != 0

    @property
    def has_denominator(self):
        """has denominator if den != 1"""
        return self.denominator != 1

    @property
    def domain(self):
        # dependent from object history
        for factor in self.reduce[1]:
            if not factor.is_mono_variable:
                return self.domain_inheritance
        return _Lcl.get_pn_domain(self.reduce[1]) & self.domain_inheritance

    @property
    def reduce(self):
        # num and den (after parsing) have:
        # - integer coefficients
        # - a GCD equal to 1
        # parse for special types
        # use special parsing or pure reduction
        # simplify equal items in num and den to get reduced form
        reduced = _Lcl.reduce_pn(self.numerator, self.denominator)
        return reduced

    @property
    def mutual(self):
        return PN(self.denominator, self.numerator)

    # comparisons
    @assert_pn_other
    def __eq__(self, other):
        pass

    # operations
    # define for:
    # - PN
    # - LPN
    # - Tr
    # - numbers
    def __neg__(self):
        return PN(-self.numerator, self.denominator)

    @assert_pn_other
    def __add__(self, other):
        """return self.num * other.den + other.num + self.den and self.den * other.den"""
        # if other is LPN or number -> turn to PN
        if any(isinstance(other, tp) for tp in [LPN, Tr, RN, int, float, Fraction, Decimal]):
            other = PN(other)
        if isinstance(other, PN):
            return PN(self.numerator * other.denominator + other.numerator * self.denominator,
                      self.denominator * other.denominator, self.domain_inheritance & other.domain_inheritance)
        return NotImplemented

    @assert_pn_other
    def __sub__(self, other):
        return self + (-other)

    @assert_pn_other
    def __mul__(self, other):
        """return self.num * other.num and self.den + other.den"""
        # if other is LPN or number -> turn to PN
        if any(isinstance(other, tp) for tp in [LPN, Tr, RN, int, float, Fraction, Decimal]):
            other = PN(other)
        if isinstance(other, PN):
            return PN(self.numerator * other.numerator, self.denominator * other.denominator,
                      self.domain_inheritance & other.domain_inheritance)
        return NotImplemented

    @assert_pn_other
    def __truediv__(self, other):
        """return inverted product"""
        # if other is LPN or number -> turn to PN
        if any(isinstance(other, tp) for tp in [LPN, RN, Tr, int, float, Fraction, Decimal]):
            other = PN(other)
        if isinstance(other, PN):
            return self * other.mutual
        return NotImplemented

    @assert_pn_other
    def __pow__(self, power, modulo=None):
        # power must be integer
        # if power is LPN or Tr or RN -> iter
        if any(isinstance(power, tp) for tp in [PN, LPN, Tr, RN]):
            if not power.is_integer:
                raise Error.MissingImplementationError('Powers of non-integers polynomials is yet to be implemented, '
                                                       'unable to get {} elevated to the power of {}'.format(
                                                        str(self), str(power)))
            n = PN(1)
            for _ in power:
                n *= self
            return n
        # if power is simple number -> assert is integer and then iter
        elif any(isinstance(power, tp) for tp in [int, float, Fraction, Decimal]):
            if not int(power) == power:
                raise Error.MissingImplementationError('Powers of non-integer polynomials is yet to be implemented,'
                                                       'unable to get {} elevated to the power of {}'
                                                       .format(str(self), str(power)))
            n = PN(1)
            power = int(power)
            for _ in range(power):
                n *= self
            return n
        return NotImplemented

    def eval_to(self, literals_dict):
        _Lcl.validate_literals_dict(self.parameters, literals_dict, self.__class__)
        return self.numerator.eval_to(_Lcl.filter_lpn_literals_dict(literals_dict, self.numerator)) \
               / self.denominator.eval_to(_Lcl.filter_lpn_literals_dict(literals_dict, self.denominator))

    # r-operations
    # define for:
    # - LPN
    # - Tr
    # - numbers
    @assert_pn_other
    def __radd__(self, other):
        return PN(other) + self

    @assert_pn_other
    def __rsub__(self, other):
        return PN(other) - self

    @assert_pn_other
    def __rmul__(self, other):
        return PN(other) * self

    @assert_pn_other
    def __rtruediv__(self, other):
        return PN(other) / self

    @assert_pn_other
    def __rpow__(self, other):
        return PN(other) ** self
