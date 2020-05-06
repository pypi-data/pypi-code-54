import unittest

from ftests.expectation_result import ExpectationResult
from ftests.expectations import Expectation


class DummyExpectation(Expectation):
    codename = 'dummy'

    def is_expectation_met(self, result) -> bool:
        return True


class ExpectationResultTest(unittest.TestCase):

    def test_str_success(self):
        self.assertEqual('Passed', str(ExpectationResult(expectation=DummyExpectation(),
                                                         passed=True, expected='Good', got='Good')))

    def test_str_fail_str_args(self):
        self.assertEqual('Failed "dummy" expectation\nExpected: \'OK\'\nGot: \'KO\'',
                         str(ExpectationResult(expectation=DummyExpectation(),
                                               passed=False, expected='OK', got='KO')))

    def test_str_fail_int_args(self):
        self.assertEqual('Failed "dummy" expectation\nExpected: 0\nGot: 42',
                         str(ExpectationResult(expectation=DummyExpectation(),
                                               passed=False, expected=0, got=42)))
        self.assertEqual('Failed "dummy" expectation\nExpected: -7\nGot: -21',
                         str(ExpectationResult(expectation=DummyExpectation(),
                                               passed=False, expected=-7, got=-21)))

    def test_str_fail_mixed_args(self):
        self.assertEqual('Failed "dummy" expectation\nExpected: 0\nGot: \'42\'',
                         str(ExpectationResult(expectation=DummyExpectation(),
                                               passed=False, expected=0, got='42')))
        self.assertEqual('Failed "dummy" expectation\nExpected: \'-7\'\nGot: -21',
                         str(ExpectationResult(expectation=DummyExpectation(),
                                               passed=False, expected='-7', got=-21)))

    def test_str_fail_none_args(self):
        self.assertEqual('Failed "dummy" expectation\nExpected: <None>\nGot: \'Something\'',
                         str(ExpectationResult(expectation=DummyExpectation(),
                                               passed=False, expected=None, got='Something')))
        self.assertEqual('Failed "dummy" expectation\nExpected: \'Something\'\nGot: <None>',
                         str(ExpectationResult(expectation=DummyExpectation(),
                                               passed=False, expected='Something', got=None)))
