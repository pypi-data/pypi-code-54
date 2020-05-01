""" Tools for manipulation of docstrings """
from __future__ import annotations

import ast
from dataclasses import dataclass
import typing as T
import docstring_parser as dsparser

from . import ast_tools, type_tools


# TODO this should maybe be parameterizable
_TAB = '    '

TODO_REQUIRED = 0
TODO_TYPES = 1
TODO_DESCRIPTIONS = 2
TODO_RETURN_NAMES = 3
TODO_EXTENDED_SUMMARY = 4
TODO_ALL = 5

_FunctionLike = T.Union[ast.FunctionDef, ast.AsyncFunctionDef]


def _is_generator(node: _FunctionLike) -> bool:
    # this is really just a "good guess" and cannot reliably determine if a function is a generator
    return ast_tools.search_ast(node, lambda n: isinstance(n, ast.Yield)) is not None


def _is_classmethod(node: _FunctionLike) -> bool:
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == 'classmethod':
            return True
    return False


def _is_property(node: _FunctionLike, getter: bool = True, setter: bool = True) -> bool:
    # again, just a good guess
    for decorator in node.decorator_list:
        if getter and isinstance(decorator, ast.Name) and decorator.id == 'property':
            return True
        if setter and isinstance(decorator, ast.Attribute) and decorator.attr == 'setter':
            return True
    return False


def _header(cls: T.Type, header: T.Optional[str] = None) -> T.Type:
    class _Wrapped(cls):
        def lines(self, todo_level: int = 0) -> T.Iterable[str]:
            yield self._header
            yield '-' * len(self._header)
            yield from super().lines(todo_level)

    if header is not None:
        _Wrapped._header = header

    return _Wrapped


def _o_dataclass(cls: T.Type) -> T.Type:
    """ Ordered dataclass decorator.

    Classes annotated with this decorator are dataclasses, with an
    extra ``iter_fields`` method which returns an iterator through
    dataclass fields in the order in which they were defined.
    """
    dc = dataclass(cls)

    def iter_fields(self):
        return (getattr(self, f) for f in dc.__annotations__ if f in dc.__dataclass_fields__)

    dc.iter_fields = iter_fields
    return dc


def _default_for(fieldname: str, level: int) -> T.Callable[[], T.Optional[str]]:
    def method(self, todo_level: int = 0) -> T.Optional[str]:
        value = getattr(self, fieldname)
        if value is not None:
            return str(value)
        elif todo_level >= level:
            return f"<TODO {fieldname}>"

    return method


def _with_todo(cls: T.Type) -> T.Type:
    for name in dir(cls):
        if name.startswith('_todo_'):
            fieldname = name[6:]
            threshold = getattr(cls, name)
            setattr(cls, f"get_{fieldname}", _default_for(fieldname, threshold))

    return cls


class _AbstractKV:
    def _primary_key(self) -> str: pass
    def _key(self, todo_level: int = 0) -> str: pass
    def _value(self, todo_level: int = 0) -> str: pass

    def lines(self, todo_level: int = 0) -> T.Iterable[str]:
        yield self._key(todo_level)

        value = self._value(todo_level)
        if value:
            for line in value.split(sep='\n'):
                yield _TAB + line


@_with_todo
@dataclass
class _Simple:
    value: str

    def lines(self, todo_level: int = 0) -> T.Iterable[str]:
        for line in self.value.split(sep='\n'):
            yield line


class _FromParser:
    _meta_key: T.Optional[str] = None

    @classmethod
    def _from_parser(cls, parser: Docstring) -> T.Optional[_FromParser]:
        value = '\n'.join(meta.description for meta in parser.meta if cls._meta_key in meta.args)
        if len(value) > 0:
            return cls(
                value=value
            )


class _Joinable:
    def join(self, other: _Joinable) -> _Joinable:
        """Merge this instance's data with another's."""
        if not (hasattr(self, '__dataclass_fields__') and hasattr(other, '__dataclass_fields__')):
            raise AttributeError("`join` only valid for dataclasses")

        kwargs = {}
        for fieldname in self.__dataclass_fields__:
            ours = getattr(self, fieldname)
            if fieldname in other.__dataclass_fields__:
                theirs = getattr(other, fieldname)
                if ours is None:
                    kwargs[fieldname] = theirs
                elif isinstance(ours, _Joinable) and isinstance(theirs, _Joinable):
                    kwargs[fieldname] = ours.join(theirs)
                else:
                    kwargs[fieldname] = ours
            else:
                kwargs[fieldname] = ours

        return self.__class__(**kwargs)


