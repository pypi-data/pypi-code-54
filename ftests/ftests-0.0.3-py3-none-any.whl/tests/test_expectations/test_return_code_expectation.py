import unittest
from subprocess import CompletedProcess

from ftests.expectation_result import ExpectationResult
from ftests.expectations import ReturnCodeExpectation, CompletedProcessExpectation


class ReturnCodeExpectationTest(unittest.TestCase):
    def test_correct_inheritance(self):
        expectation = ReturnCodeExpectation(0)
        self.assertIsInstance(expectation, CompletedProcessExpectation)

    def test_mandatory_parameter(self):
        self.assertRaises(TypeError, ReturnCodeExpectation)

    def test_codename(self):
        self.assertEqual('return_code', ReturnCodeExpectation.codename)

    def test_accept_only_ints(self):
        self.assertRaises(TypeError, ReturnCodeExpectation, 'not an int')
        self.assertRaises(TypeError, ReturnCodeExpectation, 0.1)
        self.assertRaises(TypeError, ReturnCodeExpectation, None)

    def test_expectation_met(self):
        expectation = ReturnCodeExpectation(0)
        mock_cp = CompletedProcess('', 0)
        self.assertTrue(expectation.is_expectation_met(mock_cp))

    def test_expectation_not_met(self):
        expectation = ReturnCodeExpectation(42)
        mock_cp = CompletedProcess('', 84)
        self.assertEqual(ExpectationResult(expectation=expectation, passed=False, expected=42, got=84),
                         expectation.is_expectation_met(mock_cp))


if __name__ == '__main__':
    unittest.main()
