#!/usr/bin/env python
# -*- coding: utf-8 -*0


"""A formatter for int as bytes."""


class EyeFriendlyBytes:
    """Easily make number for bytes into eye-friendly string.

    Instantiate with number and
    call methods::

        efb123 = zobepy.EyeFriendlyBytes(123)
        print(efb123.get())
        # output string: 123 B
        print(efb123)
        # output string: 123 B

    Use default
    automatically chosen unit::

        efb123 = zobepy.EyeFriendlyBytes(12300)

        print(efb123.get())
        # output string: 12 KiB
        print(efb123.get_unit_string())
        # output string: KiB

    .. csv-table:: examples
        :header: "integer value", "converted text (default)"
        :widths: 5, 5

        123, "123 B"
        12300, "12 KiB"
        123000000, "117 MiB"
        1230000000000, "1.1 TiB"
        123000000000000000000000000, "102 YiB"
        12300000000000000000000000000000, "10,174,322 YiB"


    Note:
        The symbols and names are declared in
        IEC 60027-2 A.2 and ISO/IEC 80000.

        Reference: https://en.wikipedia.org/wiki/Binary_prefix

    Parameters
    ----------
    val : int
        An int value.

    """

    def __init__(self, val: int):
        """Initialize this instance."""
        self._val = val
        self._decide_preferred_unit()

    UNIT_B = 0
    """Unit 'bytes'. """

    UNIT_KIB = 1
    """Unit 'kibi bytes', 'KiB'"""

    UNIT_MIB = 2
    """Unit 'mebi bytes', 'MiB'"""

    UNIT_GIB = 3
    """Unit 'gibi bytes', 'GiB'"""

    UNIT_TIB = 4
    """Unit 'tebi bytes', 'TiB'"""

    UNIT_PIB = 5
    """Unit 'pebi bytes', 'PiB'"""

    UNIT_EIB = 6
    """Unit 'exbi bytes', 'EiB'"""

    UNIT_ZIB = 7
    """Unit 'zebi bytes', 'ZiB'"""

    UNIT_YIB = 8
    """Unit 'yobi bytes', 'YiB'"""

    UNIT_MAX = UNIT_YIB
    """Current largest unit symbol is YiB."""

    UNIT_MIN = UNIT_B
    """No symbol."""

    UNIT_SYMBOLS = {
        0: '',
        1: 'Ki',
        2: 'Mi',
        3: 'Gi',
        4: 'Ti',
        5: 'Pi',
        6: 'Ei',
        7: 'Zi',
        8: 'Yi',
    }
    """Binary prefix symbols declared in ISO/IEC 80000."""

    UNIT_NAMES = {
        0: '',
        1: 'kibi',
        2: 'mebi',
        3: 'gibi',
        4: 'tebi',
        5: 'pebi',
        6: 'exbi',
        7: 'zebi',
        8: 'yobi',
    }
    """Binary prefix names declared in ISO/IEC 80000."""

    UNIT_CUSTOMARY_SYMBOLS = {
        0: '',
        1: 'K',
        2: 'M',
        3: 'G',
        4: 'T',
        5: 'P',
        6: 'E',
        7: 'Z',
        8: 'Y',
    }
    """Customary binary prefixes."""

    UNIT_CUSTOMARY_NAMES = {
        0: '',
        1: 'kilo',
        2: 'mega',
        3: 'giga',
        4: 'tera',
        5: 'peta',
        6: 'exa',
        7: 'zeta',
        8: 'yotta',
    }
    """Customary binary prefix names declared in ISO/IEC 80000."""

    @staticmethod
    def round(val, digit: int = 0):
        """Round specified digit of the val.

        Parameters
        ----------
        val : int
            An int value.
        digit : int, default 0
            The digit to be rounded at.

        Returns
        -------
        float
            Rounded value.

        """
        p = 10 ** digit
        return (val * p * 2 + 1) // 2 / p

    @staticmethod
    def conv(val: int) -> str:
        """Easily make number for bytes into eye-friendly string.

        The most simple way to use this class.

        Parameters
        ----------
        val : int
            An int value.

        Returns
        -------
        int
            Formatted string.

        """
        return str(EyeFriendlyBytes(val))

    def __str__(self):
        """Convert value into string with appropriate unit prefix."""
        return self.get()
        # return self.get_value_string() + ' ' + self.get_unit_string()

    def get(self, base1024: int = -1) -> str:
        """Convert value into string. You can choose unit prefix.

        .. csv-table::
            :header: "base1024", "descirption"

            -1, "default, unit prefix automatically selected"
            0, "expression in bytes. ex. 123: 123 B"
            1, "expression in KiB. ex. 1024: 1.0 KiB"
            2, "expression in MiB."
            "...", "..."
            8, "expression in YiB."

        Parameters
        ----------
        base1024 : int, default -1
            Force the unit.

        Returns
        -------
        str
            Formatted string of the value.

        See also
        --------
        get_value_string : get formatted string of numeric part only

        """
        return (self.get_value_string(base1024)
                + ' ' + self.get_unit_string(base1024))

    def get_value_string(self, base1024: int = -1) -> str:
        """Convert numeric value into string.

        Returns number only.
        You can also use unit string getter methods.

        Parameters
        ----------
        base1024 : int, default -1
            Force the unit.

        Returns
        -------
        str
            Formatted string of the numeric part of the value.

        See also
        --------
        get_unit_string : Like 'KiB', 'MiB'.
        get_unit_symbol : Like 'Ki', 'Mi'.
        get_unit_name : Like 'kibi', 'mebi'.
        get_unit_customary_symbol : Like 'K', 'M'.
        get_unit_customary_name : Like 'kilo', 'mega'.

        """
        if base1024 == -1:
            base1024 = self._unit

        if base1024 == 0:
            s = '{:,}'
            s = s.format(self._val)
            return s
        else:
            if self._val < (100 * (1024 ** (base1024 - 1))):
                return '0.0'
            elif self._val < (10 * (1024 ** base1024)):
                v = self._val / 1024 ** base1024
                v = EyeFriendlyBytes.round(v, 1)
                return str(v)
            elif self._val < (100 * (1024 ** base1024)):
                v = self._val / 1024 ** base1024
                v = EyeFriendlyBytes.round(v)
                v = int(v)
                return str(v)
            else:
                v = self._val / 1024 ** base1024
                v = EyeFriendlyBytes.round(v)
                v = int(v)
                return '{:,}'.format(v)

    def get_unit(self) -> int:
        """Return preferred unit number, in EyeFriendlyBytes.UNIT_* constants.

        * Same as base-1024 value.
        * ex. KiB = 1
        * ex. MiB = 2

        Returns
        -------
        int

        """
        return self._unit

    def get_unit_string(self, base1024: int = -1):
        """Return unit string, KiB, MiB, etc.

        if base1024 = 0, it returns 'B' (no prefix).

        Returns
        -------
        string

        """
        return self.get_unit_symbol(base1024) + 'B'

    def get_unit_symbol(self, base1024: int = -1):
        """Return binary prefix of ISO/IEC 80000. ex:'Ki' for 1024.

        * ex1. 0 = '' (no prefix)
        * ex2. 1 = 'Ki' (kibi)
        * ex3. 2 = 'Mi' (mebi)

        If do not specify base1024, it returns automatically preferred prefix
        for the initial value of the instance.

        Returns
        -------
        string

        """
        unit = base1024
        if base1024 == -1:
            unit = self.get_unit()

        if unit < EyeFriendlyBytes.UNIT_MIN:
            unit = EyeFriendlyBytes.UNIT_MIN
        elif unit > EyeFriendlyBytes.UNIT_MAX:
            unit = EyeFriendlyBytes.UNIT_MAX

        return EyeFriendlyBytes.UNIT_SYMBOLS.get(unit, '')

    def get_unit_name(self, base1024: int = -1):
        """Return binary prefix name instead of the symbol. ex:'kibi' for 1024.

        * ex1. 0 = '' (no prefix)
        * ex2. 1 = 'kibi'
        * ex3. 2 = 'mebi'

        If do not specify base1024, it returns automatically preferred prefix
        for the initial value of the instance.

        Returns
        -------
        string

        """
        unit = base1024
        if base1024 == -1:
            unit = self.get_unit()

        if unit < EyeFriendlyBytes.UNIT_MIN:
            unit = EyeFriendlyBytes.UNIT_MIN
        elif unit > EyeFriendlyBytes.UNIT_MAX:
            unit = EyeFriendlyBytes.UNIT_MAX

        return EyeFriendlyBytes.UNIT_NAMES.get(unit, '')

    def get_unit_customary_symbol(self, base1024: int = -1):
        """Return customary binary prefix. ex: 'K' for 1024.

        * ex1. 0 = '' (no prefix)
        * ex2. 1 = 'K' (prefix of 'kilo-bytes' instead of 'kibi')
        * ex3. 2 = 'M' (prefix of 'mega-bytes' instead of 'mebi')

        If do not specify base1024, it returns automatically preferred prefix
        for the initial value of the instance.

        Returns
        -------
        string

        """
        unit = base1024
        if base1024 == -1:
            unit = self.get_unit()

        if unit < EyeFriendlyBytes.UNIT_MIN:
            unit = EyeFriendlyBytes.UNIT_MIN
        elif unit > EyeFriendlyBytes.UNIT_MAX:
            unit = EyeFriendlyBytes.UNIT_MAX

        return EyeFriendlyBytes.UNIT_CUSTOMARY_SYMBOLS.get(unit, '')

    def get_unit_customary_name(self, base1024: int = -1):
        """Return customary binary prefix name. ex:'kilo' for 1024.

        * ex1. 0 = '' (no prefix)
        * ex2. 1 = 'kilo'
        * ex3. 2 = 'mega'

        If do not specify base1024, it returns automatically preferred prefix
        for the initial value of the instance.

        Returns
        -------
        string

        """
        unit = base1024
        if base1024 == -1:
            unit = self.get_unit()

        if unit < EyeFriendlyBytes.UNIT_MIN:
            unit = EyeFriendlyBytes.UNIT_MIN
        elif unit > EyeFriendlyBytes.UNIT_MAX:
            unit = EyeFriendlyBytes.UNIT_MAX

        return EyeFriendlyBytes.UNIT_CUSTOMARY_NAMES.get(unit, '')

    def _decide_preferred_unit(self):
        self._unit = EyeFriendlyBytes.UNIT_MAX
        for i in range(0, 1 + EyeFriendlyBytes.UNIT_MAX):
            if self._val < 512 * (1024**i):
                self._unit = i
                break