@dataclass
class _KVContainer:
    elements: T.Iterable[_AbstractKV] = tuple()

    def lines(self, todo_level: int = 0) -> T.Iterable[str]:
        for e in self.elements:
            yield from e.lines(todo_level)

    def diff(self, other: _KVContainer) -> T.Iterable(_AbstractKV):
        """ Iterate over elements in this that are not in ``other`` """
        theirs = {e._primary_key() for e in other.elements}
        return (e for e in self.elements if e._primary_key() not in theirs)


@_with_todo
@dataclass
class DeprecationWarning_(_FromParser, _Joinable):
    _meta_key = 'deprecation'
    version: T.Optional[str] = None
    message: T.Optional[str] = None

    _todo_version = TODO_REQUIRED
    _todo_message = TODO_REQUIRED

    def lines(self, todo_level: int = 0) -> T.Iterable[str]:
        yield f".. deprecated:: {self.get_version(todo_level)}"
        for line in self.get_message(todo_level).split(sep='\n'):
            yield _TAB + line

    @classmethod
    def _from_parser(cls, parser: Docstring) -> T.Optional[DeprecationWarning_]:
        if parser.deprecation is not None:
            return cls(
                version=parser.deprecation.version,
                message=parser.deprecation.description
            )


@_with_todo
@dataclass
class Parameter(_AbstractKV, _Joinable):
    # required: name, description
    name: T.Optional[str] = None
    description: T.Optional[str] = None
    typ: T.Optional[str] = None
    optional: T.Optional[bool] = None

    _todo_name = TODO_REQUIRED
    _todo_description = TODO_DESCRIPTIONS
    _todo_typ = TODO_TYPES

    def _primary_key(self) -> str:
        return self.name

    def _key(self, todo_level: int = 0) -> str:
        name = self.get_name(todo_level)
        typ = self.get_typ(todo_level)
        if typ is not None:
            if self.optional:
                return f"{name} : {typ}, optional"
            else:
                return f"{name} : {typ}"
        else:
            if self.optional:
                return f"{name} : optional"
            else:
                return name

    def _value(self, todo_level: int = 0) -> str:
        return self.get_description(todo_level)

    @classmethod
    def _from_parser_meta(cls, meta: dsparser.DocstringMeta) -> Parameter:
        return cls(
            name=meta.arg_name,
            description=meta.description,
            typ=meta.type_name,
            optional=meta.is_optional,
        )

    @classmethod
    def from_ast(cls, node: ast.Node, default: T.Optional[ast.Node] = None) -> Parameter:
        if node.annotation is not None:
            typ = type_tools.describe_type_annotation(node.annotation)
        elif node.type_comment is not None:
            typ = node.type_comment
        else:
            typ = None

        return cls(
            name=node.arg,
            description=None,
            typ=typ,
            optional=default is not None
        )


@_header
@dataclass
class Parameters(_FromParser, _Joinable, _KVContainer):
    _header = "Parameters"
    _meta_key = 'param'

    def join(self, other: _Joinable) -> _Joinable:
        name_map = {p.name: p for p in self.elements}

        def merge_params():
            # prefer other (inferred)
            for p in other.elements:
                if p.name in name_map:
                    yield name_map[p.name].join(p)
                else:
                    yield p

        return self.__class__(elements=list(merge_params()))

    @classmethod
    def _from_parser(cls, parser: Docstring) -> T.Optional[Parameters]:
        parsed_params = [Parameter._from_parser_meta(m) for m in parser.meta if cls._meta_key in m.args]
        if len(parsed_params) > 0:
            return cls(elements=parsed_params)

    @classmethod
    def from_ast(cls, node: _FunctionLike) -> T.Optional[Parameters]:
        args = node.args
        n_positional = len(args.args) - len(args.defaults)
        arg_list = zip(args.args, ([None] * n_positional) + args.defaults)
        parameters = list(Parameter.from_ast(arg, default) for arg, default in arg_list)
        if len(parameters) > 0:
            # ignore self/cls param
            head, *tail = parameters
            if head.name == 'self' or (head.name == 'cls' and _is_classmethod(node)):
                if len(tail) > 0:
                    return cls(elements=tail)
            else:
                return cls(elements=parameters)


class OtherParameters(Parameters):
    _header = "Other Parameters"
    _meta_key = 'other_param'


