"""Operations for running numpydoctor as an application"""

import ast
import os
import pathlib
import typing as T
from . import docstring_tools, ast_tools

_PathLike = T.Union[str, bytes, os.PathLike, pathlib.Path]

CHECK_NOTHING_MISSING = 0
CHECK_MISSING_DATA = 1


def _iter_documentable_nodes(tree: ast.AST,
                             nested: bool = False,
                             magic: bool = False,
                             private: bool = False) -> T.Iterable[ast.AST]:
    def filter_name(node: ast.AST) -> bool:
        if 'name' in node._fields:
            if node.name is None:
                return False
            else:
                if not magic and node.name.startswith('__') and node.name.endswith('__'):
                    return False
                if not private and node.name.startswith('_'):
                    return False
        return True

    class DocumentableIterator(ast_tools.ASTIterWalker):
        def filter(self, node: ast.AST) -> bool:
            if not filter_name(node):
                return False

            if nested:
                return True
            else:
                return not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))

        def post_visit(self, node: ast.AST) -> T.Optional[ast.AST]:
            if isinstance(node, ast_tools._DOCUMENTABLE) and filter_name(node):
                return node

    yield from DocumentableIterator().walk(tree)


def _write_output(new_source: str, path: T.Optional[_PathLike] = None) -> None:
    if path is not None:
        with open(path, 'w') as f:
            f.write(new_source)
    else:
        print(new_source)


def check_missing(path: _PathLike,
                  offset: T.Optional[int] = None,
                  nested: bool = False,
                  private: bool = False,
                  magic: bool = False) -> int:
    """Check for missing docstrings in a python module.

    Parameters
    ----------
    path : _PathLike
        Filesystem path of a python module source file.
    offset : int or None, optional
        Character offset in the source file inside the definition to
        check. If ``None``, all documentable definitions in the module
        will be checked. Defaults to ``None``.
    nested : bool, optional
        If ``True``, check definitions nested inside function
        scopes. Defaults to ``False``.
    private : bool, optional
        If ``True``, check private names. Defaults to ``False``.
    magic : bool, optional
        If ``True``, check magic names. Defaults to ``False``.

    Returns
    -------
    code : {``CHECK_NOTHING_MISSING``, ``CHECK_MISSING_DATA``}
    """
    tree, source = ast_tools.parse_module(path)

    def check_node(node: ast.AST) -> int:
        if ast.get_docstring(node) is None:
            print(f"{ast_tools.fmt_documentable_node(node)} is missing docstring")
            return CHECK_MISSING_DATA
        else:
            return CHECK_NOTHING_MISSING

    if offset is not None:
        # check node at offset
        node = ast_tools.documentable_node_at_point(tree, source, offset=offset,
                                                    nested=nested, private=private, magic=magic)
        return check_node(node)
    else:
        # check all nodes
        codes = list(check_node(n) for n in _iter_documentable_nodes(
            tree, nested=nested, private=private, magic=magic
        ))
        if any(code != CHECK_NOTHING_MISSING for code in codes):
            return CHECK_MISSING_DATA
        else:
            return CHECK_NOTHING_MISSING


def fill_missing(path: _PathLike,
                 offset: T.Optional[int] = None,
                 nested: bool = False,
                 private: bool = False,
                 magic: bool = False,
                 inplace: bool = False,
                 line_wrap_col: T.Optional[int] = None,
                 tab_len: int = 4,
                 todo_level: int = docstring_tools.TODO_REQUIRED) -> None:
    """Fill in missing docstrings in a python module.

    Parameters
    ----------
    path : _PathLike
        Filesystem path of a python module source file.
    offset : int or None, optional
        Character offset in the source file inside the definition to
        fill. If ``None``, all missing documentable definitions in the
        module will be filled. Defaults to ``None``.
    nested : bool, optional
        If ``True``, fill definitions nested inside function
        scopes. Defaults to ``False``.
    private : bool, optional
        If ``True``, fill private names. Defaults to ``False``.
    magic : bool, optional
        If ``True``, fill magic names. Defaults to ``False``.
    inplace : bool, optional
        If ``True``, modify the file in-place. Defaults to ``False``.
    line_wrap_col : int or None, optional
        Automatically wrap docstrings at this column limit. If
        ``None``, do not try to wrap docstrings. Defaults to ``None``.
    tab_len : int, optional
        Number of spaces used for one level of indentation. Defaults
        to 4.
    todo_level : int, optional
        Level of pedantry when inserting TODO messages. Defaults to 0,
        which will insert TODO messages only for missing required
        data.
    """
    tree, source = ast_tools.parse_module(path)

    def fill_missing_docstrings(nodes: T.Iterable[ast.AST]) -> str:
        def iter_missing_node_docstrings() -> T.Iterable[T.Tuple[ast.AST, str]]:
            for node in nodes:
                if ast.get_docstring(node) is None:
                    docstring = docstring_tools.Docstring.from_ast(node)
                    yield node, docstring.build(todo_level=todo_level)

        return ast_tools.insert_docstrings(
            source, iter_missing_node_docstrings(),
            line_wrap_col=line_wrap_col,
            tab_len=tab_len
        )

    if offset is not None:
        # fill missing docstring for node at offset
        node = ast_tools.documentable_node_at_point(tree, source, offset=offset,
                                                    nested=nested, private=private, magic=magic)
        new_source = fill_missing_docstrings([node])
    else:
        # fill all missing docstrings in module
        new_source = fill_missing_docstrings(
            _iter_documentable_nodes(tree, nested=nested, private=private, magic=magic)
        )

    _write_output(new_source, path if inplace else None)


