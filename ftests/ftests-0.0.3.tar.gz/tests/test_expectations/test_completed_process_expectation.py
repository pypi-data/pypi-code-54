import unittest
from subprocess import CompletedProcess

from ftests.expectations import CompletedProcessExpectation


class MockExpectation(CompletedProcessExpectation):

    def _check_expectation(self, completed_process: CompletedProcess) -> bool:
        return True

    @property
    def codename(self):
        return 'mock_expectation'


class CompletedProcessExpectationTest(unittest.TestCase):

    def test_abstractness(self):
        self.assertRaises(TypeError, CompletedProcessExpectation)

    def test_is_expectation_met_arg_check_good_type(self):
        mock_expectation = MockExpectation()
        mock_cp = CompletedProcess(args=[], returncode=0)
        self.assertTrue(mock_expectation.is_expectation_met(mock_cp))

    def test_is_expectation_met_arg_check_wrong_type(self):
        mock_expectation = MockExpectation()
        self.assertRaises(TypeError, mock_expectation.is_expectation_met, 'wrong argument type')
        self.assertRaises(TypeError, mock_expectation.is_expectation_met, 1.5)
        self.assertRaises(TypeError, mock_expectation.is_expectation_met, {})
        self.assertRaises(TypeError, mock_expectation.is_expectation_met, None)


if __name__ == '__main__':
    unittest.main()
