"""
Utilities dealing with text.
"""

import logging
from pathlib import Path

from ndd_utils4p.commons import FileSerializer

LOGGER = logging.getLogger(__name__)


class TextFileSerializer(FileSerializer):
    """
    Load/save text from/to files.
    """

    def load(self, input_file_path: Path) -> str:
        """
        Load text from the given text file.
        Args:
            input_file_path (Path): The path of the file to load text from
        Returns:
            The loaded text
        """
        LOGGER.debug('Loading data from text file "%s"', input_file_path)
        return input_file_path.read_text()

    def save(self, data: str, output_file_path: Path) -> str:
        """
        Save the given text to the given text file.
        Args:
            data (Any): The text to save
            output_file_path (Path): The path of the file to save text into
        Returns:
            The saved text
        """
        LOGGER.debug('Saving data to text file "%s"', output_file_path)
        output_file_path.write_text(data)
        return data

    def default_extension(self) -> str:
        """
        Returns:
            str: The default text file extension without the dot, i.e. 'txt'
        """
        return 'txt'
