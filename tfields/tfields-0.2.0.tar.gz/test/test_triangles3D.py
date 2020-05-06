import tfields
import numpy as np
import unittest
import sympy  # NOQA: F401
import os
import sys
THIS_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(THIS_DIR)))
from test_core import Base_Check


class IO_test(Base_Check, unittest.TestCase):
    pass


class IO_Stl_test(IO_test):
    def setUp(self):
        self._inst = tfields.Triangles3D.load(r'../data/baffle.stl')

if __name__ == '__main__':
    unittest.main()