from abc import ABC, abstractmethod
from subprocess import CompletedProcess

from ._base_expectation import Expectation
from ..expectation_result import ExpectationResult


class CompletedProcessExpectation(Expectation, ABC):

    @abstractmethod
    def _check_expectation(self, completed_process: CompletedProcess) -> ExpectationResult:
        raise NotImplementedError

    def is_expectation_met(self, result: CompletedProcess) -> ExpectationResult:
        if isinstance(result, CompletedProcess):
            return self._check_expectation(result)
        else:
            raise TypeError('CompletedProcessExpectation subclasses expects a CompletedProcess object for checking.')
