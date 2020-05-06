import unittest

from ftests.expectations import ReturnCodeExpectation
from ftests.test_cases import CommandTestCase, TestCase


class CommandTestCaseTest(unittest.TestCase):
    def test_inheritance(self):
        self.assertIsInstance(CommandTestCase('A command test case', 'echo "I am good!"', {}), TestCase)

    def test_codename(self):
        self.assertEqual('command', CommandTestCase.codename)

    def test_command_arg_good_fetching(self):
        case = CommandTestCase('My test case', 'echo success', {})
        self.assertEqual('echo success', case.command)

    def _test_bad_command_arg_check(self, arg):
        try:
            CommandTestCase('Some name', arg, {})
            self.fail('CommandTestCase should only accept string commands')
        except TypeError:
            return

    def test_command_arg_bad_type(self):
        self._test_bad_command_arg_check(42)
        self._test_bad_command_arg_check(b'ls /bin')
        self._test_bad_command_arg_check(['cat', '/some_directory/chocolatine'])
        self._test_bad_command_arg_check(None)

    def test_expectations_parsing(self):
        case = CommandTestCase('A real test case', 'cat my_file.txt',
                               {
                                   'return_code': 2
                               })
        self.assertIsInstance(case.expectations, list)
        self.assertEqual(1, len(case.expectations))
        expectation = case.expectations[0]
        self.assertIsInstance(expectation, ReturnCodeExpectation)
        self.assertEqual(2, expectation.expected_return_code)

    def test_expectations_non_existing(self):
        try:
            CommandTestCase('Some name', 'echo not important',
                            {
                                'non_existing_expectation': 'chocolatine'
                            })
            self.fail('CommandTestCase should not accept non-existing or non-compatible expectations')
        except ValueError:
            return

    def test_from_dict_correct(self):
        case = CommandTestCase.from_dict({
            'name': 'My dictionary case',
            'command': 'echo I was born from a dictionary',
            'expected': {
                'return_code': 0
            }
        })
        self.assertEqual('My dictionary case', case.name)
        self.assertEqual('echo I was born from a dictionary', case.command)
        self.assertIsInstance(case.expectations, list)
        self.assertEqual(1, len(case.expectations))
        expectation = case.expectations[0]
        self.assertIsInstance(expectation, ReturnCodeExpectation)
        self.assertEqual(0, expectation.expected_return_code)

    def test_real_test_successful(self):
        case = CommandTestCase('First real launched test', 'echo successful',
                               {
                                   'return_code': 0
                               })
        self.assertTrue(case.launch().is_passed())

    def test_real_test_unsuccessful(self):
        case = CommandTestCase('First real launched test', '__non_existant_command_1248',
                               {
                                   'return_code': 0
                               })
        self.assertFalse(case.launch().is_passed())


if __name__ == '__main__':
    unittest.main()
