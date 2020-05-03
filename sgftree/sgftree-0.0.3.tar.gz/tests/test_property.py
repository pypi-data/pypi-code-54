import pytest

from sgftree import Property


@pytest.mark.parametrize(
    "label, data, expected",
    [
        ("B", ["aa"], "B[aa]"),
        ("W", ["aa", "aa"], "W[aa]"),
        ("TR", ["aa", "ab"], "TR[aa][ab]"),
        ("TR", ["aa", "ac", "ab"], "TR[aa][ab][ac]"),
    ],
)
def test_property_create(label, data, expected):
    new_prop = Property(label, data)
    assert str(new_prop) == expected
