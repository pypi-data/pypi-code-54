import copy
from marshmallow import ValidationError
from sqlalchemy.orm.exc import (
    NoResultFound,
)
from parameterized import parameterized

from test.backendtestcase import TestCase
from test.utils import second_equals_first
from src.cs_models.resources.DrugIndication import DrugIndication


class DrugIndicationResourceTestCase(TestCase):
    def setUp(self):
        super(DrugIndicationResourceTestCase, self).setUp()
        self.inst = DrugIndication()

        self.indication1 = self.inst.create({
            'appl_no': '021142',
            'appl_type': 'N',
            'indication': "plaque psoriasis",
        })

        self.indication2 = self.inst.create({
            'appl_no': '022518',
            'appl_type': 'N',
            'indication': "asthma",
        })

        self.valid_data = {
            'appl_no': '204412',
            'appl_type': 'N',
            'indication': "ulcerative colitis",
        }

    @parameterized.expand([
        ('appl_type',),
    ])
    def test_create_validation_error_missing_field(self, field_to_pop):
        base_data = copy.copy(self.valid_data)
        base_data.pop(field_to_pop)
        self.assertRaises(
            ValidationError,
            self.inst.create,
            base_data,
        )

    def test_create(self):
        resp = self.inst.create(self.valid_data)
        expected_data = {
            **self.valid_data,
        }
        second_equals_first(expected_data, resp)

    def test_read(self):
        resp = self.inst.read({})
        self.assertEqual(2, len(resp))

    @parameterized.expand([
        ('id', 'indication1', 'id', 1),
        ('indication', 'indication1', 'indication', 2),
    ])
    def test_read_w_params(
        self,
        field_name,
        attr,
        attr_field,
        expected_length,
    ):
        resp = self.inst.read({})
        self.assertEqual(2, len(resp))

        resp = self.inst.read({
            field_name: getattr(self, attr)[attr_field],
        })
        self.assertEqual(expected_length, len(resp))

    @parameterized.expand([
        ('id', 999, NoResultFound),
    ])
    def test_one_raises_exception(self, field_name, field_value, exception):
        self.assertRaises(
            exception,
            self.inst.one,
            {
                field_name: field_value,
            },
        )

    @parameterized.expand([
        ('id',),
        ('appl_no',),
    ])
    def test_one(self, field_name):
        resp = self.inst.one({
            field_name: self.indication1[field_name],
        })
        second_equals_first(
            self.indication1,
            resp,
        )

    def test_upsert_validation_error(self):
        self.assertRaises(
            ValidationError,
            self.inst.upsert,
            {
                'appl_no': self.valid_data['appl_no'],
            }
        )

    def test_upsert_creates_new_entry(self):
        data = copy.copy(self.valid_data)
        self.assertEqual(2, len(self.inst.read({})))
        self.inst.upsert(data)
        self.assertEqual(3, len(self.inst.read({})))

    def test_upsert_updates_existing_row(self):
        data = {
            **self.valid_data,
            **{'appl_no': self.indication1['appl_no'],
               'appl_type': self.indication1['appl_type'],
               'indication': self.indication1['indication']
               },
        }
        resp = self.inst.upsert(data)
        expected_data = {
            **data,
        }
        second_equals_first(
            expected_data,
            resp,
        )
        self.assertEqual(2, len(self.inst.read({})))