class Attributes(Parameters):
    _header = "Attributes"
    _meta_key = 'attribute'

    @classmethod
    def from_ast(cls, node: ast.ClassDef) -> T.Optional[Attributes]:
        def attributes():
            for n in node.body:
                if isinstance(n, ast.Assign):
                    for target in n.targets:
                        if isinstance(target, ast.Name):
                            yield Parameter(name=target.id,
                                            typ=n.type_comment)
                elif isinstance(n, ast.AnnAssign):
                    if isinstance(n.target, ast.Name):
                        yield Parameter(name=n.target.id,
                                        typ=type_tools.describe_type_annotation(n.annotation))
                elif isinstance(n, ast.FunctionDef):
                    if _is_property(n, setter=False):
                        description = ast.get_docstring(n, clean=True)
                        if description is not None:
                            description = description.strip()
                        yield Parameter(name=n.name,
                                        typ=type_tools.describe_type_annotation(n.returns) or n.type_comment,
                                        description=description)
        attrs = list(attributes())
        if len(attrs) > 0:
            return cls(elements=attrs)


@_with_todo
@dataclass
class Return(_AbstractKV, _Joinable):
    # required: description, one of (name, type)
    name: T.Optional[str] = None
    typ: T.Optional[str] = None
    description: T.Optional[str] = None

    _todo_name = TODO_RETURN_NAMES
    _todo_typ = TODO_REQUIRED
    _todo_description = TODO_DESCRIPTIONS

    def _primary_key(self) -> str:
        return self.typ

    def _key(self, todo_level: int = 0) -> str:
        name = self.get_name(todo_level)
        typ = self.get_typ(todo_level)
        if name is not None:
            if typ is not None:
                return f"{name} : {typ}"
            else:
                return self.name
        else:
            return typ

    def _value(self, todo_level: int = 0) -> str:
        return self.get_description(todo_level)

    @classmethod
    def _from_parser_meta(cls, meta: dsparser.DocstringMeta) -> Return:
        return cls(
            name=meta.return_name,
            description=meta.description,
            typ=meta.type_name,
        )


@_header
@dataclass
class Returns(_FromParser, _Joinable, _KVContainer):
    _header = "Returns"
    _meta_key = 'returns'

    def join(self, other: _Joinable) -> _Joinable:
        if len(self.elements) > 0:
            returns = self.elements
        else:
            returns = other.elements
        return self.__class__(elements=returns)

    @classmethod
    def _from_parser(cls, parser: Docstring) -> T.Optional[Returns]:
        parsed_returns = [Return._from_parser_meta(m) for m in parser.meta if cls._meta_key in m.args]
        if len(parsed_returns) > 0:
            return cls(elements=parsed_returns)

    @classmethod
    def from_ast(cls, node: _FunctionLike) -> T.Optional[Returns]:
        # TODO
        return_type = type_tools.describe_type_annotation(node.returns) or node.type_comment
        if return_type is not None:
            return cls([Return(typ=return_type)])


class Yields(Returns):
    _header = "Yields"
    _meta_key = 'yields'


class Receives(Parameters):
    _header = "Receives"
    _meta_key = 'receives'

    @classmethod
    def from_ast(cls, node: ast.FunctionDef) -> T.Optional[Receives]:
        pass  # TODO


@_with_todo
@dataclass
class Raise(_AbstractKV, _Joinable):
    exception: T.Optional[str] = None
    condition: T.Optional[str] = None

    _todo_exception = TODO_REQUIRED
    _todo_condition = TODO_DESCRIPTIONS

    def _primary_key(self) -> str:
        return self.exception

    def _key(self, todo_level: int = 0) -> str:
        return self.get_exception(todo_level)

    def _value(self, todo_level: int = 0) -> str:
        return self.get_condition(todo_level)

    @classmethod
    def _from_parser_meta(cls, meta: dsparser.DocstringMeta) -> Raise:
        return cls(
            exception=meta.type_name,
            condition=meta.description,
        )


@_header
@dataclass
class Raises(_FromParser, _Joinable, _KVContainer):
    _header = "Raises"
    _meta_key = 'raises'

    def join(self, other: _Joinable) -> _Joinable:
        our_map = {r.exception: r for r in self.elements}
        their_map = {r.exception: r for r in other.elements}

        def iter_merge():
            for r in self.elements:
                if r.exception in their_map:
                    yield r.join(their_map[r.exception])
                else:
                    yield r

            for r in other.elements:
                if r.exception not in our_map:
                    yield r

        return self.__class__(elements=list(iter_merge()))

    @classmethod
    def _from_parser(cls, parser: Docstring) -> T.Optional[Raises]:
        parsed_raises = [Raise._from_parser_meta(m) for m in parser.meta if cls._meta_key in m.args]
        if len(parsed_raises) > 0:
            return cls(elements=parsed_raises)

    @classmethod
    def from_ast(cls, node: ast.AST) -> T.Optional[Raises]:
        pass  # TODO


