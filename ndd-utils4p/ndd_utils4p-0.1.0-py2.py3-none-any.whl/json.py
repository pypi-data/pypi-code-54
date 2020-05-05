"""
Utilities dealing with JSON.
"""

import json
import logging
from pathlib import Path
from typing import Dict

from jsonschema import SchemaError
from jsonschema import validate
from jsonschema import ValidationError

LOGGER = logging.getLogger(__name__)


class JsonSchemaValidator:
    """
    Validate JSON file or JSON-like data using a JSON schema.
    """

    def __init__(self, schema_file_path: Path):
        """
        Args:
            schema_file_path (pathlib.Path): The file of the JSON schema to use.
        """
        self._schema_file_path = schema_file_path
        self._schema = json.loads(schema_file_path.read_text())

    def validate(self, variables: Dict) -> None:
        """
        Args:
            variables (Dict): The data to validate using the given JSON schema.
        """
        try:
            LOGGER.debug('Validating JSON using schema "%s"', self._schema_file_path.as_posix())
            validate(instance=variables, schema=self._schema)
        except ValidationError as error:
            message = f'Validation failed using schema "{self._schema_file_path.as_posix()}"'
            LOGGER.exception(message)
            raise RuntimeError(message) from error
        except SchemaError as error:
            message = f'Invalid schema: {self._schema_file_path.as_posix()}'
            LOGGER.exception(message)
            raise RuntimeError(message) from error
