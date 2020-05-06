from subprocess import CompletedProcess

from ._completed_process_expectation import CompletedProcessExpectation
from ..expectation_result import ExpectationResult


class StdoutExpectation(CompletedProcessExpectation):
    codename = 'stdout'
    expected_stdout: bytes

    def __init__(self, expected_stdout):
        if isinstance(expected_stdout, bytes):
            self.expected_stdout = expected_stdout
        elif isinstance(expected_stdout, str):
            self.expected_stdout = expected_stdout.encode()
        else:
            raise TypeError('Expected stdout must be either a bytes or an str object')

    def _check_expectation(self, completed_process: CompletedProcess) -> ExpectationResult:
        return ExpectationResult(
            expectation=self,
            passed=self.expected_stdout == completed_process.stdout,
            expected=self.expected_stdout,
            got=completed_process.stdout,
        )
