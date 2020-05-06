"""
Evaluable Expression module

getting PN class for pn.py

main module for the creation of complex expression passed as a human-like language string, which is then parsed

classes defined here:
    Ex (Expression class)

    _Lcl (local useful methods)
    Errors (local mathematical errors)
"""


from sys import version
import re
from .func import char_indexes
from .tr import TR
from ..engine.pn.pn import PN, LPN, Tr, ML, Li
from ..engine.rn.rn import RN, RNU


__author__ = 'Viganò Andrea'
__version__ = 'ex module 1.6 for ACE 0.1.0 official release for Python {}'.format(version)


# Local errors class
class Error:
    class ValidationError(Exception):
        pass


# Local methods
class _Lcl:
    @staticmethod
    def validate_text(text):
        # validate symbols
        data = _Lcl.validate_symbols(text)
        if not data[0]:
            raise Error.ValidationError('Bad user symbol {} for expression object text'.format(data[1]))
        # validate expressions patterns
        data = _Lcl.validate_pattern(text)
        if not data[0]:
            raise Error.ValidationError('Bad user text pattern for expression object text\n'
                                        '{}\n'
                                        '{}^'.format(text, ' ' * data[1]))

    @staticmethod
    def validate_symbols(text):
        for ch in text:
            if not re.match(r'([0-9a-z+/*^.,\-(){}[\]√ ])', ch):
                return False, ch
        return True, None

    @staticmethod
    def validate_pattern(text):
        # base Ex pattern
        #    -> expression of PN objects (numerator)/(denominator)
        #    -> where numerator and denominator are generic LPN expression (linear polynomials)
        #    -> need to determinate what characters can be found after another character
        #    -> ensure that brackets degree is null at the end of parsing
        # Set 'expectations' values
        # Set 'default expectations' -> open brackets / number / literal / signs

        # remove whitespaces
        text = text.replace(' ', '')

        # assign default values
        expectations = re.compile(r'([0-9a-z(\[{+\- ])')
        degree, ch = 0, ''

        # iter
        for p, ch in enumerate(text):
            if not re.match(expectations, ch):
                return False, p
            # update degree value
            degree += 1 if ch in '([{' else 0
            degree -= 1 if ch in ')]}' else 0
            # assign new expectations depending on ch nature
            # open brackets
            if ch in '([{':
                expectations = re.compile(r'([0-9a-z(\[{+\-])')
            # closed brackets
            elif ch in ')}':
                expectations = re.compile(r'([0-9a-z()[\]{}+\-/*^])')
            # square open brackets can also be root indexes brackets
            elif ch == ']':
                expectations = re.compile(r'([0-9a-z()[\]{}+\-/*^√])')
            # sign - / +
            elif ch in '-+':
                expectations = re.compile(r'([0-9a-z([{])')
            # sign * / /
            elif ch in '*/':
                expectations = re.compile(r'([0-9a-z([{])')
            # comma / dot
            elif ch in '.,':
                expectations = re.compile(r'([0-9])')
            # number
            elif re.match(r'([0-9])', ch):
                expectations = re.compile(r'([0-9a-z()[\]{}+\-*/^.,])')
            # literal
            elif re.match(r'([a-z])', ch):
                expectations = re.compile(r'([a-z()[\]{}+\-*/^])')
            # elevation ^
            elif ch == '^':
                expectations = re.compile(r'([0-9()[\]{}])')
            # root symbol
            elif ch == '√':
                expectations = re.compile(r'([0-9+\-])')
            # won't parse for single PN objects text patterns here
        if not re.match(r'([0-9a-z)\]}])', ch):
            return False, len(text) - 1

        # ensure degree is null
        if degree != 0:
            raise Error.ValidationError('Bad user pattern, brackets inconsistency in expression object text\n'
                                        '{}'.format(text))
        return True, None

    @staticmethod
    def get_nested_end(string, opener='(', closer=')'):
        # need to sum the rest of the string after;
        # opening brackets (if there is one) mustn't be in string.
        lcl_degree = 1
        for p, ch in enumerate(string):
            lcl_degree += 1 if ch == opener else 0
            lcl_degree -= 1 if ch == closer else 0
            if lcl_degree == 0:
                return p
        return False

    @staticmethod
    def get_exponent_end(string, literals=False):
        # get end of exponent starting at the start of passed string
        if not literals:
            accepted_zero = re.compile(r'([0-9\-+])')
            accepted = re.compile(r'([0-9])')
        else:
            accepted_zero = re.compile(r'([0-9a-z\-+])')
            accepted = re.compile(r'([0-9a-z^])')
        p = 0
        for p, ch in enumerate(string):
            if p == 0 and not re.match(accepted_zero, ch):
                return False
            elif not re.match(accepted, ch):
                # end of exponent
                return p
        return p

    @staticmethod
    def _get_degree(text):
        lcl_degree, max_degree = 0, 0
        for ch in text:
            lcl_degree += 1 if ch == '(' else 0
            lcl_degree -= 1 if ch == ')' else 0
            max_degree = lcl_degree if lcl_degree > max_degree else max_degree
        return max_degree

    @staticmethod
    def get_brackets_dict(text):
        degree = _Lcl._get_degree(text)
        to_degree, lcl_degree, opens_closes = {'to_degree' + str(n + 1): None for n in range(degree)}, 0, {}
        for p, ch in enumerate(text):
            if ch == '(':
                lcl_degree += 1
                to_degree['degree_to_' + str(lcl_degree)] = p
            elif ch == ')':
                opens_closes[str(to_degree['degree_to_' + str(lcl_degree)])] = p
                lcl_degree -= 1
        return {opens_closes[value]: int(value) for value in opens_closes}

    @staticmethod
    def _parse_units(units):
        for p, unit in enumerate(units):
            try:
                if unit[-1] in '/*-+' and unit[0] not in '()':
                    units[p], units[p + 1] = unit[:-1], unit[-1] + units[p + 1]
                elif unit[0:2] == '**' and units[p - 1][-1] == ')':
                    units[p], units[p - 1] = unit[2:], units[p - 1] + unit[0:2]
                elif unit[0] in '/*-+' and unit[-1] not in '()' and '(' not in units[p - 1]:
                    units[p], units[p - 1] = unit[1:], units[p - 1] + unit[0]
            except IndexError:
                continue
        return units

    # parse text from raw to canonic form:
    # polish whitespaces
    # parse brackets
    # -> get indexes brackets to special chars
    # -> swap remaining brackets to round brackets
    # -> place indexes brackets back
    # parse high level powers
    # parse low level powers
    # parse for multiplication division specific patterns
    # split units
    # create objects

    @staticmethod
    def polish_whitespaces(text):
        return text.replace(' ', '')

    @staticmethod
    def parse_brackets(text):
        return _Lcl._parse_multiplication_division_brackets(_Lcl._parse_brackets(_Lcl._parse_indexes_brackets(text)))

    @staticmethod
    def _parse_indexes_brackets(text):
        # -> get indexes brackets to special chars
        for root_index in char_indexes(text, '√'):
            for p in range(root_index, -1, -1):
                if text[p] == '[':
                    text = text[: p] + 'ç' + text[p + 1: root_index - 1] + '@' + text[root_index:]
                    break
        return text

    @staticmethod
    def _parse_brackets(text):
        # -> swap remaining brackets to round brackets
        # -> place indexes brackets back
        return '(' + text.replace('[', '(').replace('{', '(').replace(']', ')').replace('}', ')') \
            .replace('ç', '[').replace('@', ']') + ')'

    @staticmethod
    def _parse_multiplication_division_brackets(text):
        # -> parse for multiplication / division division specific patterns
        ref = ''
        for p, ch in enumerate(text):
            try:
                if ch == '(' and re.fullmatch(r'[a-z0-9)}\]]', text[p - 1]) and p != 0:
                    ref += '*'
                ref += ch
            except IndexError:
                continue
        return ref

    @staticmethod
    def parse_hl_powers(text):
        refined = ''
        for p, ch in enumerate(text):
            refined += '**' if ch == '^' and text[p - 1] in ')]}' else ch
        text = refined
        for n, hl_power in enumerate(re.finditer(r'\)\*\*', text)):
            # add brackets around exponent
            # -> get exponent start (if a bracket after '**' -> get nested end
            #                        else: parse / validate for end of number)
            # -> get exponent end
            # -> surround with brackets
            p = hl_power.span()[1] + n * 2
            if text[p] == '(':
                end = _Lcl.get_nested_end(text[p + 1:]) + p + 1
            else:
                end = _Lcl.get_exponent_end(text[: p]) + p + 1
            text = text[: p] + '(' + text[p: end] + ')' + text[end:]
        return text

    @staticmethod
    def parse_ll_powers(text):
        # add brackets around exponent
        # -> get position of ^ chars
        # -> get exponent end
        # -> add brackets
        for n, exponent_index in enumerate(char_indexes(text, '^')):
            p = exponent_index + 1 + n * 2
            if text[p] == '(':
                end = _Lcl.get_nested_end(text[p + 1:]) + p + 1
            else:
                end = _Lcl.get_exponent_end(text[: p]) + p + 1
            text = text[: p] + '{' + text[p: end] + '}' + text[end:]
        return text

    @staticmethod
    def parse_multiplication_division_one(text):
        # SET DEFAULT VARIABLES
        # refined text variable
        ref = text
        # re pattern
        pattern = re.compile(r'(' + TR + r')[*/]\(')
        # offset handler
        index = {p: p for p in range(len(text))}
        # GET PATTERNS
        for match in re.finditer(pattern, text):
            # swap ref and text (before each processing)
            text, ref = ref, ''
            # get nested end / start (end / start of multiplication block 'a*(...)')
            block_start, block_end = index[match.span()[0]], \
                                           _Lcl.get_nested_end(text[index[match.span()[1]]:]) + index[match.span()[1]]
            # LOOP
            for p, ch in enumerate(text):
                ref += '(' if p == block_start else (')' if p == block_end else '')
                ref += ch
            # update index dict
            for key in index:
                if block_start <= key < block_end:
                    index[key] += 1
                elif key >= block_end:
                    index[key] += 2
        return ref

    @staticmethod
    def parse_multiplication_division_two(text):
        # SET DEFAULT VALUES
        pattern, ref = re.compile(r'\)[*/]'
                                  r'(' + TR + r')'), text
        # offset handler
        index = {p: p for p in range(len(text))}
        # GET PATTERNS
        for n, match in enumerate(re.finditer(pattern, text)):
            # swap ref and text (before each processing) + get brackets dict
            text, ref, bra = ref, '', _Lcl.get_brackets_dict(text)
            # get nested end / start (end / start of multiplication block '(...)*a')
            block_start, block_end = index[bra[match.span()[0]]], index[match.span()[1]]
            # LOOP
            for p, ch in enumerate(text):
                ref = ref[: block_start] + '(' + ref[block_start: block_end + 1] + ')' + ch if p == block_end \
                    else ref + ch
            # update index dict
            for key in index:
                if block_start <= key < block_end:
                    index[key] += 1
                elif key >= block_end:
                    index[key] += 2
        return ref

    @staticmethod
    def parse_double_brackets(text):
        refined = ''
        for p, ch in enumerate(text):
            try:
                refined += ch
                if ch == '(' and text[p + 1] == '(':
                    refined += '0+'
                elif ch == ')' and text[p + 1] == ')':
                    refined += '+0'
            except IndexError:
                continue
        return refined

    @staticmethod
    def split_units(text):
        units, unit = [], ''
        for p, ch in enumerate(text):
            if ch in '()':
                units, unit = units + [unit, ch] if unit else units + [ch], ''
            else:
                unit += ch
        for _ in range(2):
            units = _Lcl._parse_units(units)
        for p, unit in enumerate(units):
            if not unit:
                del (units[p])
        return units

    @staticmethod
    def create_objects(units):
        for p, unit in enumerate(units):
            if '(' not in unit and ')' not in unit:
                units[p] = 'pn("' + unit + '")'
        ref = ''
        for p, unit in enumerate(units):
            ref += unit
        return ref.replace('{', '(').replace('}', ')')

    @staticmethod
    def get_coefficient(text):
        string = ''
        for ch in text:
            if re.match(r'([a-z])', ch):
                break
            string += ch
        if string == '' or string in '-+':
            string += '1'
        return string

    @staticmethod
    def get_literals(text):
        string, letter = '', False
        for ch in text:
            if re.match(r'([a-z])', ch):
                letter = True
            if letter:
                string += ch
        text = string
        string = ''
        for p, ch in enumerate(text):
            string += ch
            if re.match(r'([a-z])', ch):
                try:
                    if re.match(r'([a-z])', text[p + 1]):
                        string += '^(1)'
                except IndexError:
                    string += '^(1)'
        return string

    @staticmethod
    def get_literals_objects(text):
        literals = []
        # split string into single literals
        for literal in text.split(')'):
            # 'x^(n'
            if literal:
                if len(literal) == 4:
                    literals += [Li(literal[0], int(literal[3]))]
                else:
                    literals += [Li(literal[0], int(literal[3:]))]
        return ML(literals)


