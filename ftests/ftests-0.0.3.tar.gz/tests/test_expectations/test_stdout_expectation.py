import unittest
from subprocess import CompletedProcess

from ftests.expectation_result import ExpectationResult
from ftests.expectations import CompletedProcessExpectation, StdoutExpectation


class StdoutExpectationTest(unittest.TestCase):
    def test_correct_inheritance(self):
        expectation = StdoutExpectation(b'Test')
        self.assertIsInstance(expectation, CompletedProcessExpectation)

    def test_mandatory_parameter(self):
        self.assertRaises(TypeError, StdoutExpectation)

    def test_accepts_bytes(self):
        expectation = StdoutExpectation(b'bytes')
        self.assertEqual(b'bytes', expectation.expected_stdout)

    def test_accepts_str(self):
        expectation = StdoutExpectation('string')
        self.assertEqual(b'string', expectation.expected_stdout)

    def test_codename(self):
        self.assertEqual('stdout', StdoutExpectation.codename)

    def test_accept_only_bytes(self):
        self.assertRaises(TypeError, StdoutExpectation, [b'not bytes'])
        self.assertRaises(TypeError, StdoutExpectation, 0.42)
        self.assertRaises(TypeError, StdoutExpectation, None)

    def test_expectation_met(self):
        expectation = StdoutExpectation(b'It is OK\n')
        mock_cp = CompletedProcess('', 0, stdout=b'It is OK\n')
        self.assertEqual(
            ExpectationResult(expectation=expectation, passed=True, expected=b'It is OK\n', got=b'It is OK\n'),
            expectation.is_expectation_met(mock_cp))

    def test_expectation_not_met(self):
        expectation = StdoutExpectation(b'It is true')
        mock_cp = CompletedProcess('', 84, stdout=b'It is false')
        self.assertEqual(
            ExpectationResult(expectation=expectation, passed=False, expected=b'It is true', got=b'It is false'),
            expectation.is_expectation_met(mock_cp))


if __name__ == '__main__':
    unittest.main()
