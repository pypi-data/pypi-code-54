from subprocess import CompletedProcess

from ._completed_process_expectation import CompletedProcessExpectation
from ..expectation_result import ExpectationResult


class ReturnCodeExpectation(CompletedProcessExpectation):
    codename = 'return_code'
    expected_return_code: int

    def __init__(self, expected_return_code: int):
        if not isinstance(expected_return_code, int):
            raise TypeError('Expected return code must be an int')
        self.expected_return_code = expected_return_code

    def _check_expectation(self, completed_process: CompletedProcess) -> ExpectationResult:
        return ExpectationResult(
            expectation=self,
            passed=self.expected_return_code == completed_process.returncode,
            expected=self.expected_return_code,
            got=completed_process.returncode,
        )
