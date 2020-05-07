import os
import shutil
import unittest

from PyRSIR import pyrsir


class TestPyRSIR(unittest.TestCase):
    def setUp(self) -> None:
        # target xlsx and mzml pairings
        self.targets = [
            [
                os.path.join(os.path.dirname(__file__), 'multitest_pyrsir_validation.xlsx'),
                os.path.join(os.path.dirname(__file__), 'MultiTest.mzML.gz')
            ],
            [
                os.path.join(os.path.dirname(__file__), 'LY-2015-09-15 06 pyrsir example.xlsx'),
                os.path.join(os.path.dirname(__file__), 'LY-2015-09-15 06.mzML.gz'),
            ]
        ]
        # create backups
        for xlfile, _ in self.targets:
            shutil.copy(
                xlfile,
                f'{xlfile}.bak'
            )

    def test(self):
        for xlfile, msfile in self.targets:
            pyrsir(
                msfile,
                xlfile,
                3,
                plot=False,
                verbose=False,
            )

    def tearDown(self) -> None:
        for xlfile, _ in self.targets:
            shutil.copy(
                f'{xlfile}.bak',
                xlfile,
            )
            os.remove(f'{xlfile}.bak')
