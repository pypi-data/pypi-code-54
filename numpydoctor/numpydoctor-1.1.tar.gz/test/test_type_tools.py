""" Tests covering numpydoctor.type_tools """

import ast

from numpydoctor import type_tools


def test_describe_type_annotation():
    def do_test(source, expected):
        if source is None:
            node = None
        else:
            node = ast.parse(source).body[-1].value
        actual = type_tools.describe_type_annotation(node)
        assert actual == expected, f"{actual} != {expected}"

    yield do_test, None, None

    yield do_test, "str", "str"
    yield do_test, "MyType", "MyType"
    yield do_test, "None", "None"

    yield do_test, "Union[a, b, c]", "a or b or c"
    yield do_test, "Optional[type]", "type or None"
    yield do_test, "Tuple[a,b,c]", "a, b, c"
    yield do_test, "Tuple[int, int, int]", "int, int, int"
    yield do_test, "List[type]", "list of type"
    yield do_test, "Iterable[a, b, c]", "iterable of a, b, c"

    yield do_test, "Optional[Union[a, b]]", "a or b or None"
    yield do_test, "Union[Optional[a], b]", "a or None or b"
    yield do_test, "List[Union[a, b, c], d, e]", "list of a or b or c, d, e"

    yield do_test, "T.Optional[T.Union[a, b]]", "a or b or None"
    yield do_test, "T.Union[T.Optional[a], b]", "a or None or b"
    yield do_test, "T.List[T.Union[a, b, c], d, e]", "list of a or b or c, d, e"
