from dataclasses import dataclass

from ftests.expectations import Expectation


@dataclass
class ExpectationResult:
    expectation: Expectation
    passed: bool
    expected: object
    got: object

    def __str__(self):
        if self.passed:
            return 'Passed'
        else:
            return '\n'.join([
                f'Failed "{self.expectation.codename}" expectation',
                f'Expected: {repr(self.expected) if self.expected is not None else "<None>"}',
                f'Got: {repr(self.got) if self.got is not None else "<None>"}'
            ])