class ExParser:
    def __init__(self, text):
        self.text = text
        self.parsed_text = text
        self.validate()
        # assign empty values
        self.brackets_dict = {}

    def validate(self):
        # validate text symbols / pattern
        _Lcl.validate_text(self.parsed_text)

    def parse(self):
        self.parsed_text = _Lcl.polish_whitespaces(self.parsed_text)
        # parse brackets
        self._parse_brackets()
        # parse powers
        self._parse_powers()
        # parse multiplications / divisions
        self._parse_multiplication_division()
        # create objects
        self._create_objects()

    def _parse_brackets(self):
        self.parsed_text = _Lcl.parse_brackets(self.parsed_text)

    def _parse_powers(self):
        # parse high level powers
        self.parsed_text = _Lcl.parse_hl_powers(self.parsed_text)
        # parse low level powers
        self.parsed_text = _Lcl.parse_ll_powers(self.parsed_text)

    def _parse_multiplication_division(self):
        # parse N * (...)
        self.parsed_text = _Lcl.parse_multiplication_division_one(self.parsed_text)
        # parse (...) * N
        self.parsed_text = _Lcl.parse_multiplication_division_two(self.parsed_text)
        # parse (( and ))
        self.parsed_text = _Lcl.parse_double_brackets(self.parsed_text)

    def _create_objects(self):
        # split units
        self.parsed_text: str
        self.parsed_text = _Lcl.split_units(self.parsed_text)
        # create objects
        self.parsed_text = _Lcl.create_objects(self.parsed_text)


