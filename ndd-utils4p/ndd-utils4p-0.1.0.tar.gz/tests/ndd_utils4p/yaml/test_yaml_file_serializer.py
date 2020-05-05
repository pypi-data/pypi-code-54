from abc import ABC
from pathlib import Path

import jsonschema
import pytest
from expects import *
from ndd_test4p.test_cases import AbstractTest

from ndd_utils4p.json import JsonSchemaValidator
from ndd_utils4p.yaml import YamlFileSerializer


class TestYamlFileSerializer(AbstractTest, ABC):

    @pytest.fixture()
    def invalid_data(self):
        return self._test_data_from_yaml('invalid-data.yaml')

    @pytest.fixture()
    def invalid_data_path(self):
        return self._test_data_file_path('invalid-data.yaml')

    @pytest.fixture()
    def invalid_schema_validator(self) -> JsonSchemaValidator:
        return JsonSchemaValidator(self._test_data_file_path('invalid-schema.json'))

    @pytest.fixture()
    def valid_data(self):
        return self._test_data_from_yaml('valid-data.yaml')

    @pytest.fixture()
    def valid_data_path(self):
        return self._test_data_file_path('valid-data.yaml')

    @pytest.fixture()
    def valid_schema_validator(self) -> JsonSchemaValidator:
        return JsonSchemaValidator(self._test_data_file_path('valid-schema.json'))

    def test_default_extension(self, valid_schema_validator):
        serializer = YamlFileSerializer(valid_schema_validator)
        expect(serializer.default_extension()).to(equal('yaml'))


class TestYamlFileSerializer_Load(TestYamlFileSerializer):

    def test_load_without_schema(self, valid_data_path):
        serializer = YamlFileSerializer()
        data = serializer.load(valid_data_path)
        expect(data).to(equal({'name': '12345'}))

    def test_load_with_schema(self, valid_schema_validator, valid_data_path):
        serializer = YamlFileSerializer(valid_schema_validator)
        data = serializer.load(valid_data_path)
        expect(data).to(equal({'name': '12345'}))

    def test_load_with_invalid_schema(self, invalid_schema_validator, valid_data_path):
        serializer = YamlFileSerializer(invalid_schema_validator)
        with pytest.raises(RuntimeError) as error_info:
            serializer.load(valid_data_path)
        expect(error_info.value.__cause__).to(be_a(jsonschema.exceptions.SchemaError))
        expect(error_info.value.__cause__.message).to(equal("'invalid' is not valid under any of the given schemas"))

    def test_load_with_invalid_data(self, valid_schema_validator, invalid_data_path):
        serializer = YamlFileSerializer(valid_schema_validator)
        with pytest.raises(RuntimeError) as error_info:
            serializer.load(invalid_data_path)
        expect(error_info.value.__cause__).to(be_a(jsonschema.exceptions.ValidationError))
        expect(error_info.value.__cause__.message).to(equal("'1' is too short"))


class TestYamlFileSerializer_Save(TestYamlFileSerializer):

    @pytest.fixture()
    def actual_result_path(self, tmp_path: Path):
        return tmp_path.joinpath('actual-data.yaml')

    def test_save_without_schema(self, valid_data, actual_result_path):
        serializer = YamlFileSerializer()
        actual_result = serializer.save(valid_data, actual_result_path)
        expected_result = "---\nname: '12345'\n"
        expect(actual_result).to(equal(expected_result))
        expect(actual_result_path.read_text()).to(equal(expected_result))

    def test_save_with_schema(self, valid_schema_validator, valid_data, actual_result_path):
        serializer = YamlFileSerializer(valid_schema_validator)
        actual_result = serializer.save(valid_data, actual_result_path)
        expected_result = "---\nname: '12345'\n"
        expect(actual_result).to(equal(expected_result))
        expect(actual_result_path.read_text()).to(equal(expected_result))

    def test_save_with_invalid_schema(self, invalid_schema_validator, valid_data, actual_result_path):
        serializer = YamlFileSerializer(invalid_schema_validator)
        with pytest.raises(RuntimeError) as error_info:
            serializer.save(valid_data, actual_result_path)
        expect(error_info.value.__cause__).to(be_a(jsonschema.exceptions.SchemaError))
        expect(error_info.value.__cause__.message).to(equal("'invalid' is not valid under any of the given schemas"))

    def test_save_with_invalid_data(self, valid_schema_validator, invalid_data, actual_result_path):
        serializer = YamlFileSerializer(valid_schema_validator)
        with pytest.raises(RuntimeError) as error_info:
            serializer.save(invalid_data, actual_result_path)
        expect(error_info.value.__cause__).to(be_a(jsonschema.exceptions.ValidationError))
        expect(error_info.value.__cause__.message).to(equal("'1' is too short"))
