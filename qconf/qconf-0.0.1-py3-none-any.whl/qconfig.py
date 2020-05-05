import os
import re
from collections import UserDict, Mapping
from copy import deepcopy

import yaml

from qconf.qparser import parse_type, decode


class QConfig(UserDict):

    def __init__(self, data, merge_env=False):
        super(QConfig, self).__init__(data)
        if merge_env:
            self.env_overrides()

    def get_sub_config(self, name):
        return QConfig(self.get(name, {}))

    def get_as(self, name, default=None, required=False, as_type=None):
        val = self.get(name, default)
        if required and not val:
            raise AssertionError("Value for " + name + " required but not given")
        return parse_type(val, as_type) if as_type else val

    def get_bool(self, name, default=False, required=False):
        val = self.get_as(name, default, required)
        return str(val).lower() in ['true', '1']

    def get_string(self, name, default=False, required=False):
        return self.get_as(name, default, required, str)

    def get_int(self, name, default=False, required=False):
        return self.get_as(name, default, required, int)

    def get_float(self, name, default=False, required=False):
        return self.get_as(name, default, required, float)

    def get_list(self, name, default=False, required=False):
        return self.get_as(name, default, required, list)

    def get_dict(self, name, default=False, required=False):
        return self.get_as(name, default, required, dict)

    def merge(self, update):
        self.merge_dict(self.data, update)

    def get_path(self, name, default=None, required=False):
        raw = self.get_as(name, default, required)
        return os.sep.join(re.split('[/\\\\]+', raw)) if raw else None

    def load_data_for_keys(self, parent, dir=''):
        for r, path in parent.items():
            if path.split('.')[-1].lower() in ['yml', 'yaml']:
                parent[r] = self.load_yaml(os.path.join(dir, path))
            else:
                parent[r] = os.path.join(dir, path)

    def env_overrides(self, key="cfg."):
        overrides = {}
        reduced = {decode(k, True): decode(v, True) for k, v in os.environ._data.items() if decode(k, True)}
        reduced = {k.lstrip(key): v for k, v in reduced.items() if k.startswith(key)}

        for k, v in reduced.items():
            entry = QConfig.make_dict(k.split("."), v)
            QConfig.merge_dict(overrides, entry)
        QConfig.merge_dict(self.data, overrides)

    @classmethod
    def from_yaml(cls, props_file, merge_env=False):
        return QConfig(cls.load_yaml(props_file), merge_env)

    @staticmethod
    def load_yaml(yaml_file):
        with open(yaml_file, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def make_dict(keylist, value):
        tree_dict = {}
        for i, key in enumerate(reversed(keylist)):
            val = value if i == 0 else tree_dict
            tree_dict = {
                key: val}
        return tree_dict

    @staticmethod
    def merge_dict(d1, d2, immutable=False):
        """
        # Combine dictionaries recursively
        # preserving the originals
        # assumes d1 and d2 dictionaries!!
        :param d1: original dictionary
        :param d2: update dictionary
        :return:
        """

        d1 = {} if d1 is None else d1
        d2 = {} if d2 is None else d2
        d1 = deepcopy(d1) if immutable else d1

        for k in d2:
            # if d1 and d2 have dict for k, then recurse
            # else assign the new value to d1[k]
            if (k in d1 and isinstance(d1[k], Mapping)
                    and isinstance(d2[k], Mapping)):
                QConfig.merge_dict(d1[k], d2[k])
            else:
                d1[k] = d2[k]
        return d1
