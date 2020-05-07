import unittest
import geta.name as name


class TestGenerateName(unittest.TestCase):

    def test_get_first_name(self):
        first_name = name.first_name()
        self.assertEqual(1, len(first_name.split(" ")))

    def test_get_last_name(self):
        last_name = name.last_name()
        self.assertEqual(1, len(last_name.split(" ")))

    def test_get_full_name(self):
        last_name = name.full_name()
        self.assertEqual(2, len(last_name.split(" ")))
