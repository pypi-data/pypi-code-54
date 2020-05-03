import pytest

from sgftree import Property, Node


prop_b = Property("B", ["aa"])
prop_w = Property("W", ["ab"])
prop_c = Property("C", ["comment"])
prop_many1 = Property("TR", ["v1", "v2"])
prop_many2 = Property("TR", ["v3", "v4"])


@pytest.mark.parametrize(
    "props, expected", [([], ";"), ([prop_b], ";B[aa]"), ([prop_b, prop_many1], ";B[aa]TR[v1][v2]"), ]
)
def test_node_create(props, expected):
    node = Node(props)

    assert str(node) == expected
