import unittest
from subprocess import CompletedProcess

from ftests.expectation_result import ExpectationResult
from ftests.expectations import CompletedProcessExpectation, StderrExpectation


class StderrExpectationTest(unittest.TestCase):
    def test_correct_inheritance(self):
        expectation = StderrExpectation(b'Test')
        self.assertIsInstance(expectation, CompletedProcessExpectation)

    def test_mandatory_parameter(self):
        self.assertRaises(TypeError, StderrExpectation)

    def test_accepts_bytes(self):
        expectation = StderrExpectation(b'bytes')
        self.assertEqual(b'bytes', expectation.expected_stderr)

    def test_accepts_str(self):
        expectation = StderrExpectation('string')
        self.assertEqual(b'string', expectation.expected_stderr)

    def test_codename(self):
        self.assertEqual('stderr', StderrExpectation.codename)

    def test_accept_only_bytes(self):
        self.assertRaises(TypeError, StderrExpectation, [b'not bytes'])
        self.assertRaises(TypeError, StderrExpectation, 0.42)
        self.assertRaises(TypeError, StderrExpectation, None)

    def test_expectation_met(self):
        expectation = StderrExpectation(b'It is OK\n')
        mock_cp = CompletedProcess('', 0, stderr=b'It is OK\n')
        self.assertEqual(
            ExpectationResult(expectation=expectation, passed=True, expected=b'It is OK\n', got=b'It is OK\n'),
            expectation.is_expectation_met(mock_cp))

    def test_expectation_not_met(self):
        expectation = StderrExpectation(b'It is true')
        mock_cp = CompletedProcess('', 84, stderr=b'It is false')
        self.assertEqual(
            ExpectationResult(expectation=expectation, passed=False, expected=b'It is true', got=b'It is false'),
            expectation.is_expectation_met(mock_cp))


if __name__ == '__main__':
    unittest.main()
