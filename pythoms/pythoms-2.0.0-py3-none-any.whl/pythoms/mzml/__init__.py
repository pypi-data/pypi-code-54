"""
Module for interacting with mzML files
"""
from .structure import mzML

__all__ = [
    'mzML',
]


if __name__ == '__main__':
    filename = 'MultiTest'
    mzml = mzML(filename, verbose=True, ftt=True)
    # sp = {
    # 'pos':{'bounds':[325,327],'affin':'+','spectrum':Spectrum(3),'raw':[]},
    # 'neg':{'bounds':[348,350],'affin':'-','spectrum':Spectrum(3),'raw':[]},
    # 'uv':{'bounds':[378,None],'affin':'UV','raw':[]}
    # }
