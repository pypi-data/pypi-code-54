# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 21:18:44 2019

@author: yoelr
"""

__all__ = ('PoyintingCorrectionFactors',
           'IdealPoyintingCorrectionFactors')

class PoyintingCorrectionFactors:
    """Abstract class for the estimation of Poyinting correction factors. Non-abstract subclasses should implement the following methods:
        
    __init__(self, chemicals: Iterable[Chemicals]):
        Should use pure component data from chemicals to setup future calculations of Poyinting correction factors.
    
    __call__(self, y: 1d array, T: float):
        Should accept an array of vapor molar compositions `y`, and temperature `T` (in Kelvin), and return an array of Poyinting correction factors. Note that the molar compositions must be in the same order as the chemicals defined when creating the PoyintingCorrectionFactors object.
        
    """
    __slots__ = ()
    
    def __init__(self, chemicals):
        self.chemicals = chemicals
    
    def __repr__(self):
        chemicals = ", ".join([i.ID for i in self.chemicals])
        return f"<{type(self).__name__}([{chemicals}])>"


class IdealPoyintingCorrectionFactors(PoyintingCorrectionFactors):
    """Create an IdealPoyintingCorrectionFactor object that estimates all poyinting correction factors to be 1 when called with composition and temperature (K).
    
    Parameters
    ----------
    
    chemicals : Iterable[Chemical]
    
    """
    __slots__ = ('_chemicals')
    
    @property
    def chemicals(self):
        return self._chemicals
    @chemicals.setter
    def chemicals(self, chemicals):
        self._chemicals = tuple(chemicals)

    def __call__(self, y, T):
        return 1.
