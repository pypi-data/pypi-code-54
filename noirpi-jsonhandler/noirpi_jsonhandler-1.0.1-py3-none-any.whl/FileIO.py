import json
import os
import traceback
from pathlib import Path
from random import randint


class InvalidFileIOCall(Exception):
    pass


class FileIO:
    def __init__(self, filepath, io, data=None):
        self.filepath = filepath
        self.io = io
        self.data = data

    @staticmethod
    def fileio(filepath, io, data=None):
        """

        :param filepath: Full Filepath including Filename
        :param io: action [save, load, check]
        :param data: json formatted data to save
        :return:
        """
        if io == "save" and data is not None:
            return FileIO.save_json(filepath, data)
        elif io == "load" and data is None:
            return FileIO._read_json(filepath)
        elif io == "check" and data is None:
            return FileIO.is_valid_json(filepath)
        else:
            raise InvalidFileIOCall("FileIO was called with invalid parameters")

    @staticmethod
    def is_valid_json(filepath):
        """Verifies if json file exists / is readable
        :param filepath Full Filepath including Filename"""
        try:
            FileIO._read_json(filepath)
            return True
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return False

    @staticmethod
    def load_json(filepath):
        """Loads json file
        :param filepath Full Filepath including Filename"""
        return FileIO._read_json(filepath)

    @staticmethod
    def _read_json(filepath):
        """internally used function to read a json File
        :param filepath Full Filepath including Filename"""
        with open(filepath, encoding='utf-8', mode="r") as f:
            return json.loads(f.read())

    @staticmethod
    def _save_json(filepath, data):
        """internally used function to read a json File
        :param filepath Full Filepath including Filename
        :param data: json formatted data to save"""
        with open(filepath, encoding='utf-8', mode="w") as f:
            json.dump(data, f, indent=4, sort_keys=True,
                      separators=(',', ' : '))
        return data

    # noinspection PySameParameterValue
    @staticmethod
    def save_json(filepath, data):
        """Automically saves json file
        :param filepath Full Filepath including Filename
        :param data: json formatted data to save"""
        rnd = randint(1000, 9999)
        path, ext = os.path.splitext(filepath)
        tmp_file = "{}-{}.tmp".format(path, rnd)
        FileIO._save_json(tmp_file, data)
        try:
            FileIO._read_json(tmp_file)
        except json.decoder.JSONDecodeError as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            print(f"Attempted to write file {filepath} but JSON integrity check on tmp file has failed.")
            print(f"The original file is unaltered.")
            return False
        os.replace(tmp_file, f"{filepath}")
        return True

    @staticmethod
    def check_files(path: str, filename: str, default_value):
        """check if file exists or create one
        :param path Path to file
        :param filename Filename
        :param default_value Default Value to input in a new created Json"""
        if not FileIO.fileio(f"{path}/{filename}", "check"):
            Path(path).mkdir(parents=True, exist_ok=True)
            print(f"Creating empty {filename}")
            FileIO.fileio(f"{path}/{filename}", "save", default_value)

    @staticmethod
    def get_value(filepath, *path):
        """get a value from a json File
        :param filepath Full filepath including Filename
        :param path Path inside the File (json standard use)"""
        _dict = FileIO.fileio(filepath, "load")
        for part in path:
            _dict = _dict[part]
        return _dict

    @staticmethod
    def set_value(filepath, add, *path):
        """get a value from a json File
        :param filepath Full filepath including Filename
        :param add Value to add into the json file
        :param path Path inside the File (json standard use)"""
        _dict = FileIO.fileio(filepath, "load")
        for part in path:
            try:
                if part == path[-1]:
                    _dict[part] = add
                elif not isinstance(_dict[part], dict):
                    _dict[part] = {}
                    _dict = _dict[part]
                else:
                    _dict = _dict[part]
            except KeyError:
                _dict[part] = {}
                _dict = _dict[part]
        FileIO.fileio(filepath, "save", _dict)
        return True
