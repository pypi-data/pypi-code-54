""" Unit tests covering numpydoctor.ast_tools """

import ast
from numpydoctor import ast_tools


def test_transform_file_offset():
    source = '\n'.join([
        '0123456789',
        '012345',
        '',
        '0'
    ])

    def do_test(offset: int, expected_lineno: int, expected_col: int):
        lineno, col = ast_tools._transform_file_offset(source, offset)
        assert lineno == expected_lineno and col == expected_col, \
            f"actual {lineno}:{col} != expected {expected_lineno}:{expected_col}"

    yield do_test, 0, 1, 0
    yield do_test, 1, 1, 1
    yield do_test, 10, 1, 10
    yield do_test, 11, 2, 0
    yield do_test, 18, 3, 0
    yield do_test, 19, 4, 0
    yield do_test, 20, 4, 1


def test_ASTWalker():
    tree = ast.parse("""
def a():
    def b():
        def c(x, y, z, *args, **kwargs):
            pass
        return c
    def d():
        pass
    return b(), d

def e():
    return a()

""")

    def pre_factory(base):
        class PreTestWalker(base):
            def pre_visit(self, node):
                if hasattr(node, 'name'):
                    return node.name
        return PreTestWalker

    def post_factory(base):
        class PostTestWalker(base):
            def post_visit(self, node):
                if hasattr(node, 'name'):
                    return node.name
        return PostTestWalker

    def test_walker():
        pre_result = pre_factory(ast_tools.ASTWalker)().walk(tree)
        assert pre_result == 'a'
        post_result = post_factory(ast_tools.ASTWalker)().walk(tree)
        assert post_result == 'c'

    def test_iter_walker():
        pre_result = list(pre_factory(ast_tools.ASTIterWalker)().walk(tree))
        assert pre_result == ['a', 'b', 'c', 'd', 'e']
        post_result = list(post_factory(ast_tools.ASTIterWalker)().walk(tree))
        assert post_result == ['c', 'b', 'd', 'a', 'e']

    yield test_walker
    yield test_iter_walker


def test_DocumentableFinder():
    tree = ast.parse(_FIXTURE_MODULE_SOURCE)

    def do_test(lineno: int, col: int, expected_node_name: str):
        node = ast_tools.DocumentableFinder(lineno=lineno, col=col).walk(tree)
        if expected_node_name is not None:
            assert hasattr(node, 'name'), f"AST node {node} has no name"
            assert node.name == expected_node_name, f"AST node name '{node.name}' != expected '{expected_node_name}'"
        else:
            assert isinstance(node, ast.Module), f"Expected instance of ast.Module, got {node}"

    yield do_test, 1, 0, None
    yield do_test, 13, 17, None
    yield do_test, 16, 0, None
    yield do_test, 17, 0, 'MyClass'
    yield do_test, 25, 71, 'MyClass'
    yield do_test, 31, 3, 'MyClass'
    yield do_test, 31, 4, '__init__'
    yield do_test, 34, 0, 'MyClass'
    yield do_test, 36, 75, 'my_method'
    yield do_test, 62, 86, 'where_am_i'
    yield do_test, 63, 0, None
    yield do_test, 84, 6, 'my_function'
    yield do_test, 105, 0, None
    yield do_test, 106, 0, 'my_coroutine'
    yield do_test, 110, 33, 'my_coroutine'
    yield do_test, 116, 0, None


def test_query_ast():
    tree = ast.parse(_FIXTURE_MODULE_SOURCE)

    def names(results):
        for node in results:
            if hasattr(node, 'id'):
                yield node.id
            elif hasattr(node, 'name'):
                yield node.name
            elif hasattr(node, 'arg'):
                yield node.arg

    def do_test(predicate, expected_results):
        # results = list(names(ast_tools.query_ast(tree, predicate)))
        results = list((n.lineno, n.col_offset) for n in ast_tools.query_ast(tree, predicate))
        assert results == expected_results, f"Actual query results {results} != expected {expected_results}"

    def is_int(node: ast.AST) -> bool:
        return hasattr(node, 'annotation') and hasattr(node.annotation, 'id') and node.annotation.id == 'int'

    def is_str(node: ast.AST) -> bool:
        return hasattr(node, 'annotation') and hasattr(node.annotation, 'id') and node.annotation.id == 'str'

    yield do_test, is_int, [(35, 24), (35, 32), (69, 4), (79, 11), (81, 8), (106, 23)]

    yield do_test, is_str, [(25, 4), (61, 19), (71, 4), (87, 17), (98, 24), (102, 22)]


# source for a python module with many things in it, used by a number of tests
_FIXTURE_MODULE_SOURCE = """\""" Module-level docstring \"""
from __future__ import annotations

# just a comment. good documentation practices are important!

import asyncio
from dataclasses import dataclass
from typing import Iterable, List, Dict, Any, Union


_MY_CONSTANT = "a very important string"

# Meaning of life, the universe, everything
_MY_DOCUMENTED_CONSTANT = 42  # type: int


class MyClass:
    \""" Here's a docstring for my class!

    See Also
    --------
    ``MyDataclass`` : maybe this is related...
    \"""
    class_variable = 1969
    annotated_class_variable: str = f"{class_variable} in the sunshine"
    class_variable_without_assignment: Any

    data_structure = [8, 6, 7]  # type: List[int]
    data_structure[3] = 5

    def __init__(self, instance_variable, is_cool: bool = True):
        self.instance_variable = instance_variable
        self._is_cool = is_cool

    def my_method(self, a: int, b: int) -> int:
        \""" This method adds two numbers, in a very regular sort of way \"""
        return a + b

    @property
    def is_cool(self) -> bool:
        \""" Docstring for a very cool property \"""
        return self._is_cool

    @is_cool.setter
    def is_cool(self, value: bool):
        \""" Docstring for a property setter? \"""
        if value is False:
            raise ValueError("Sorry, I'm too cool for that")
        else:
            self._is_cool = value

    @classmethod
    def create_cool_instance(cls, instance_variable: Any) -> MyClass:
        \""" Here's a class method!

        It's probably a constructor.
        \"""
        return cls(instance_variable, is_cool=True)

    @staticmethod
    def where_am_i(name: str):
        print(f"You best start believin' in static methods, {name}... You're in one!")


@dataclass
class MyDataclass:
    required: bool
    very_strange_type: Iterable[Union[int, Dict, bytes]]
    first: int = 8
    second: float = 6.0
    third: str = '7'
    fourth: List[int] = [5]
    fifth: bytes = b'\x03'
    sixth: bool = False
    seventh: Dict[str, int] = {'value': 9}


def my_function(
        a, b: int,
        c=8.0,  # type: float
        d: int = 6, *args, **kwargs):  # type: int
    return sum([
        a, b, c, d, *args, *kwargs.values()
    ])


def my_generator(value: str) -> Iterable[str]:
    \""" Docstring for my generator.

    Iterate through ``value``, disemvoweled.
    \"""

    for c in value:
        if c.lower() not in 'aeiou':
            yield c


def my_better_generator(value: str) -> Iterable[str]:
    yield from (c for c in value if c.lower() not in 'aeiou')


def my_best_generator(value: str) -> Iterable[str]:
    return (c for c in value if c.lower() not in 'aeiou')


async def my_coroutine(wait_time: int):
    \""" This docstring is for an `asyncio` coroutine! \"""
    print("Help! I'm trapped in a")
    await asyncio.sleep(wait_time)
    print("`asyncio` coroutine!")


\""" This is just a string somebody left in here.
It should be removed!
\"""
"""
