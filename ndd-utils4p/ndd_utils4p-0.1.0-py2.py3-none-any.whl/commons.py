"""
Commons stuff for this library.
"""

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any


class Exporter(ABC):
    """
    Export data to another format.
    """

    @abstractmethod
    def export(self, data: Any) -> Any:
        """
        Export the given data to another format.
        Args:
            data: the data to export
        Returns:
            The exported data in the format of the actual exporter
        """
        raise NotImplementedError


class FileSerializer(ABC):
    """
    Load/save data from/to files.
    """

    @abstractmethod
    def load(self, input_file_path: Path) -> Any:
        """
        Load data from the given file.
        Args:
            input_file_path (Path): The path of the file to load data from
        Returns:
            The loaded data
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, data: Any, output_file_path: Path) -> Any:
        """
        Save the given data to the given file.
        Args:
            data (Any): The data to save
            output_file_path (Path): The path of the file to save data into
        Returns:
            The saved data
        """
        raise NotImplementedError

    @abstractmethod
    def default_extension(self) -> str:
        """
        Returns:
            str: The default file extension without the dot, e.g. 'txt'
        """
        raise NotImplementedError
