"""Functions for computing resistivity from saturation
"""


def archie(sw, poro, m, n, a=1):
    """Compute the formation resistivity.

    This function calculate formation resistivity from water saturation, porosity,
    and Archie's parameters a, m, and n.
    The formula for the Archie's Law is::

        Rt = a * poro**m * sw**n

    Args:
        sw : 1d array. Water saturations.
        poro : 1d array. Formation porosity.
        a : Archie's parameter, constant.
        m : Archie's parameter, cementation exponent.
        n : Archie's parameter, saturation exponent.

    Returns:
        resistivity : 1d array.

    Example:
        >>> from petrophysics.resistivity import archie
        >>> rt = archie(1.0, 0.2, 2, 2, 1)
        0.04
    """
    
    rt = a * poro**m * sw**n

    return rt