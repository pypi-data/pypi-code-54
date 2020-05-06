import subprocess

from ftests.args_type_checkers import assert_isinstance
from ftests.expectations import CompletedProcessExpectation
from tests.helpers import all_subclasses
from ._test_case import TestCase


class CommandTestCase(TestCase):
    codename = 'command'
    command: str
    expectations: list

    def __init__(self, name: str, command: str, expectations_dict: dict):
        super().__init__(name)
        assert_isinstance(command, str, 'Command must be a string')
        assert_isinstance(expectations_dict, dict, 'Expectations dict must be a dict')
        self.command = command
        self.expectations = self.__get_expectations_from_dict(expectations_dict)

    @staticmethod
    def __get_expectations_from_dict(expectations_dict: dict) -> list:
        expectations_list = []
        for codename, value in expectations_dict.items():
            expectations_type = CommandTestCase.__get_expectation_for_codename(codename)
            if expectations_type:
                expectations_list.append(expectations_type(value))
        return expectations_list

    @staticmethod
    def __get_expectation_for_codename(codename: str):
        expectation: CompletedProcessExpectation
        for expectation in all_subclasses(CompletedProcessExpectation):
            if expectation.codename == codename:
                return expectation
        raise ValueError(f'Invalid expectation with codename "{codename}".')

    def launch(self):
        command_result = subprocess.run(self.command,
                                        shell=True,
                                        capture_output=True,
                                        )
        from ftests.test_result import TestResult
        return TestResult(test_case=self,
                          expectations_results=[e.is_expectation_met(command_result) for e in self.expectations])

    @staticmethod
    def from_dict(data_dict: dict):
        name = data_dict['name']
        command = data_dict['command']
        expectations = data_dict['expected']
        return CommandTestCase(name, command, expectations)
