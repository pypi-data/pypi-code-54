from subprocess import CompletedProcess

from ._completed_process_expectation import CompletedProcessExpectation
from ..expectation_result import ExpectationResult


class StderrExpectation(CompletedProcessExpectation):
    codename = 'stderr'
    expected_stderr: bytes

    def __init__(self, expected_stdout):
        if isinstance(expected_stdout, bytes):
            self.expected_stderr = expected_stdout
        elif isinstance(expected_stdout, str):
            self.expected_stderr = expected_stdout.encode()
        else:
            raise TypeError('Expected stderr must be either a bytes or an str object')

    def _check_expectation(self, completed_process: CompletedProcess) -> ExpectationResult:
        return ExpectationResult(
            expectation=self,
            passed=self.expected_stderr == completed_process.stderr,
            expected=self.expected_stderr,
            got=completed_process.stderr,
        )
