"""
The :mod:`sklearn.covariance` module includes methods and algorithms to
robustly estimate the covariance of features given a set of points. The
precision matrix defined as the inverse of the covariance is also estimated.
Covariance estimation is closely related to the theory of Gaussian Graphical
Models.
"""

from .types.csv import Csv
from .types.parquet import Parquet
from .types.json import Json

__all__ = ['Csv',
           'Json',
           'Parquet']