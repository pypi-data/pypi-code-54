import unittest
from osirisvalidator.intl.br import valid_cpf, valid_cep, valid_cnpj, ValidationException


class TestBR(unittest.TestCase):

    def test_cpf_random_string(self):
        @valid_cpf(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'a6712gdsa!das1'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_cpf_invalid_len(self):
        @valid_cpf(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '1234'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_cpf_invalid_cpf(self):
        @valid_cpf(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '12345678911'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_cpf_repeated_numbers(self):
        @valid_cpf(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '11111111111'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_cpf_valid_cpf(self):
        @valid_cpf(field='field')
        def validation(obj, key, field_value):
            return field_value

        value = '36041181404'
        self.assertEqual(validation(None, 1, value), value)

    def test_cnpj_random_string(self):
        @valid_cnpj(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = 'a6712gdsa!das1'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_cnpj_invalid_len(self):
        @valid_cnpj(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '12345678901'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_cnpj_invalid_cnpj(self):
        @valid_cnpj(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '12345678901234'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_cnpj_repeated_numbers(self):
        @valid_cnpj(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '11111111111111'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_cnpj_valid_cnpj(self):
        @valid_cnpj(field='field')
        def validation(obj, key, field_value):
            return field_value

        value = '37445306000161'
        self.assertEqual(validation(None, 1, value), value)

    def test_cep_invalid_len(self):
        @valid_cep(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '8402002012'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_cep_random_string(self):
        @valid_cep(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '84a20020'
        self.assertRaises(ValidationException, validation, None, 1, value)

    def test_cep_valid(self):
        @valid_cep(field='field')
        def validation(obj, key, field_value):
            return field_value
        value = '84020020'
        self.assertEqual(validation(None, 1, value), value)
