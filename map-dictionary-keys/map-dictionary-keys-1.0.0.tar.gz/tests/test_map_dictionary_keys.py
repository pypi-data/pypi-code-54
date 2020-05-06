from .test_data import input_dict, expected_output
from map_dictionary_keys import map_dictionary_keys


class TestMapDictionaryKeys:
    def test_valid_case(self):
        assert map_dictionary_keys(input_dict, lambda key: key.upper()) == expected_output
