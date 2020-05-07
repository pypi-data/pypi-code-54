"""
ChainedUnit, allowing for the `&` operator to link units together.
"""

from .unit import Unit

class ChainedUnit(DisplayUnit):
    """
    A chain of units, all of the same dimension.

    Instantiate by:
     -  `ChainedUnit(a, b, c, ...)`, where the "default unit" is a,
     -  `a & b & c &...`, where the "default unit" is the smallest.
    
    While it can be used in measurements, this is best used for display
    eg "length @ feet&inch".
    """
    __slots__ = Unit.__slots__ + "units"

    def __and__(self, unit):
        pass