class PnValidator:
    """
    PARSING:
        divide text into terms;
        get terms-elements type pattern.
    """
    default_expectation = re.compile(r'([0-9a-z\-+[√])')

    def __init__(self, text):
        """

        :param text: str
        Assign empty parsing data
        types: co-ra, co-ir, co-ir-ix, li-var, li-exp, exp-cl
        """
        self.data = text
        self.current = {'e': '', 't': '', 'T': ''}  # Element, Type, Term (increasing size)
        self.history, self.terms = [], []

    def parse(self):
        expected = PnValidator.default_expectation

        for CH in self.data:
            if not re.fullmatch(expected, CH):
                raise ValueError('Bad user text')

            if not self.current['t']:
                # no element defined yet or previous one already closed -> CLEAR TERM
                # expected -> default_expectation
                # ch could be either:
                #     Sign -> co-ra
                #     Number-> co-ra
                #     Square bra -> co-ir-ix
                #     Letter -> li-var
                #     Square root -> co-ir-ix
                if re.match(r'([-+])', CH):
                    self.current['t'] = 'co-ra'
                    expected = re.compile(r'([0-9a-z[√])')
                elif re.match(r'([0-9])', CH):
                    self.current['t'] = 'co-ra'
                    expected = re.compile(r'([0-9a-z-+/.,[√])')
                elif CH == '[':
                    self.current['t'] = 'co-ir-ix'
                    expected = re.compile(r'([0-9-+])')
                elif re.match(r'([a-z])', CH):
                    self.current['t'] = 'li-var'
                    expected = re.compile(r'([0-9a-z^\-+[√])')
                elif CH == '√':
                    self.current['t'] = 'co-ir'
                    expected = re.compile(r'([0-9\-+])')

            elif self.current['t'] == 'co-ra':
                # element defined as co-ra
                # expected -> either Number, Literal, Sq bra, Sq rt
                #                 or Number, Literal, Sq bra, Sq rt, Sign, dot/comma
                # ch could be either:
                #     Sign -> -NEW TERM- ra-co
                #     Number -> -same-
                #     Square bra -> ir-co-ix -same term-
                #     Letter -> li-var -same term-
                #     Square root -> ir-co -same term-
                #     dot/comma -> -same-
                if re.match(r'([-+])', CH):
                    self._reassign_elem()
                    self.terms += [self.current['T']]
                    self.current['T'] = ''
                    self.current['t'] = 'co-ra'
                    expected = re.compile(r'([0-9a-z[√])')
                elif re.match(r'([0-9])', CH):
                    expected = re.compile(r'([0-9a-z-+/.,[√])')
                elif CH == '[':
                    self._reassign_elem()
                    self.current['t'] = 'co-ir-ix'
                    expected = re.compile(r'([0-9-+])')
                elif re.match(r'([a-z])', CH):
                    self._reassign_elem()
                    self.current['t'] = 'li-var'
                    expected = re.compile(r'([0-9a-z^\-+[√])')
                elif CH == '√':
                    self._reassign_elem()
                    self.current['t'] = 'co-ir'
                    expected = re.compile(r'([0-9\-+])')
                elif re.match(r'([.,/])', CH):
                    expected = re.compile(r'([0-9])')

            elif self.current['t'] == 'co-ir-ix':
                # element defined as ir-co-ix
                # always defined with a '['
                # expected -> Number, Sign
                # ch could be either:
                #     Number -> -same-
                #     Sign -> -same-
                #
                # ... when ch is ']', element is ended -> ir-co -same term-
                if re.match(r'([0-9])', CH):
                    expected = re.compile(r'([0-9\]])')
                elif re.match(r'([-+])', CH):
                    expected = re.compile(r'([0-9\]])')
                elif CH == ']':
                    self._reassign_elem()
                    self.current['t'] = ''
                    expected = re.compile(r'√')

            elif self.current['t'] == 'co-ir':
                # element defined as ir-co
                # always defined with a '√'
                # expected -> Number, Sign, dot/comma, Literal
                # ch could be either:
                #     Number -> -same-
                #     Sign -> analyse current[e]: if '√' or ']√' -> same, else -NEW TERM- co-ra
                #     dot/comma -> -same-
                #     Literal -> li-var -same term-
                if re.match(r'([0-9])', CH):
                    expected = re.compile(r'([0-9a-z/.,\-+])')
                elif re.match(r'([-+])', CH):
                    if self.current['e'][-1] == '√':
                        expected = re.compile(r'([0-9])')
                    else:
                        self._reassign_elem()
                        self.terms += [self.current['T']]
                        self.current['T'] = ''
                        self.current['t'] = 'co-ra'
                        expected = re.compile(r'([0-9a-z[√])')
                elif re.match(r'([.,/])', CH):
                    expected = re.compile(r'([0-9])')
                elif re.match(r'([a-z])', CH):
                    self._reassign_elem()
                    self.current['t'] = 'li-var'
                    expected = re.compile(r'([0-9a-z^\-+[√])')

            elif self.current['t'] == 'li-var':
                # element defined as li-var
                # always defined with a Literal
                # expected -> Literal, Exponent Sign, Number, Sq bra, Sq root, Sign
                # ch could either be:
                #     Exponent sign ^ -> li-exp -same term-
                #     Literal -> li-var -same term-
                #     Sign -> -NEW TERM- co-ra
                #     Number -> co-ra -same term-
                #     Sq bra -> co-ir-ix -same term-
                #     Sq root -> co-ir -same term-
                #
                # Cannot remain -same-
                if CH == '^':
                    self._reassign_elem()
                    self.current['t'] = 'li-exp'
                    expected = re.compile(r'\(')  # may be re-seen
                elif re.match(r'([a-z])', CH):
                    self._reassign_elem()
                    self.current['t'] = 'li-var'
                    expected = re.compile(r'([0-9a-z^\-+[√])')
                elif re.match(r'([-+])', CH):
                    self._reassign_elem()
                    self.terms += [self.current['T']]
                    self.current['T'] = ''
                    self.current['t'] = 'co-ra'
                    expected = re.compile(r'([0-9a-z[√])')
                elif re.match(r'([0-9])', CH):
                    self._reassign_elem()
                    self.current['t'] = 'co-ra'
                    expected = re.compile(r'([0-9a-z-+/.,[√])')
                elif CH == '[':
                    self._reassign_elem()
                    self.current['t'] = 'co-ir-ix'
                    expected = re.compile(r'([0-9-+])')
                elif CH == '√':
                    self._reassign_elem()
                    self.current['t'] = 'co-ir'
                    expected = re.compile(r'([0-9\-+])')

            elif self.current['t'] == 'li-exp':
                # element defined as li-exp
                # always defined with a exponent sign ^
                # expected -> open bra, Number, Sign, close bra
                # ch could be either:
                #     open bra -> -same-
                #     Number -> -same-
                #     Sign -> -same-
                #     close bra -> exp-cl -same term-
                if CH == '(':
                    expected = re.compile(r'([0-9\-+])')
                elif re.match(r'([0-9])', CH):
                    expected = re.compile(r'([0-9)])')
                elif re.match(r'([-+])', CH):
                    expected = re.compile(r'([0-9)])')
                elif CH == ')':
                    self._reassign_elem()
                    self.current['t'] = 'exp-cl'
                    expected = re.compile(r'([-+0-9a-z[√])')

            elif self.current['t'] == 'exp-cl':
                # element defined as exp-cl
                # always defined with close bra )
                # expected -> Sign, Number, Literal, Sq root, Sq bra
                # ch could be either:
                #     Sign -> -NEW TERM- co-ra
                #     Number -> co-ra -same term-
                #     Literal -> li-var -same term-
                #     Sq root -> co-ir -same term-
                #     Sq bra -> co-ir-ix -same term-
                if re.match(r'([-+])', CH):
                    self._reassign_elem()
                    self.terms += [self.current['T']]
                    self.current['T'] = ''
                    self.current['t'] = 'co-ra'
                    expected = re.compile(r'([0-9a-z[√])')
                elif re.match(r'([0-9])', CH):
                    self._reassign_elem()
                    self.current['t'] = 'co-ra'
                    expected = re.compile(r'([0-9a-z-+/.,[√])')
                elif re.match(r'([a-z])', CH):
                    self._reassign_elem()
                    self.current['t'] = 'li-var'
                    expected = re.compile(r'([0-9a-z^\-+[√])')
                elif CH == '√':
                    self._reassign_elem()
                    self.current['t'] = 'co-ir'
                    expected = re.compile(r'([-+0-9])')
                elif CH == '[':
                    self._reassign_elem()
                    self.current['t'] = 'co-ir-ix'
                    expected = re.compile(r'([0-9\-+])')

            self.current['e'] += CH
            self.history += [self.current['t']]

        self.terms += [self.current['T'] + self.current['e']]

    def _reassign_elem(self):
        self.current['T'] += self.current['e']
        self.current['e'] = ''


