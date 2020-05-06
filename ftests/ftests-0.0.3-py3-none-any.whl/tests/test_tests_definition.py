import unittest
from unittest.mock import patch, mock_open

from ftests.test_cases import CommandTestCase
from ftests.tests_definition import TestsDefinition


class TestsDefinitionTest(unittest.TestCase):
    def test_parsing_correct_yaml(self):
        with patch("builtins.open",
                   mock_open(read_data="""
        tests:
          - name: First test
            type: command
            command: python3 -m ftests
            expected:
              return_code: 0
          - name: Another one
            type: command
            command: python3 -m ftests invalid_argument
            expected: # Some comment
              return_code: 1""")) as mock_file:
            tests_definition = TestsDefinition('mocked/path')
            mock_file.assert_called_with('mocked/path', 'r')

            self.assertIsInstance(tests_definition.test_cases, list)
            self.assertEqual(2, len(tests_definition.test_cases))
            first_test_case = tests_definition.test_cases[0]
            self.assertIsInstance(first_test_case, CommandTestCase)
            second_test_case = tests_definition.test_cases[1]
            self.assertIsInstance(second_test_case, CommandTestCase)

    def test_parsing_incorrect_yaml(self):
        with patch("builtins.open",
                   mock_open(read_data="I am not a YAML")) as _:
            try:
                TestsDefinition('')
                self.fail('TestsDefinition should raise a ValueError if the YAML file is invalid.')
            except ValueError:
                return


if __name__ == '__main__':
    unittest.main()
