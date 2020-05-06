from typing import List

import yaml

from ftests.test_cases import TestCase
from ftests.test_result import TestResult
from tests.helpers import all_subclasses


class TestsDefinition:
    _yaml: dict
    test_cases: List[TestCase]

    def __init__(self, file_path: str):
        with open(file_path, 'r') as yaml_file:
            self._yaml = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
            if not isinstance(self._yaml, dict):
                raise ValueError(f'{file_path} is not a valid YAML file.')
            self.__load_test_cases(self._yaml['tests'])

    def __load_test_cases(self, test_list: list):
        self.test_cases = []
        for case_dict in test_list:
            type_codename = case_dict['type']
            case_class = TestsDefinition.__get_test_case_for_codename(type_codename)
            self.test_cases.append(case_class.from_dict(case_dict))

    def launch_tests(self) -> List[TestResult]:
        results: List[TestResult] = []
        for test in self.test_cases:
            result = test.launch()
            print(result)
            results.append(result)
        return results

    @staticmethod
    def __get_test_case_for_codename(codename):
        test_case: TestCase
        for test_case in all_subclasses(TestCase):
            if test_case.codename == codename:
                return test_case
        raise ValueError(f'Invalid test type with codename "{codename}".')
