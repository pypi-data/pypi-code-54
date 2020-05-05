
from file_util import File
import json


class JSONFile(File):

    def __init__(self, path, keep_formatting=None):
        super().__init__(path)

        self._keep_formatting = keep_formatting

    @property
    def keep_formatting(self):
        return self._keep_formatting

    @property
    def text(self):
        return self.pathlib.read_text()

    @property
    def pretty(self):
        return json.dumps(self.dict, indent=4)

    @property
    def dict(self) -> dict:
        return json.loads(self.text)

    @property
    def string(self):
        return self.text

    @property
    def is_formatted(self):
        return self.is_json_string_formatted(self.string)

    @property
    def is_not_formatted(self):
        return not self.is_formatted

    def write_dict(self, _dict):
        if self.keep_formatting and self.is_formatted:
            text = json.dumps(_dict, indent=4)
        else:
            text = json.dumps(_dict)
        self.write(text)

    def add_key_value_string(self, key_value: str):

        splits = key_value.split(':')
        key = splits[0]
        value = splits[1]

        _dict = self.dict
        _dict[key] = value
        self.write_dict(_dict)

        return True

    def create(self):
        if self.does_not_exists:
            self.write_dict({})
            return True
        else:
            return False

    def update_key_value_trim(self, key: str, value):

        if key.endswith(':'):
            key = key.replace(':', '')

        self.update_key_value(key, value)

    def update_key_value(self, key: str, value):

        _dict = self.dict
        _dict[key] = value
        self.write_dict(_dict)

        return True

    def remove(self, key):
        _dict = self.dict

        if key not in _dict:
            return False

        _dict.pop(key)
        self.write_dict(_dict)
        return True

    @staticmethod
    def is_json_string_formatted(json_string):

        json_object = json.loads(json_string)
        json_string_formatted_4 = json.dumps(json_object, indent=4)
        json_string_formatted_2 = json.dumps(json_object, indent=2)
        json_string_not_formatted = json.dumps(json_object)

        if json_string == json_string_formatted_4 or json_string == json_string_formatted_2:
            return True

        elif json_string == json_string_not_formatted:
            return False

        else:
            raise NotImplementedError

    def create_from_string(self, json_string):
        if self.exists:
            raise NotImplementedError
        self.write(json_string)
        return True

    def override_from_string(self, json_string):
        self.write(json_string)

