"""
Utilities dealing with Jinja2.
"""

import logging
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict

import jmespath
from jinja2 import Environment
from jinja2 import FileSystemLoader

from ndd_utils4p.commons import Exporter
from ndd_utils4p.commons import FileSerializer

LOGGER = logging.getLogger(__name__)


class JinjaExporter(Exporter):
    """
    Export data to text using a Jinja2 template.
    """

    def __init__(self, template_file_path: Path):
        """
        Args:
            template_file_path (Path): The path of the Jinja2 template
        """
        self._template_file_path = template_file_path.absolute()
        self._environment = Environment(loader=FileSystemLoader('/'),
                                        keep_trailing_newline=True,
                                        lstrip_blocks=True,
                                        trim_blocks=True)
        self.add_filter('jmespath', lambda data, expression: jmespath.search(expression, data))

    def export(self, data: Dict) -> str:
        """
        Export the given data to text using the specified Jinja2 template.
        Args:
            data (Dict): The data to export
        Returns:
            str: The exported data as text
        """
        LOGGER.debug('Exporting data using Jinja template "%s"', self._template_file_path.as_posix())
        template = self._environment.get_template(self._template_file_path.as_posix())
        content = template.render(data)
        return content

    def add_filter(self, name: str, function: Callable) -> None:
        """
        Add a Jinja2 filter.
        Args:
            name (str): The name of the filter
            function (Callable): The filter as a function
        """
        self._environment.filters[name] = function


class JinjaFileSerializer(FileSerializer):
    """
    Save text to file using a Jinja2 template.
    """

    @classmethod
    def from_template_file(cls, template_file_path: Path) -> 'JinjaFileSerializer':
        """
        Args:
            template_file_path (Path): The path of the Jinja2 template
        Returns:
            JinjaFileSerializer: A Jinja serializer using the given Jinja2 template
        """
        return JinjaFileSerializer(JinjaExporter(template_file_path))

    def __init__(self, jinja_exporter: JinjaExporter):
        """
        Args:
            jinja_exporter (ndd_utils4p.jinja.JinjaExporter): The Jinja2 exporter to use
        """
        self._jinja_exporter = jinja_exporter

    def load(self, input_file_path: Path) -> Any:
        """
        Not implemented.
        """
        raise NotImplementedError

    def save(self, data: Dict, output_file_path: Path) -> str:
        """
        Save the given data as text using the specified Jinja2 template.
        Args:
            data (Any): The data to save
            output_file_path (Path): The path of the file to save data into
        Returns:
            str: The exported data as text
        """
        content = self._jinja_exporter.export(data)
        LOGGER.debug('Exporting data to file "%s"', output_file_path.as_posix())
        output_file_path.write_text(content)
        return content

    def default_extension(self) -> None:
        """
        Returns:
            str: The default file extension without the dot as specified in the constructor
        """
        return None
