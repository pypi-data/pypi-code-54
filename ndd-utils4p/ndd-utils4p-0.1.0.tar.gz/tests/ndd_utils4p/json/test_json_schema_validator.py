from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

import jsonschema
import pytest
from expects import *
from ndd_test4p.test_cases import AbstractTest

from ndd_utils4p.json import JsonSchemaValidator


class TestJsonSchemaValidator(AbstractTest):

    @pytest.fixture()
    def invalid_data(self) -> Union[Dict, List]:
        return self._test_data_from_json('invalid-data.json')

    @pytest.fixture()
    def valid_data(self) -> Union[Dict, List]:
        return self._test_data_from_json('valid-data.json')

    @pytest.fixture()
    def invalid_schema_path(self) -> Path:
        return self._test_data_file_path('invalid-schema.json')

    @pytest.fixture()
    def valid_schema_path(self) -> Path:
        return self._test_data_file_path('valid-schema.json')

    def test_validate_with_invalid_schema(self, invalid_schema_path, valid_data):
        validator = JsonSchemaValidator(invalid_schema_path)
        with pytest.raises(RuntimeError) as error_info:
            validator.validate(valid_data)
        expect(error_info.value.__cause__).to(be_a(jsonschema.exceptions.SchemaError))
        expect(error_info.value.__cause__.message).to(equal("'invalid' is not valid under any of the given schemas"))

    def test_validate_with_invalid_data(self, valid_schema_path, invalid_data):
        validator = JsonSchemaValidator(valid_schema_path)
        with pytest.raises(RuntimeError) as error_info:
            validator.validate(invalid_data)
        expect(error_info.value.__cause__).to(be_a(jsonschema.exceptions.ValidationError))
        expect(error_info.value.__cause__.message).to(equal("'1' is too short"))

    def test_validate(self, valid_schema_path, valid_data):
        validator = JsonSchemaValidator(valid_schema_path)
        validator.validate(valid_data)
