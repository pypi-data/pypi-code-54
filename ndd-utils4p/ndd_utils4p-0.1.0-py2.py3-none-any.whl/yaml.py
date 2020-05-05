"""
Utilities dealing with YAML.
"""

import logging
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

import yaml

from ndd_utils4p.commons import Exporter
from ndd_utils4p.commons import FileSerializer
from ndd_utils4p.json import JsonSchemaValidator

LOGGER = logging.getLogger(__name__)


class YamlExporter(Exporter):
    """
    Export data to YAML optionally using a JSON schema for validation.
    """

    def __init__(self, schema_validator: JsonSchemaValidator = None):
        """
        Args:
            schema_validator (ndd_utils4p.json.JsonSchemaValidator): The JSON schema validator to use.
        """
        self._schema_validator = schema_validator
        yaml.Dumper.ignore_aliases = lambda *args: True

    def export(self, data: Union[Dict, List]) -> str:
        """
        Export the given data to YAML.
        Args:
            data (Union[Dict, List]): The data to export
        Returns:
            str: The exported data as YAML
        """
        LOGGER.debug('Exporting data to YAML')
        data_as_dict = self._validate(data)
        data_as_yaml = yaml.dump(data_as_dict, default_flow_style=False, explicit_start=True)
        return data_as_yaml

    def _validate(self, data: Union[Dict, List]) -> Union[Dict, List]:
        """
        Validate The given data against the JSON schema if specified.
        Args:
            data (Union[Dict, List]): The data to validate
        Returns:
            Union[Dict, List]: The validated data
        """
        if self._schema_validator:
            self._schema_validator.validate(data)
        return data


class YamlFileSerializer(FileSerializer):
    """
    Load/save YAML from/to files.
    """

    def __init__(self, schema_validator: JsonSchemaValidator = None):
        """
        Args:
            schema_validator (ndd_utils4p.json.JsonSchemaValidator): The JSON schema validator to use.
        """
        self._schema_validator = schema_validator
        yaml.Dumper.ignore_aliases = lambda *args: True

    def load(self, input_file_path: Path) -> Union[Dict, List]:
        """
        Load data from the given YAML file before validation against the JSON schema if specified.
        Args:
            input_file_path (Path): The path of the file to load data from
        Returns:
            The loaded data
        """
        LOGGER.debug('Loading data from YAML file "%s"', input_file_path)
        file_content_as_yaml = input_file_path.read_text()
        file_content_as_dict = yaml.safe_load(file_content_as_yaml)
        file_content_as_dict = self._validate(file_content_as_dict)
        return file_content_as_dict

    def save(self, data: Union[Dict, List], output_file_path: Path) -> str:
        """
        Save the given data to the given YAML file after validation against the JSON schema if specified.
        Args:
            data (Union[Dict, List]): The data to save
            output_file_path (Path): The path of the file to save data into
        Returns:
            The saved data as YAML
        """
        LOGGER.debug('Saving data to YAML file "%s"', output_file_path)
        file_content_as_dict = self._validate(data)
        file_content_as_yaml = '---\n' + yaml.dump(file_content_as_dict, default_flow_style=False)
        output_file_path.write_text(file_content_as_yaml)
        return file_content_as_yaml

    def default_extension(self) -> str:
        """
        Returns:
            str: The default YAML file extension without the dot, i.e. 'yaml'
        """
        return 'yaml'

    def _validate(self, data: Union[Dict, List]) -> Union[Dict, List]:
        """
        Validate The given data against the JSON schema if specified.
        Args:
            data (Union[Dict, List]): The data to validate
        Returns:
            Union[Dict, List]: The validated data
        """
        if self._schema_validator:
            self._schema_validator.validate(data)
        return data
