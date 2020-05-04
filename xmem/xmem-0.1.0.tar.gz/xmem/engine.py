import atexit
from pathlib import Path
from typing import Dict, Union

from .template import MemoryTemplate

DICT_EXPOSED_METHODS = ['clear', 'items']


class MemoryEngine(object):
    _data: Dict
    _location: Path
    _template: MemoryTemplate

    def __init__(self, location: Union[Path, str], template: MemoryTemplate, auto_load=True):
        """
        :param location: path to save file
        :param template: memory template
        """

        self._data = {}
        self._template = template

        # update location
        self.location = location

        # exposing dictionary methods
        self.clear = self._data.clear
        self.items = self._data.items

        # for method in DICT_EXPOSED_METHODS:
        #     setattr(self, method, getattr(self._data, method))

        # read the initial data

        if auto_load:
            self.load()

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value: Union[Path, str]):
        # conversion
        if type(value) != Path:
            self._location = Path(value)
        else:
            self._location = value

        # making sure directory exists
        self._location.parent.mkdir(parents=True, exist_ok=True)

        # updating template location attribute
        self._template.location = self._location

    @property
    def template(self):
        return self._template

    def save(self):
        """
        write current data to disk
        """
        self._template.save(self._data)

    def load(self):
        """
        read data from disk
        """
        try:
            self._data = self._template.load()
        except FileNotFoundError:
            self.save()

    def get(self, key, default=None):
        """
        :param key: key used as identifier
        :param default: value to return is key not found

        :return: data corresponding to identifer(key)
        :returns: default if key not found
        """
        try:
            value = self._data[key]
        except KeyError:
            value = default

        return value

    def delete(self, *args):
        """
        removes the keys from memory

        :param args: keys to be removed
        """
        for key in args:
            try:
                del self._data[key]
            except KeyError:
                pass

    def put(self, key, value):
        """
        adds key-value pair to memory

        :param key: key used as identifier
        :param value: data to store
        :return: self, may be chained
        """
        self._data[key] = value

        return self

    def putall(self, d: dict):
        """
        adds all the key-value pairs in the map

        :param d: dictionary map to be stored
        """
        for key, value in d.items():
            self._data[key] = value

    def save_atexit(self, should_save=True):
        """
        register save function to atexit module

        :param should_save: whether to register or unregister
        """
        if should_save:
            atexit.register(self.save)
        else:
            atexit.unregister(self.save)