def check(path: _PathLike,
          offset: T.Optional[int] = None,
          nested: bool = False,
          private: bool = False,
          magic: bool = False) -> int:
    """Check for missing data in docstrings in a python module.

    Parameters
    ----------
    path : _PathLike
        Filesystem path of a python module source file.
    offset : int or None, optional
        Character offset in the source file inside the definition to
        check. If ``None``, all documentable definitions in the module
        will be checked. Defaults to ``None``.
    nested : bool, optional
        If ``True``, check definitions nested inside function
        scopes. Defaults to ``False``.
    private : bool, optional
        If ``True``, check private names. Defaults to ``False``.
    magic : bool, optional
        If ``True``, check magic names. Defaults to ``False``.

    Returns
    -------
    code : {``CHECK_NOTHING_MISSING``, ``CHECK_MISSING_DATA``}
    """
    tree, source = ast_tools.parse_module(path)

    def iter_missing_sections(docstring, existing):
        for fieldname in docstring.__dataclass_fields__:
            inferred_section = getattr(docstring, fieldname)
            parsed_section = getattr(existing, fieldname)
            if inferred_section is not None:
                if isinstance(inferred_section, docstring_tools._KVContainer):
                    if parsed_section is None:
                        diff = inferred_section.elements
                    else:
                        diff = inferred_section.diff(parsed_section)

                    yield f"{fieldname} ({', '.join(e._primary_key() for e in diff)})"
                else:
                    if parsed_section is None:
                        yield fieldname

    def check_node(node: ast.AST) -> int:
        old_docstring = ast.get_docstring(node)
        if old_docstring is None:
            print(f"{ast_tools.fmt_documentable_node(node)} is missing docstring")
            return CHECK_MISSING_DATA
        else:
            docstring = docstring_tools.Docstring.from_ast(node)
            existing = type(docstring).from_docstring(old_docstring)
            missing = list(iter_missing_sections(docstring, existing))
            if len(missing) > 0:
                print(f"{ast_tools.fmt_documentable_node(node)} docstring is missing {', '.join(missing)}")
                return CHECK_MISSING_DATA
            else:
                return CHECK_NOTHING_MISSING

    if offset is not None:
        # check node at offset
        node = ast_tools.documentable_node_at_point(tree, source, offset=offset,
                                                    nested=nested, private=private, magic=magic)
        return check_node(node)
    else:
        # check all nodes
        codes = list(check_node(n) for n in _iter_documentable_nodes(
            tree, nested=nested, private=private, magic=magic
        ))
        if any(code != CHECK_NOTHING_MISSING for code in codes):
            return CHECK_MISSING_DATA
        else:
            return CHECK_NOTHING_MISSING


def fix(path: _PathLike,
        offset: T.Optional[int] = None,
        nested: bool = False,
        private: bool = False,
        magic: bool = False,
        inplace: bool = False,
        line_wrap_col: T.Optional[int] = None,
        tab_len: int = 4,
        todo_level: int = docstring_tools.TODO_REQUIRED) -> None:
    """Fix docstrings in a python module.

    Parameters
    ----------
    path : _PathLike
        Filesystem path of a python module source file.
    offset : int or None, optional
        Character offset in the source file inside the definition to
        fix. If ``None``, all missing documentable definitions in the
        module will be fixed. Defaults to ``None``.
    nested : bool, optional
        If ``True``, fix definitions nested inside function
        scopes. Defaults to ``False``.
    private : bool, optional
        If ``True``, fix private names. Defaults to ``False``.
    magic : bool, optional
        If ``True``, fix magic names. Defaults to ``False``.
    inplace : bool, optional
        If ``True``, modify the file in-place. Defaults to ``False``.
    line_wrap_col : int or None, optional
        Automatically wrap docstrings at this column limit. If
        ``None``, do not try to wrap docstrings. Defaults to ``None``.
    tab_len : int, optional
        Number of spaces used for one level of indentation. Defaults
        to 4.
    todo_level : int, optional
        Level of pedantry when inserting TODO messages. Defaults to 0,
        which will insert TODO messages only for missing required
        data.
    """
    tree, source = ast_tools.parse_module(path)

    def fix_docstrings(nodes: T.Iterable[ast.AST]) -> str:
        def iter_fixed_docstrings() -> T.Iterable[T.Tuple[ast.AST, str]]:
            for node in nodes:
                docstring = docstring_tools.Docstring.from_ast(node)
                old_docstring = ast.get_docstring(node)
                if old_docstring is not None:
                    # if there is already a docstring for this node,
                    # merge the inferred new docstring onto it
                    existing = type(docstring).from_docstring(old_docstring)
                    docstring = existing.join(docstring)
                yield node, docstring.build(todo_level=todo_level)
        return ast_tools.insert_docstrings(
            source, iter_fixed_docstrings(),
            line_wrap_col=line_wrap_col,
            tab_len=tab_len
        )

    if offset is not None:
        # fill missing docstring for node at offset
        node = ast_tools.documentable_node_at_point(tree, source, offset=offset,
                                                    nested=nested, private=private, magic=magic)
        new_source = fix_docstrings([node])
    else:
        # fill all missing docstrings in module
        new_source = fix_docstrings(_iter_documentable_nodes(tree, nested=nested, private=private, magic=magic))

    _write_output(new_source, path if inplace else None)
