import unittest
from osirisvalidator.string import ValidationException
from osirisvalidator.string import not_blank, not_empty, is_digit, is_alnum, is_alnum_space
from osirisvalidator.string import is_alpha, is_alpha_space, match_regex, string_len


class TestString(unittest.TestCase):

    def test_not_empty_str_null(self):
        @not_empty(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = None
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_not_empty_str_empty(self):
        @not_empty(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = ''
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_not_empty_str_blank(self):
        @not_empty(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '    '
        self.assertEqual(validation(None, 1, value), value)

    def test_not_empty_str_filled(self):
        @not_empty(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '1234 45a123'
        self.assertEqual(validation(None, 1, value), value)

    def test_not_blank_str_null(self):
        @not_blank(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = None
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_not_blank_str_empty(self):
        @not_blank(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = ''
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_not_blank_str_blank(self):
        @not_blank(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '    '
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_not_blank_str_filled(self):
        @not_blank(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '1234 45a123'
        self.assertEqual(validation(None, 1, value), value)

    def test_is_alpha_str_with_digits(self):
        @is_alpha(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'H3ll0W0rld'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_is_alpha_str_alpha(self):
        @is_alpha(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'HelloWorld'
        self.assertEqual(validation(None, 1, value), value)

    def test_is_alpha_space_str_with_digits(self):
        @is_alpha_space(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'H3ll0 W0rld'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_is_alpha_space_str_alpha(self):
        @is_alpha_space(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'Hello World'
        self.assertEqual(validation(None, 1, value), value)

    def test_is_alnum_str_with_special_char(self):
        @is_alnum(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'H3ll0@@W0rld!'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_is_alnum_str_alpha(self):
        @is_alnum(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'HelloWorld12'
        self.assertEqual(validation(None, 1, value), value)

    def test_is_alnum_space_str_with_special_char(self):
        @is_alnum_space(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'H3ll0 W0rld!!'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_is_alnum_space_str_alpha(self):
        @is_alnum_space(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'Hello World 1234'
        self.assertEqual(validation(None, 1, value), value)

    def test_is_digit_str_with_alpha(self):
        @is_digit(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '123 3124a'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_is_digit_str_digit(self):
        @is_digit(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '123412'
        self.assertEqual(validation(None, 1, value), value)

    def test_string_len_undersized(self):
        @string_len(field='field', min=3, max=5)
        def validation(obj, key, field_value):
            return field_value
        value = 'ab'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_string_len_oversized(self):
        @string_len(field='field', min=3, max=5)
        def validation(obj, key, field_value):
            return field_value
        value = 'abc de'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_string_len_fitted(self):
        @string_len(field='field', min=3, max=5)
        def validation(obj, key, field_value):
            return field_value
        value = 'abcde'
        self.assertEqual(validation(None, 1, value), value)

    def test_match_regex_wrong_str(self):
        @match_regex(field='field', regex=r'^a...s$')
        def validation(obj, key, field_value):
            return field_value
        value = 'brocolis'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_match_regex_correct_str(self):
        @match_regex(field='field', regex=r'^a...s$')
        def validation(obj, key, field_value):
            return field_value
        value = 'alias'
        self.assertEqual(validation(None, 1, value), value)

    def test_br_mobile_number_incorrect(self):
        @string_len(field='field', min=11, max=11)
        @is_digit(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '418883133131'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_br_mobile_number_correct(self):
        @string_len(field='field', min=11, max=11)
        @is_digit(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '41888313313'
        self.assertEqual(validation(None, 1, value), value)
