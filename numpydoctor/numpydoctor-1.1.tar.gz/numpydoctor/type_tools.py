"""Tools for describing types and type annotations"""

import typing as T
import ast
import astor


def _not_none(it: T.Iterable) -> T.Iterable:
    return (e for e in it if e is not None)


def describe_type_annotation(annotation: T.Optional[ast.AST]) -> T.Optional[str]:
    if isinstance(annotation, ast.Subscript):
        if isinstance(annotation.slice, ast.Index):
            index = annotation.slice.value
            if 'elts' in index._fields:
                values = (describe_type_annotation(e) for e in index.elts)
            else:
                values = [describe_type_annotation(index)]

            name = None
            if isinstance(annotation.value, ast.Name):
                name = annotation.value.id
            elif isinstance(annotation.value, ast.Attribute) and annotation.value.attr in dir(T):
                # this is a nasty hack.
                # TODO use off-the-shelf type inference solution
                name = annotation.value.attr

            if name is not None:
                if name == 'Union':
                    return ' or '.join(_not_none(values))
                elif name == 'Optional':
                    return ', '.join(_not_none(values)) + ' or None'
                elif name == 'Tuple':
                    return ', '.join(_not_none(values))
                else:
                    return f"{name.lower()} of {', '.join(values)}"

    if annotation is not None:
        return astor.to_source(annotation).strip()
