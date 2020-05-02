"""Tests covering `numpydoctor.application`"""

from pathlib import Path
from io import StringIO
from unittest.mock import patch
import tempfile
import shutil
import itertools
import typing as T

from numpydoctor import application

_FIXTURE_PATH = Path(__file__).parent / '_fixtures'

_workdir: T.Optional[tempfile.TemporaryDirectory] = None
_workdir_path: T.Optional[Path] = None


def setup():
    global _workdir, _workdir_path
    _workdir = tempfile.TemporaryDirectory()
    _workdir.__enter__()
    _workdir_path = Path(_workdir.name)
    shutil.copytree(_FIXTURE_PATH, _workdir_path, dirs_exist_ok=True)


def teardown():
    _workdir.__exit__(None, None, None)


def _assert_lines_equal(actual: str, expected: str) -> None:
    for i, (line_a, line_e) in enumerate(itertools.zip_longest(
            actual.strip().split(sep='\n'),
            expected.strip().split(sep='\n'))):
        assert line_a == line_e, f"Line {i}: '{line_a}' != '{line_e}'"


def test_check_missing():
    def do_test(kwargs: dict, expected_stdout: str, expected_ret: int):
        with patch('sys.stdout', new=StringIO()) as mock_out:
            ret = application.check_missing(_workdir_path / 'pymodule.py', **kwargs)
            stdout = mock_out.getvalue()
        _assert_lines_equal(stdout, expected_stdout)
        assert ret == expected_ret, f"return value {ret} != expected {expected_ret}"

    yield do_test, {}, "", 0

    yield do_test, dict(private=True), """
FunctionDef _where_am_i (L65:4) is missing docstring
FunctionDef _method_without_docstring (L68:4) is missing docstring
ClassDef _MyDataclass (L74:0) is missing docstring
FunctionDef _my_function (L93:0) is missing docstring
FunctionDef _my_better_generator (L113:0) is missing docstring
FunctionDef _my_best_generator (L117:0) is missing docstring
""", 1

    yield do_test, dict(private=True, magic=True), """
FunctionDef __init__ (L35:4) is missing docstring
FunctionDef _where_am_i (L65:4) is missing docstring
FunctionDef _method_without_docstring (L68:4) is missing docstring
FunctionDef __str__ (L85:4) is missing docstring
ClassDef _MyDataclass (L74:0) is missing docstring
FunctionDef _my_function (L93:0) is missing docstring
FunctionDef _my_better_generator (L113:0) is missing docstring
FunctionDef _my_best_generator (L117:0) is missing docstring
""", 1

    yield do_test, dict(nested=True), "", 0

    yield do_test, dict(nested=True, private=True), """
FunctionDef _where_am_i (L65:4) is missing docstring
FunctionDef nested (L69:8) is missing docstring
FunctionDef _method_without_docstring (L68:4) is missing docstring
ClassDef _MyDataclass (L74:0) is missing docstring
FunctionDef _my_function (L93:0) is missing docstring
FunctionDef _my_better_generator (L113:0) is missing docstring
FunctionDef _my_best_generator (L117:0) is missing docstring
""", 1

    yield do_test, dict(offset=1928), "", 0

    yield do_test, dict(offset=1928, private=True), """
FunctionDef _method_without_docstring (L68:4) is missing docstring
""", 1

    yield do_test, dict(offset=1928, nested=True, private=True), """
FunctionDef nested (L69:8) is missing docstring
""", 1


def test_check():
    def do_test(kwargs: dict, expected_stdout: str, expected_ret: int):
        with patch('sys.stdout', new=StringIO()) as mock_out:
            ret = application.check(_workdir_path / 'pymodule.py', **kwargs)
            stdout = mock_out.getvalue()
        _assert_lines_equal(stdout, expected_stdout)
        assert ret == expected_ret, f"return value {ret} != expected {expected_ret}"

    yield do_test, {}, """
FunctionDef my_method (L39:4) docstring is missing parameters (a, b), returns (int)
FunctionDef create_cool_instance (L57:4) docstring is missing parameters (instance_variable), returns (MyClass)
ClassDef MyClass (L21:0) docstring is missing parameters (instance_variable, is_cool), attributes (class_variable, annotated_class_variable, class_variable_without_assignment, data_structure, is_cool)
FunctionDef my_generator (L102:0) docstring is missing parameters (value), yields (iterable of str)
AsyncFunctionDef my_coroutine (L121:0) docstring is missing parameters (wait_time)
""".lstrip(), 1


def test_fill_missing():
    def do_test(kwargs: dict, expected_module_path: Path):
        with open(expected_module_path, 'r') as f:
            expected_stdout = f.read()
        with patch('sys.stdout', new=StringIO()) as mock_out:
            application.fill_missing(_workdir_path / 'pymodule.py', **kwargs)
            stdout = mock_out.getvalue()
        _assert_lines_equal(stdout, expected_stdout)

    yield do_test, dict(private=True, magic=True), _workdir_path / 'pymodule_fill_missing.py'


def test_fix():
    def do_test(kwargs: dict, expected_module_path: Path):
        with open(expected_module_path, 'r') as f:
            expected_stdout = f.read()
        with patch('sys.stdout', new=StringIO()) as mock_out:
            application.fix(_workdir_path / 'pymodule.py', **kwargs)
            stdout = mock_out.getvalue()
        _assert_lines_equal(stdout, expected_stdout)

    yield do_test, dict(private=True, magic=True), _workdir_path / 'pymodule_fix.py'