class Warns(Raises):
    _header = "Warns"
    _meta_key = 'warns'

    @classmethod
    def from_ast(cls, node: ast.AST) -> T.Optional[Warns]:
        pass  # TODO


@_header
class Warnings(_Simple, _FromParser):
    _header = "Warnings"
    _meta_key = 'warnings'


@_header
class SeeAlso(_Simple, _FromParser):
    _header = "See Also"
    _meta_key = 'see_also'


@_header
class Notes(_Simple, _FromParser):
    _header = "Notes"
    _meta_key = 'notes'


@_header
class References(_Simple, _FromParser):
    _header = "References"
    _meta_key = 'references'


@_header
class Examples(_Simple, _FromParser):
    _header = "Examples"
    _meta_key = 'examples'


@_with_todo
@dataclass
class Docstring(_Joinable):
    summary: T.Optional[str] = None
    extended_summary: T.Optional[str] = None

    _todo_summary = TODO_REQUIRED
    _todo_extended_summary = TODO_EXTENDED_SUMMARY

    @classmethod
    def from_ast(cls, node: ast.AST) -> Docstring:
        if isinstance(node, ast.Module):
            return ModuleDocstring.from_ast(node)
        elif isinstance(node, ast.ClassDef):
            return ClassDocstring.from_ast(node)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if _is_generator(node):
                return GeneratorDocstring.from_ast(node)
            else:
                return FunctionDocstring.from_ast(node)
        else:
            raise ValueError(type(node))

    def lines(self, todo_level: int = 0) -> T.Iterable[str]:
        summary = self.get_summary(todo_level)
        if summary is not None:
            yield from summary.split(sep='\n')

        extended_summary = self.get_extended_summary(todo_level)
        if extended_summary is not None:
            yield ''
            yield from extended_summary.split(sep='\n')

        for section in self.iter_fields():
            if section is not None:
                yield ''
                yield from section.lines(todo_level)

    def build(self, section_seperator: str = '\n', **kwargs) -> str:
        return section_seperator.join(ln.rstrip() for ln in self.lines(**kwargs) if ln is not None)


@_o_dataclass
class ModuleDocstring(Docstring):
    deprecation_warning: T.Optional[DeprecationWarning_] = None
    warnings: T.Optional[Warnings] = None
    see_also: T.Optional[SeeAlso] = None
    notes: T.Optional[Notes] = None
    references: T.Optional[References] = None
    examples: T.Optional[Examples] = None

    @classmethod
    def from_docstring(cls, docstring: str) -> ModuleDocstring:
        parsed = dsparser.numpydoc.parse(docstring)
        return cls(
            summary=parsed.short_description,
            deprecation_warning=DeprecationWarning_._from_parser(parsed),
            extended_summary=parsed.long_description,
            warnings=Warnings._from_parser(parsed),
            see_also=SeeAlso._from_parser(parsed),
            notes=Notes._from_parser(parsed),
            references=References._from_parser(parsed),
            examples=Examples._from_parser(parsed),
        )

    @classmethod
    def from_ast(cls, node: ast.AST) -> ModuleDocstring:
        return cls()


@_o_dataclass
class FunctionDocstring(Docstring):
    deprecation_warning: T.Optional[DeprecationWarning_] = None
    parameters: T.Optional[Parameters] = None
    returns: T.Optional[Returns] = None
    other_parameters: T.Optional[OtherParameters] = None
    raises: T.Optional[Raises] = None
    warns: T.Optional[Warns] = None
    warnings: T.Optional[Warnings] = None
    see_also: T.Optional[SeeAlso] = None
    notes: T.Optional[Notes] = None
    references: T.Optional[References] = None
    examples: T.Optional[Examples] = None

    @classmethod
    def from_docstring(cls, docstring: str) -> ModuleDocstring:
        parsed = dsparser.numpydoc.parse(docstring)
        return cls(
            summary=parsed.short_description,
            deprecation_warning=DeprecationWarning_._from_parser(parsed),
            extended_summary=parsed.long_description,
            parameters=Parameters._from_parser(parsed),
            returns=Returns._from_parser(parsed),
            other_parameters=OtherParameters._from_parser(parsed),
            raises=Raises._from_parser(parsed),
            warns=Warns._from_parser(parsed),
            warnings=Warnings._from_parser(parsed),
            see_also=SeeAlso._from_parser(parsed),
            notes=Notes._from_parser(parsed),
            references=References._from_parser(parsed),
            examples=Examples._from_parser(parsed),
        )

    @classmethod
    def from_ast(cls, node: ast.AST) -> FunctionDocstring:
        if _is_property(node):
            return cls(raises=Raises.from_ast(node), warns=Warns.from_ast(node))
        else:
            return cls(
                parameters=Parameters.from_ast(node),
                returns=Returns.from_ast(node),
                raises=Raises.from_ast(node),
                warns=Warns.from_ast(node)
            )


