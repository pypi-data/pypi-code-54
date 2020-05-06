import unittest

from ftests.test_cases import TestCase


class MockTestCase(TestCase):

    def launch(self):
        """Nothing need to be done here"""

    @staticmethod
    def from_dict(data_dict: dict):
        """Nothing need to be done here"""


class TestCaseTest(unittest.TestCase):

    def test_abstractness(self):
        self.assertRaises(TypeError, TestCase)

    def test_codename(self):
        self.assertIsNone(TestCase.codename)

    def test_name_arg_good_type_check(self):
        mock_tc = MockTestCase('Mock test name')
        self.assertEqual('Mock test name', mock_tc.name)

    def _test_bad_name_arg_check(self, arg):
        try:
            MockTestCase(arg)
            self.fail('TestCase should only accept string names')
        except TypeError:
            return

    def test_name_arg_bad_type_check(self):
        self._test_bad_name_arg_check(42)
        self._test_bad_name_arg_check(b'Binary name')
        self._test_bad_name_arg_check(1.5)
        self._test_bad_name_arg_check(None)


if __name__ == '__main__':
    unittest.main()
