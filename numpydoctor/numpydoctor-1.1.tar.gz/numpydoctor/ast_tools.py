"""Tools for finding docstrings in an AST"""

import ast
import os
import sys
import pathlib
import textwrap
from dataclasses import dataclass
import typing as T


_DOCUMENTABLE = (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
_PathLike = T.Union[str, bytes, os.PathLike, pathlib.Path]


class ASTWalker:
    """Abstract base class for an AST visitor.

    Derived classes can be implemented by overriding `pre_visit` and
    `post_visit`
    """

    def pre_visit(self, node: ast.AST) -> T.Any:
        """Visitor method called before walking a node of the AST.

        Parameters
        ----------
        node : ast.AST
            The AST node being visited. This method is called BEFORE
            visiting the children of this node.

        Returns
        -------
        result : Optional[Any]
            If non-None, the walk will immediately return this value.
        """
        # Implemented by derived class
        pass

    def post_visit(self, node: ast.AST) -> T.Any:
        """Visitor method called after walking a node of the AST.

        Parameters
        ----------
        node : ast.AST
            The AST node being visited. This method is called AFTER
            visiting the children of this node.

        Returns
        -------
        result : Optional[Any]
            If not None, the walk will immediately return this value.
        """
        # Implemented by derived class
        pass

    def filter(self, node: ast.AST) -> bool:
        """Visitor helper method controlling the path of the walk.

        This method is called immediately before walking the children
        of ``node``. If this method returns ``True``, the walk will
        descend to the children; otherwise, it will continue to the
        next sibling.

        Parameters
        ----------
        node : ast.AST
            The AST node being visited. This method is called BEFORE
            visiting the children of this node.

        Returns
        -------
        bool
            If ``True``, visit the children of ``node``. Otherwise
            continue to the next sibling.
        """
        # Implemented by derived class
        return True

    def walk(self, node: ast.AST) -> T.Any:
        """Walk an AST depth-first.

        If any visitor method of this object returns a non-None value
        during the walk, at any depth, the walk will stop and this
        method will return that value.

        Parameters
        ----------
        node : ast.AST
            Root node of the AST to walk.

        Returns
        -------
        Any
            The first non-None value returned by a visitor method.
        """
        return self.pre_visit(node) \
            or next((v for v in self._walk(node) if v is not None), None) \
            or self.post_visit(node)

    def _walk(self, node: ast.AST) -> T.Any:
        if self.filter(node):
            for fieldname in node._fields:
                field = getattr(node, fieldname)
                if isinstance(field, ast.AST):
                    yield self.walk(field)
                elif isinstance(field, T.Iterable) and not isinstance(field, (str, bytes)):
                    for n in field:
                        if isinstance(n, ast.AST):
                            yield self.walk(n)


class ASTIterWalker(ASTWalker):
    """Alternate abstract base class for an AST visitor."""
    def walk(self, node: ast.AST) -> T.Iterable[T.Any]:
        """Walk an AST depth-first, iterating over results.

        Parameters
        ----------
        node : ast.AST
            Root node of the AST to walk.

        Yields
        ------
        Any
            Iterate over all non-None values returned by visitor methods.
        """
        def iter_walk():
            yield self.pre_visit(node)
            for i in self._walk(node):
                yield from i

            yield self.post_visit(node)
        yield from (v for v in iter_walk() if v is not None)


@dataclass
class DocumentableFinder(ASTWalker):
    """AST visitor that finds an enclosing scope for a point in the source file.

    Parameters
    ----------
    lineno : int
        Line number of point to find, 1-indexed.
    col : int, optional
        Column offset of point to find, 0-indexed. If omitted, only the
        line number will be considered.
    """
    lineno: int
    col: int = None

    def post_visit(self, node: ast.AST) -> T.Union[_DOCUMENTABLE]:
        if isinstance(node, _DOCUMENTABLE):
            if 'lineno' in node._attributes and 'end_lineno' in node._attributes:
                if node.lineno <= self.lineno <= node.end_lineno:
                    if self.col is not None \
                       and 'col_offset' in node._attributes and 'end_col_offset' in node._attributes:

                        if not ((self.lineno == node.lineno and self.col < node.col_offset)
                                or (self.lineno == node.end_lineno and self.col > node.end_col_offset)):
                            # in line and col range
                            return node
                    else:
                        # in line range, but either no col attributes or self.col not given
                        return node
            else:
                # in valid types, but no line attributes (e.g. if node is a module)
                return node


def query_ast(node: ast.AST, predicate: T.Callable[[ast.AST], bool]) -> T.Iterable[ast.AST]:
    """Get all descendents (depth-first order) of an AST node that match a predicate.

    Parameters
    ----------
    node : ast.AST
        AST tree root to search
    predicate : func(ast.AST) -> bool
        A function to call on each visited node (pre-visit) which
        returns ``True`` for matched nodes.

    Yields
    -------
    ast.AST
        Iterate over all AST nodes matching ``predicate``
    """
    class Finder(ASTIterWalker):
        def pre_visit(self, node: ast.AST) -> ast.AST:
            if predicate(node):
                return node

    yield from Finder().walk(node)


def search_ast(node: ast.AST, predicate: T.Callable[[ast.AST], bool]) -> ast.AST:
    """Get the first descendent (depth-first order) of an AST node that matches a predicate.

    Parameters
    ----------
    node : ``ast.AST``
        AST tree root to search
    predicate : func(``ast.AST``) -> bool
        A function to call on each visited node (pre-visit) which
        returns ``True`` for the queried node.

    Returns
    -------
    ast.AST
        The first node in the AST for which ``predicate(node) == True``,
        or ``None`` if no matches are found.
    """
    return next(query_ast(node, predicate), None)


def parse_module(path: _PathLike) -> T.Tuple[ast.Module, str]:
    """Parse a python module and return it as an AST.

    Parameters
    ----------
    path : path-like object
        Path to a python module source file.

    Returns
    -------
    tree : ast.Module
        The root AST node of the parsed module.
    source : str
        The source code from which ``tree`` was parsed.
    """
    if path is None:
        source = sys.stdin.read()
    else:
        with open(path, 'r') as f:
            source = f.read()
    tree = ast.parse(source, mode='exec')
    return tree, source


def _transform_file_offset(source: str, offset: int) -> T.Tuple[int, int]:
    """ Given the bytestring source of a file, transform a byte offset into line and column offsets. """
    pre_source = source[:offset]
    lineno = pre_source.count('\n') + 1
    col = offset - pre_source.rfind('\n') - 1
    return lineno, col


def _filter_name(node: ast.AST, private: bool = False, magic: bool = False) -> bool:
    if 'name' in node._fields and node.name is not None:
        if not magic and node.name.startswith('__') and node.name.endswith('__'):
            return False
        if not private and node.name.startswith('_'):
            return False
    return True


def documentable_node_at_point(tree: ast.AST, source: str,
                               offset: int = None,
                               lineno: int = None, col: int = None,
                               nested: bool = True,
                               private: bool = True,
                               magic: bool = True) -> T.Union[_DOCUMENTABLE]:
    """Find the closest documentable node to a point in source code.

    Only certain python elements can be documented with a docstring;
    specifically modules, class definitions, and function definitions
    (including methods, generators, async functions). Given a point in
    the source code, this will find the closest valid enclosing scope
    at that point and return the AST node defining that scope.

    Parameters
    ----------
    tree : ast.AST
        The root AST node of the of the python module.
    source : str
        Python source code.
    offset : int, optional
        Source code character offset of the point to find the
        enclosing scope for. May be specified instead of ``lineno``
        and ``col``.
    lineno : int, optional
        Source code line number of the definition to find the
        enclosing scope for. Along with ``col``, may be specified
        instead of ``offset``.
    col : int, optional
        Source code column offset of the definition to find the
        enclosing scope for. Along with ``lineno``, may be specified
        instead of ``offset``.
    nested : bool, optional
        If ``True``, include nested functions scopes (functions nested
        in other functions) in search. Otherwise, if the closest scope
        is a nested function scope, the closest non-nested scope
        will be returned.
    private : bool, optional
       If ``True``, include private names in search.
    magic : bool, optional
       If ``True``, include magic names in search.

    Returns
    -------
    node : documentable ast.AST
        The AST node for the enclosing scope at the given point.
    """
    if offset is not None:
        lineno, col = _transform_file_offset(source, offset)
        return documentable_node_at_point(tree, source, lineno=lineno, col=col,
                                          nested=nested, private=private, magic=magic)
    else:
        class FilteredFinder(DocumentableFinder):
            def filter(self, node: ast.AST) -> bool:
                if not _filter_name(node, private, magic):
                    return False

                if not nested:
                    return not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                else:
                    return True

            def post_visit(self, node: ast.AST) -> T.Union[_DOCUMENTABLE]:
                if _filter_name(node, private, magic):
                    return super().post_visit(node)

        return FilteredFinder(lineno=lineno, col=col).walk(tree)


def _docnode_for_node(node: T.Union[_DOCUMENTABLE]) -> ast.Expr:
    """ Find the docstring node for a documentable AST node. """
    if 'body' in node._fields and len(node.body) > 0:
        child = node.body[0]
        if isinstance(child, ast.Expr) and 'value' in child._fields and isinstance(child.value, ast.Constant):
            return child


def fmt_documentable_node(node: T.Union[_DOCUMENTABLE]) -> str:
    """Format a documentable node for human-readable output.

    Parameters
    ----------
    node : documentable ast.AST
        AST node to format

    Returns
    -------
    str
       A human-readable string describing the node and its location,
       if available.
    """
    if isinstance(node, ast.Module):
        return "module"
    elif 'lineno' in node._attributes and 'col_offset' in node._attributes:
        helpstr = f"L{node.lineno}:{node.col_offset}"
        if 'name' in node._fields:
            return f"{type(node).__name__} {node.name} ({helpstr})"
        else:
            return f"node {str(node)} ({helpstr})"
    else:
        return f"node {str(node)}"


def _get_docstring_span(node: T.Union[_DOCUMENTABLE], tab_len: int = 4) -> T.Tuple[int, int, int]:
    existing_docnode = _docnode_for_node(node)
    if existing_docnode is not None:
        return (existing_docnode.lineno - 1, existing_docnode.end_lineno, existing_docnode.col_offset)
    else:
        if len(node.body) > 0:
            return (node.body[0].lineno - 1, node.body[0].lineno - 1, node.body[0].col_offset)
        elif 'end_lineno' in node._attributes and 'col_offset' in node._attributes:
            return (node.end_lineno, node.end_lineno, node.col_offset + tab_len)
        else:
            return (0, 0, 0)


def insert_docstrings(source: str, node_docstrings: T.Iterable[T.Tuple[T.Union[_DOCUMENTABLE], str]],
                      line_wrap_col: int = None, tab_len: int = 4) -> str:
    """Insert docstrings for AST nodes into python source code.

    Parameters
    ----------
    source : str
        Python module source code.
    node_docstrings : iterable of (documentable ast.AST, str)
        Iterable of pairs of documentable AST nodes and the docstrings
        to insert for them.
    line_wrap_col : int, optional
        Automatically wrap docstrings at this column limit. If
        ``None``, do not try to wrap docstrings.
    tab_len : int, optional
        Number of spaces used for one level of indentation. The
        default is 4.

    Yields
    ------
    new_source : str
        The changed source code after inserting docstrings.
    """
    source_lines = source.split(sep='\n')

    sorted_node_docstrings = sorted(node_docstrings, key=lambda t: t[0].lineno if 'lineno' in t[0]._attributes else -1)

    def iter_lines():
        index = None
        for node, docstring in sorted_node_docstrings:
            ds_start, ds_end, indent = _get_docstring_span(node, tab_len)
            tab = ' ' * indent

            yield from source_lines[index:ds_start]

            head, *tail = docstring.split(sep='\n')
            if len(tail) == 0 and (line_wrap_col is None or len(head) <= line_wrap_col - len(tab) - 6):
                # single line docstring
                yield f'{tab}"""{head}"""'
            else:
                # multiline docstring
                ds_lines = [f'"""{head}'] + tail + ['"""']
                for line in ds_lines:
                    if line_wrap_col is None:
                        yield tab + line if len(line) > 0 else ''
                    else:
                        wrapped_lines = textwrap.wrap(line, width=line_wrap_col - len(tab)) or ['']

                        for wrapped_line in wrapped_lines:
                            yield tab + wrapped_line if len(wrapped_line) > 0 else ''

            index = ds_end
        yield from source_lines[index:]

    return '\n'.join(iter_lines())