@_o_dataclass
class GeneratorDocstring(Docstring):
    deprecation_warning: T.Optional[DeprecationWarning_] = None
    parameters: T.Optional[Parameters] = None
    yields: T.Optional[Yields] = None
    receives: T.Optional[Receives] = None
    other_parameters: T.Optional[OtherParameters] = None
    raises: T.Optional[Raises] = None
    warns: T.Optional[Warns] = None
    warnings: T.Optional[Warnings] = None
    see_also: T.Optional[SeeAlso] = None
    notes: T.Optional[Notes] = None
    references: T.Optional[References] = None
    examples: T.Optional[Examples] = None

    @classmethod
    def from_docstring(cls, docstring: str) -> ModuleDocstring:
        parsed = dsparser.numpydoc.parse(docstring)
        return cls(
            summary=parsed.short_description,
            deprecation_warning=DeprecationWarning_._from_parser(parsed),
            extended_summary=parsed.long_description,
            parameters=Parameters._from_parser(parsed),
            yields=Yields._from_parser(parsed),
            receives=Receives._from_parser(parsed),
            other_parameters=OtherParameters._from_parser(parsed),
            raises=Raises._from_parser(parsed),
            warns=Warns._from_parser(parsed),
            warnings=Warnings._from_parser(parsed),
            see_also=SeeAlso._from_parser(parsed),
            notes=Notes._from_parser(parsed),
            references=References._from_parser(parsed),
            examples=Examples._from_parser(parsed),
        )

    @classmethod
    def from_ast(cls, node: ast.AST) -> GeneratorDocstring:
        if _is_property(node):
            return cls(raises=Raises.from_ast(node), warns=Warns.from_ast(node))
        else:
            return cls(
                parameters=Parameters.from_ast(node),
                yields=Yields.from_ast(node),
                receives=Receives.from_ast(node),
                raises=Raises.from_ast(node),
                warns=Warns.from_ast(node)
            )


@_o_dataclass
class ClassDocstring(FunctionDocstring):
    deprecation_warning: T.Optional[DeprecationWarning_] = None
    parameters: T.Optional[Parameters] = None
    attributes: T.Optional[Attributes] = None
    other_parameters: T.Optional[OtherParameters] = None
    raises: T.Optional[Raises] = None
    warns: T.Optional[Warns] = None
    warnings: T.Optional[Warnings] = None
    see_also: T.Optional[SeeAlso] = None
    notes: T.Optional[Notes] = None
    references: T.Optional[References] = None
    examples: T.Optional[Examples] = None

    @classmethod
    def from_docstring(cls, docstring: str) -> ModuleDocstring:
        parsed = dsparser.numpydoc.parse(docstring)
        return cls(
            summary=parsed.short_description,
            deprecation_warning=DeprecationWarning_._from_parser(parsed),
            extended_summary=parsed.long_description,
            parameters=Parameters._from_parser(parsed),
            attributes=Attributes._from_parser(parsed),
            other_parameters=OtherParameters._from_parser(parsed),
            raises=Raises._from_parser(parsed),
            warns=Warns._from_parser(parsed),
            warnings=Warnings._from_parser(parsed),
            see_also=SeeAlso._from_parser(parsed),
            notes=Notes._from_parser(parsed),
            references=References._from_parser(parsed),
            examples=Examples._from_parser(parsed),
        )

    @classmethod
    def from_ast(cls, node: ast.AST) -> ClassDocstring:
        init_node = ast_tools.search_ast(node, lambda n: isinstance(n, ast.FunctionDef) and n.name == '__init__')
        return cls(
            parameters=Parameters.from_ast(init_node) if init_node is not None else None,
            attributes=Attributes.from_ast(node),
            raises=Raises.from_ast(node),
            warns=Warns.from_ast(node)
        )
