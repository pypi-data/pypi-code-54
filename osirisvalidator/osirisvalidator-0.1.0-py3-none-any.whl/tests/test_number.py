import unittest
from osirisvalidator.number import min_max, ValidationException


class TestNumber(unittest.TestCase):

    def test_number_len_under(self):
        @min_max(field='field', min=3, max=5)
        def validation(obj, key, field_value):
            return field_value
        value = 2
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_number_len_over(self):
        @min_max(field='field', min=3, max=5)
        def validation(obj, key, field_value):
            return field_value
        value = 7
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_number_len_fitted(self):
        @min_max(field='field', min=3, max=5)
        def validation(obj, key, field_value):
            return field_value
        value = 3
        self.assertEqual(validation(None, 1, value), value)
