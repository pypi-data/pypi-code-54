import unittest
from osirisvalidator.internet import valid_email, ValidationException


class TestInternet(unittest.TestCase):

    def test_email_blank_email(self):
        @valid_email(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = ''
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_email_invalid_email(self):
        @valid_email(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'email@testmail'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_email_valid_email(self):
        @valid_email(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'email.test@testmail.domain.name'
        self.assertEqual(validation(None, 1, value), value)
