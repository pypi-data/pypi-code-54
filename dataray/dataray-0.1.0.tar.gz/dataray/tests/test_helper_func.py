import pytest

from dataray.helper.helper_func import structure_parser
from dataray.helper.helper_func import structure_printer

@pytest.fixture()
def flatten_dict():
    return {"a": 1, "b": 1, "c": 1}


@pytest.fixture()
def nested_dict():
    return {"a": {"b": {"f": 1}, "c": 1, "d": 1}, "e": 1}


@pytest.fixture()
def parsed_structure():
    return {"a": ["d", "f"], "b": [], "c": [], "d": [], "f": []}


def test_structure_parser_flatten_dict(flatten_dict):
    parsed = structure_parser(flatten_dict)
    expected = {"a": [], "b": [], "c": []}
    assert parsed == expected


def test_structure_parser_nested_dict(nested_dict):
    parsed = structure_parser(nested_dict)
    expected = {"a": ["b", "c", "d"], "b": ["f"], "c": [], "d": [], "e": [], "f": []}
    assert parsed == expected


def test_structure_printer(parsed_structure, capsys):
    structure_printer(parsed_structure)
    captured = capsys.readouterr()
    assert captured.out == " a\n     d\n     f\n b\n c\n"