class TrParser:
    def __init__(self, text):
        self.text = text
        self.parsed_text = text
        self.coefficient = None
        self.literals = None

    def parse(self):
        self.parsed_text = _Lcl.polish_whitespaces(self.parsed_text)
        # parse coefficient
        self._parse_coefficient()
        # parse literals
        self._parse_literals()

    def _parse_coefficient(self):
        # get coefficient string
        coefficient = _Lcl.get_coefficient(self.parsed_text)
        # get actual coefficient object
        self.coefficient = RN(RNU(s=coefficient))

    def _parse_literals(self):
        # get literals string
        literals = _Lcl.get_literals(self.parsed_text)
        # get actual literals object
        self.literals = _Lcl.get_literals_objects(literals)


# must set up a domain propagation system for PN objects, to keep track of his history in evaluation
def pn(text):
    # split terms into single terms string
    parser = PnValidator(text)
    parser.parse()
    terms = parser.terms
    # parse terms strings
    for p, term in enumerate(terms):
        term = TrParser(term)
        term.parse()
        # assign terms values from the canonic string
        terms[p] = Tr(term.coefficient, term.literals)
    return PN(LPN(terms))


class Ex:
    """
    Expression object -> expecting string
    """

    def __init__(self, text):
        self.text = text
        # parse text
        # validate text symbols / pattern
        parser = ExParser(text)
        parser.parse()
        # assign parsed text
        self.canonic_text = parser.parsed_text
        self.value = eval(self.canonic_text)
        self.reduced = self.value.reduce

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text

    # operations
    def __add__(self, other):
        if isinstance(other, Ex):
            return Ex('(' + self.text + ')' + '+' + '(' + other.text + ')')
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Ex):
            return Ex('(' + self.text + ')' + '-' + '(' + other.text + ')')
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Ex):
            return Ex('(' + self.text + ')' + '*' + '(' + other.text + ')')
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Ex):
            return Ex('(' + self.text + ')' + '/' + '(' + other.text + ')')
        return NotImplemented

    def __pow__(self, power, modulo=None):
        if isinstance(power, Ex):
            return Ex('(' + self.text + ')' + '^' + '(' + power.text + ')')
        return NotImplemented
