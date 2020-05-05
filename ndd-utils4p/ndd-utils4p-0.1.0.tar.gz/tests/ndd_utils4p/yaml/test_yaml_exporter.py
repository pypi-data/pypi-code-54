from typing import Dict
from typing import List
from typing import Union

import jsonschema
import pytest
from expects import *
from ndd_test4p.test_cases import AbstractTest

from ndd_utils4p.json import JsonSchemaValidator
from ndd_utils4p.yaml import YamlExporter


class TestYamlExporter(AbstractTest):

    @pytest.fixture()
    def invalid_data(self) -> Union[Dict, List]:
        return self._test_data_from_yaml('invalid-data.yaml')

    @pytest.fixture()
    def invalid_schema_validator(self) -> JsonSchemaValidator:
        return JsonSchemaValidator(self._test_data_file_path('invalid-schema.json'))

    @pytest.fixture()
    def valid_data(self) -> Union[Dict, List]:
        return self._test_data_from_yaml('valid-data.yaml')

    @pytest.fixture()
    def valid_schema_validator(self) -> JsonSchemaValidator:
        return JsonSchemaValidator(self._test_data_file_path('valid-schema.json'))

    def test_export_without_schema(self, valid_data):
        exporter = YamlExporter()
        actual_result = exporter.export(valid_data)
        expected_result = "---\nname: '12345'\n"
        expect(actual_result).to(equal(expected_result))

    def test_export_with_schema(self, valid_schema_validator, valid_data):
        exporter = YamlExporter(valid_schema_validator)
        actual_result = exporter.export(valid_data)
        expected_result = "---\nname: '12345'\n"
        expect(actual_result).to(equal(expected_result))

    def test_export_with_invalid_schema(self, invalid_schema_validator, valid_data):
        exporter = YamlExporter(invalid_schema_validator)
        with pytest.raises(RuntimeError) as error_info:
            exporter.export(valid_data)
        expect(error_info.value.__cause__).to(be_a(jsonschema.exceptions.SchemaError))
        expect(error_info.value.__cause__.message).to(equal("'invalid' is not valid under any of the given schemas"))

    def test_export_with_invalid_data(self, valid_schema_validator, invalid_data):
        exporter = YamlExporter(valid_schema_validator)
        with pytest.raises(RuntimeError) as error_info:
            exporter.export(invalid_data)
        expect(error_info.value.__cause__).to(be_a(jsonschema.exceptions.ValidationError))
        expect(error_info.value.__cause__.message).to(equal("'1' is too short"))
