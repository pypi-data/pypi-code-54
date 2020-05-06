from dataclasses import dataclass
from typing import List

from ftests.expectation_result import ExpectationResult
from ftests.test_cases import TestCase


@dataclass
class TestResult:
    test_case: TestCase
    expectations_results: List[ExpectationResult]

    def __str__(self):
        string = f'--- {self.test_case.name} ---\n'
        if self.is_passed():
            string += 'Passed'
        else:
            string += '\n'.join([str(result) for result in self.get_failed_expectations_results()])
        return string

    def is_passed(self):
        return all([result.passed for result in self.expectations_results])

    def get_failed_expectations_results(self):
        return [result for result in self.expectations_results if not result.passed]
