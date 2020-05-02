""" Unit tests covering numpydoctor.ast_tools """

import itertools
import ast
from numpydoctor import docstring_tools
from typing import Iterable


def test_o_dataclass():
    @docstring_tools._o_dataclass
    class MyDataclass:
        q: int
        w: int
        e: int
        r: int
        t: int
        y: int
        u: int
        i: int
        o: int
        p: int

    o = MyDataclass(y=6, t=5, o=9, u=7, i=8, p=10, q=1, w=2, e=3, r=4)
    ordered_fields = list(o.iter_fields())
    assert ordered_fields == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_parameter_from_ast():
    tree = ast.parse("""
def myfunc(a, b: int, c: Union[str, bytes], d = "hello", e: str = "world", *args, **kwargs):
    pass
""")
    args = tree.body[0].args
    a, b, c, d, e = list(zip(args.args, [None, None, None] + args.defaults))

    def do_test(argdefault, expected_key, expected_value):
        arg, default = argdefault
        parameter = docstring_tools.Parameter.from_ast(arg, default)
        assert parameter._key() == expected_key, f"expected {expected_key}, got {parameter._key()}"
        assert parameter._value() == expected_value, f"expected {expected_value}, got {parameter._value()}"

    yield do_test, a, 'a', None
    yield do_test, b, 'b : int', None
    yield do_test, c, 'c : str or bytes', None
    yield do_test, d, 'd : optional', None
    yield do_test, e, 'e : str, optional', None


def _assert_dataclass_eq(actual, expected):
    if hasattr(expected, '__dataclass_fields__'):  # i.e. `expected` is a dataclass
        assert hasattr(actual, '__dataclass_fields__'), f"Expected dataclass, got {type(actual)}"
        for fieldname in expected.__dataclass_fields__:
            assert fieldname in actual.__dataclass_fields__, f"missing key {fieldname}"
            _assert_dataclass_eq(getattr(actual, fieldname), getattr(expected, fieldname))
    elif isinstance(expected, (list, tuple, set)):
        assert isinstance(actual, Iterable), f"expected iterable field, got {type(actual)}"
        for a, e in itertools.zip_longest(actual, expected):
            _assert_dataclass_eq(a, e)
    else:
        assert actual == expected, f"{actual} != {expected}"


def _from_ast_test_factory(ds_element):
    def do_test(tree, expected_element):
        element = ds_element.from_ast(tree)
        if expected_element is not None:
            _assert_dataclass_eq(element, expected_element)
        else:
            assert element is None, f"expected None, got {element}"
    return do_test


def test_parameters_from_ast():
    do_test = _from_ast_test_factory(docstring_tools.Parameters)

    yield do_test, ast.parse("def myfunc(): pass").body[0], None

    yield do_test, ast.parse("""
def myfunc(a, b: int, c: str = "hello, world!", *args, **kwargs):
    pass
    """).body[0], docstring_tools.Parameters(
        elements=[
            docstring_tools.Parameter(
                name='a',
                optional=False,
            ),
            docstring_tools.Parameter(
                name='b',
                typ='int',
                optional=False,
            ),
            docstring_tools.Parameter(
                name='c',
                typ='str',
                optional=True,
            ),
        ]
    )

    yield do_test, ast.parse(
        "def mymethod(self, arg1): pass"
    ).body[0], docstring_tools.Parameters(
        elements=[
            docstring_tools.Parameter(
                name='arg1',
                optional=False
            )
        ]
    )

    yield do_test, ast.parse(
        "def mymethod(self): pass"
    ).body[0], None

    yield do_test, ast.parse("""
@classmethod
def myclassmethod(cls, arg1):
    pass
    """).body[0], docstring_tools.Parameters(
        elements=[
            docstring_tools.Parameter(
                name='arg1',
                optional=False
            )
        ]
    )

    yield do_test, ast.parse(
        "def not_a_classmethod(cls, arg1): pass"
    ).body[0], docstring_tools.Parameters(
        elements=[
            docstring_tools.Parameter(
                name='cls',
                optional=False,
            ),
            docstring_tools.Parameter(
                name='arg1',
                optional=False
            )
        ]
    )


def test_attributes_from_ast():
    do_test = _from_ast_test_factory(docstring_tools.Attributes)

    yield do_test, ast.parse("""
class MyClass:
    def __init__(self): pass
    """).body[0], None

    yield do_test, ast.parse("""
class MyClass:
    a = 1
    b: int = 2
    c: str

    @property
    def d(self) -> bool:
        \""" Some kind of boolean \"""
        return self._d

    @d.setter
    def d(self, value: bool):
        self._d = value

    @property
    def e(self):
        pass
    """).body[0], docstring_tools.Attributes(
        elements=[
            docstring_tools.Parameter(
                name='a',
            ),
            docstring_tools.Parameter(
                name='b',
                typ='int',
            ),
            docstring_tools.Parameter(
                name='c',
                typ='str',
            ),
            docstring_tools.Parameter(
                name='d',
                typ='bool',
                description="Some kind of boolean"
            ),
            docstring_tools.Parameter(
                name='e'
            ),
        ]
    )


def test_join_docstring():
    def do_test(ours, theirs, expected):
        joined = ours.join(theirs)
        _assert_dataclass_eq(joined, expected)

    docstring_a = docstring_tools.FunctionDocstring(
        summary="summary a",
        extended_summary="extended_summary a",
        parameters=docstring_tools.Parameters(
            elements=[
                docstring_tools.Parameter(
                    name="arg1",
                    description="description1",
                    typ="type1",
                    optional=False
                ),
                docstring_tools.Parameter(
                    name="arg2",
                ),
                docstring_tools.Parameter(
                    name="only_in_a",
                ),
            ]
        ),
        other_parameters=docstring_tools.OtherParameters(
            elements=[
                docstring_tools.Parameter(
                    name="other_param_only_in_a",
                )
            ]
        ),
        returns=docstring_tools.Returns(
            elements=[
                docstring_tools.Return(
                    name="return1",
                    typ="type1",
                    description="description1"
                ),
                docstring_tools.Return(
                    typ="only_type"
                ),
                docstring_tools.Return(
                    typ="only_in_a"
                ),
            ]
        ),
        warns=docstring_tools.Warns(
            elements=[
                docstring_tools.Raise(
                    exception="AWarning",
                    condition="only in a"
                ),
                docstring_tools.Raise(
                    exception="UserWarning"
                )
            ]
        ),
    )

    docstring_b = docstring_tools.FunctionDocstring(
        summary="summary b",
        parameters=docstring_tools.Parameters(
            elements=[
                docstring_tools.Parameter(
                    name="arg1",
                    description="description1",
                    typ="type1",
                    optional=False
                ),
                docstring_tools.Parameter(
                    name="arg2",
                    description="description2",
                    typ="type2",
                    optional=False
                ),
                docstring_tools.Parameter(
                    name="only_in_b",
                ),
            ]
        ),
        returns=docstring_tools.Returns(
            elements=[
                docstring_tools.Return(
                    name="return1",
                    typ="type1",
                    description="description1"
                ),
                docstring_tools.Return(
                    typ="only_type"
                ),
                docstring_tools.Return(
                    typ="only_in_b"
                ),
            ]
        ),
        warns=docstring_tools.Warns(
            elements=[
                docstring_tools.Raise(
                    exception="UserWarning",
                    condition="condition only in b"
                )
            ]
        ),
    )

    yield do_test, docstring_a, docstring_b, docstring_tools.FunctionDocstring(
        summary="summary a",
        extended_summary="extended_summary a",
        parameters=docstring_tools.Parameters(
            elements=[
                docstring_tools.Parameter(
                    name="arg1",
                    description="description1",
                    typ="type1",
                    optional=False
                ),
                docstring_tools.Parameter(
                    name="arg2",
                    description="description2",
                    typ="type2",
                    optional=False
                ),
                docstring_tools.Parameter(
                    name="only_in_b",
                ),
            ]
        ),
        other_parameters=docstring_tools.OtherParameters(
            elements=[
                docstring_tools.Parameter(
                    name="other_param_only_in_a",
                )
            ]
        ),
        returns=docstring_tools.Returns(
            elements=[
                docstring_tools.Return(
                    name="return1",
                    typ="type1",
                    description="description1"
                ),
                docstring_tools.Return(
                    typ="only_type"
                ),
                docstring_tools.Return(
                    typ="only_in_a"
                ),
            ]
        ),
        warns=docstring_tools.Warns(
            elements=[
                docstring_tools.Raise(
                    exception="AWarning",
                    condition="only in a"
                ),
                docstring_tools.Raise(
                    exception="UserWarning",
                    condition="condition only in b"
                )
            ]
        ),
    )

    yield do_test, docstring_b, docstring_a, docstring_tools.FunctionDocstring(
        summary="summary b",
        extended_summary="extended_summary a",
        parameters=docstring_tools.Parameters(
            elements=[
                docstring_tools.Parameter(
                    name="arg1",
                    description="description1",
                    typ="type1",
                    optional=False
                ),
                docstring_tools.Parameter(
                    name="arg2",
                    description="description2",
                    typ="type2",
                    optional=False
                ),
                docstring_tools.Parameter(
                    name="only_in_a",
                ),
            ]
        ),
        other_parameters=docstring_tools.OtherParameters(
            elements=[
                docstring_tools.Parameter(
                    name="other_param_only_in_a",
                )
            ]
        ),
        returns=docstring_tools.Returns(
            elements=[
                docstring_tools.Return(
                    name="return1",
                    typ="type1",
                    description="description1"
                ),
                docstring_tools.Return(
                    typ="only_type"
                ),
                docstring_tools.Return(
                    typ="only_in_b"
                ),
            ]
        ),
        warns=docstring_tools.Warns(
            elements=[
                docstring_tools.Raise(
                    exception="UserWarning",
                    condition="condition only in b"
                ),
                docstring_tools.Raise(
                    exception="AWarning",
                    condition="only in a"
                ),
            ]
        ),
    )


def test_iter_lines():
    def do_test(docstring, expected_lines):
        for actual, expected in itertools.zip_longest(docstring.lines(), expected_lines):
            assert actual == expected, f"{actual} != {expected}"

    yield do_test, docstring_tools.DeprecationWarning_(
        version="1.0", message="message\nline 2"
    ), [
        ".. deprecated:: 1.0",
        "    message",
        "    line 2"
    ]

    yield do_test, docstring_tools.Parameter(
        name="name", description="description\nline 2", typ="type", optional=True
    ), [
        'name : type, optional',
        '    description',
        '    line 2'
    ]

    yield do_test, docstring_tools.Return(
        name="name", description="description\nline 2", typ="type"
    ), [
        'name : type',
        '    description',
        '    line 2'
    ]

    yield do_test, docstring_tools.Raise(
        exception="exception", condition="condition\nline 2"
    ), [
        'exception',
        '    condition',
        '    line 2'
    ]

    yield do_test, docstring_tools.FunctionDocstring(summary="summary"), ["summary"]

    yield do_test, docstring_tools.FunctionDocstring(
        summary="summary", extended_summary="extended summary\nline 2"
    ), [
        'summary',
        '',
        'extended summary',
        'line 2'
    ]

    yield do_test, docstring_tools.FunctionDocstring(
        summary="summary",
        extended_summary="extended_summary\nline 2",
        deprecation_warning=docstring_tools.DeprecationWarning_(
            version="1.0",
            message="message\nline 2"
        ),
        parameters=docstring_tools.Parameters(
            elements=[
                docstring_tools.Parameter(
                    name='arg1',
                    typ='type1',
                    description='description\nline 2'
                ),
                docstring_tools.Parameter(
                    name='arg2',
                    typ='type2',
                    description='description2\nline 2',
                    optional=True
                )
            ]
        )
    ), [
        'summary',
        '',
        'extended_summary',
        'line 2',
        '',
        '.. deprecated:: 1.0',
        '    message',
        '    line 2',
        '',
        'Parameters',
        '----------',
        'arg1 : type1',
        '    description',
        '    line 2',
        'arg2 : type2, optional',
        '    description2',
        '    line 2'
    ]


def test_todo_levels():
    docstring = docstring_tools.FunctionDocstring(
        deprecation_warning=docstring_tools.DeprecationWarning_(),
        parameters=docstring_tools.Parameters(
            elements=[
                docstring_tools.Parameter(
                    name='arg1',
                    typ='type1'
                ),
                docstring_tools.Parameter(
                    name='arg2',
                ),
                docstring_tools.Parameter(),
            ]
        ),
        returns=docstring_tools.Returns(
            elements=[
                docstring_tools.Return(
                    name='return1',
                    typ='type1'
                ),
                docstring_tools.Return(
                    typ='type2'
                ),
                docstring_tools.Return(),
            ]
        ),
        warns=docstring_tools.Warns(
            elements=[
                docstring_tools.Raise(
                    exception='warning1'
                ),
                docstring_tools.Raise()
            ]
        )
    )

    def do_test(todo_level: int, expected: str):
        actual = docstring.build(todo_level=todo_level)
        assert actual == expected.strip(), f"{actual}\n!=\n{expected}"

    yield do_test, docstring_tools.TODO_REQUIRED, """
<TODO summary>

.. deprecated:: <TODO version>
    <TODO message>

Parameters
----------
arg1 : type1
arg2
<TODO name>

Returns
-------
return1 : type1
type2
<TODO typ>

Warns
-----
warning1
<TODO exception>
"""

    yield do_test, docstring_tools.TODO_TYPES, """
<TODO summary>

.. deprecated:: <TODO version>
    <TODO message>

Parameters
----------
arg1 : type1
arg2 : <TODO typ>
<TODO name> : <TODO typ>

Returns
-------
return1 : type1
type2
<TODO typ>

Warns
-----
warning1
<TODO exception>
"""

    yield do_test, docstring_tools.TODO_DESCRIPTIONS, """
<TODO summary>

.. deprecated:: <TODO version>
    <TODO message>

Parameters
----------
arg1 : type1
    <TODO description>
arg2 : <TODO typ>
    <TODO description>
<TODO name> : <TODO typ>
    <TODO description>

Returns
-------
return1 : type1
    <TODO description>
type2
    <TODO description>
<TODO typ>
    <TODO description>

Warns
-----
warning1
    <TODO condition>
<TODO exception>
    <TODO condition>
"""

    yield do_test, docstring_tools.TODO_RETURN_NAMES, """
<TODO summary>

.. deprecated:: <TODO version>
    <TODO message>

Parameters
----------
arg1 : type1
    <TODO description>
arg2 : <TODO typ>
    <TODO description>
<TODO name> : <TODO typ>
    <TODO description>

Returns
-------
return1 : type1
    <TODO description>
<TODO name> : type2
    <TODO description>
<TODO name> : <TODO typ>
    <TODO description>

Warns
-----
warning1
    <TODO condition>
<TODO exception>
    <TODO condition>
"""

    yield do_test, docstring_tools.TODO_EXTENDED_SUMMARY, """
<TODO summary>

<TODO extended_summary>

.. deprecated:: <TODO version>
    <TODO message>

Parameters
----------
arg1 : type1
    <TODO description>
arg2 : <TODO typ>
    <TODO description>
<TODO name> : <TODO typ>
    <TODO description>

Returns
-------
return1 : type1
    <TODO description>
<TODO name> : type2
    <TODO description>
<TODO name> : <TODO typ>
    <TODO description>

Warns
-----
warning1
    <TODO condition>
<TODO exception>
    <TODO condition>
"""



def test_parse_module_docstring():
    def do_test(docstring, expected_instance):
        parsed = docstring_tools.ModuleDocstring.from_docstring(docstring)
        _assert_dataclass_eq(parsed, expected_instance)

    yield do_test, "Short description", docstring_tools.ModuleDocstring(
        summary="Short description"
    )

    yield do_test, "Short description\n\nLong description", docstring_tools.ModuleDocstring(
        summary="Short description",
        extended_summary="Long description"
    )

    yield do_test, """Short description.

Long description,
spanning several lines.

.. deprecated:: v5.9.7.8
    This module's deprecated!
    Use something else!

Warnings
--------
None of this is real!

See Also
--------
numpy.ndarray : arrays
and something else perhaps

Notes
-----
something goes here
another line, too

References
----------
.. [1] G. Debord, "Society of the Spectacle", 1967

Examples
--------
An example of using this module:
>>> print(''.join(c for c in "this module" if c not in 'aeiou'))
ths mdl
    """, docstring_tools.ModuleDocstring(
        summary="Short description.",
        extended_summary="Long description,\nspanning several lines.",
        deprecation_warning=docstring_tools.DeprecationWarning_(
            version="v5.9.7.8",
            message="This module's deprecated!\nUse something else!",
        ),
        warnings=docstring_tools.Warnings(
            value="None of this is real!"
        ),
        see_also=docstring_tools.SeeAlso(
            value="numpy.ndarray : arrays\nand something else perhaps"
        ),
        notes=docstring_tools.Notes(
            value="something goes here\nanother line, too"
        ),
        references=docstring_tools.References(
            value='.. [1] G. Debord, "Society of the Spectacle", 1967'
        ),
        examples=docstring_tools.Examples(
            value="""An example of using this module:
>>> print(''.join(c for c in "this module" if c not in 'aeiou'))
ths mdl"""
        )
    )


def test_parse_function_docstring():
    def do_test(docstring, expected_instance):
        parsed = docstring_tools.FunctionDocstring.from_docstring(docstring)
        _assert_dataclass_eq(parsed, expected_instance)

    yield do_test, "Short description", docstring_tools.FunctionDocstring(
        summary="Short description"
    )

    yield do_test, "Short description\n\nLong description", docstring_tools.FunctionDocstring(
        summary="Short description",
        extended_summary="Long description"
    )

    yield do_test, r"""Summarize the function in one line.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    .. deprecated:: v5.9.7.8
       This module's deprecated!
       Use something else!

    Parameters
    ----------
    var1 : array_like
        Array_like means all those objects -- lists, nested lists, etc. --
        that can be converted to an array.  We can also refer to
        variables like `var1`.
    var2 : int
        description 2
    *args : iterable
        Other arguments.
    long_var_name : {'hi', 'ho'}, optional
        Choices in brackets, default first when optional.
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    type
        Explanation of anonymous return value of type ``type``.
    describe : type
        Explanation of return value named `describe`.
    type_without_description

    Other Parameters
    ----------------
    only_seldom_used_keywords : type, optional
        Explanation

    Raises
    ------
    BadException
        Because you shouldn't have done that.
    MissingDescriptionException

    Warns
    -----
    UserWarning
        When the user needs to be warned.
    MissingDescriptionWarning

    Warnings
    --------
    None of this is real!

    See Also
    --------
    numpy.array : Relationship (optional).
    numpy.ndarray : Relationship (optional), which could be fairly long, in
                    which case the line wraps here.
    numpy.dot, numpy.linalg.norm, numpy.eye

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    This can have multiple paragraphs.

    You may include some math:

    .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

    And even use a Greek symbol like :math:`\omega` inline.

    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.

    .. [1] O. McNoleg, "The integration of GIS, remote sensing,
       expert systems and adaptive co-kriging for environmental habitat
       modelling of the Highland Haggis using object-oriented, fuzzy-logic
       and neural-network techniques," Computers & Geosciences, vol. 22,
       pp. 585-588, 1996.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a = [1, 2, 3]
    >>> print([x + 3 for x in a])
    [4, 5, 6]
    >>> print("a\nb")
    a
    b
    """, docstring_tools.FunctionDocstring(
        summary="Summarize the function in one line.",
        extended_summary=(
            "Several sentences providing an extended description. Refer to\n"
            "variables using back-ticks, e.g. `var`."),
        deprecation_warning=docstring_tools.DeprecationWarning_(
            version="v5.9.7.8",
            message="This module's deprecated!\nUse something else!",
        ),
        parameters=docstring_tools.Parameters(
            elements=[
                docstring_tools.Parameter(
                    name='var1',
                    typ='array_like',
                    optional=False,
                    description=(
                        "Array_like means all those objects -- lists, nested lists, etc. --\n"
                        "that can be converted to an array.  We can also refer to\n"
                        "variables like `var1`."
                    )
                ),
                docstring_tools.Parameter(
                    name='var2',
                    typ='int',
                    optional=False,
                    description="description 2"
                ),
                docstring_tools.Parameter(
                    name='*args',
                    typ='iterable',
                    optional=False,
                    description="Other arguments."
                ),
                docstring_tools.Parameter(
                    name="long_var_name",
                    typ="{'hi', 'ho'}",
                    optional=True,
                    description="Choices in brackets, default first when optional."
                ),
                docstring_tools.Parameter(
                    name='**kwargs',
                    typ='dict',
                    optional=False,
                    description="Keyword arguments."
                ),
            ]
        ),
        returns=docstring_tools.Returns(
            elements=[
                docstring_tools.Return(
                    name=None,
                    typ='type',
                    description='Explanation of anonymous return value of type ``type``.'
                ),
                docstring_tools.Return(
                    name='describe',
                    typ='type',
                    description='Explanation of return value named `describe`.'
                ),
                docstring_tools.Return(
                    name=None,
                    typ='type_without_description',
                    description=None
                ),
            ]
        ),
        other_parameters=docstring_tools.OtherParameters(
            elements=[
                docstring_tools.Parameter(
                    name="only_seldom_used_keywords",
                    typ='type',
                    optional=True,
                    description="Explanation"
                )
            ]
        ),
        raises=docstring_tools.Raises(
            elements=[
                docstring_tools.Raise(
                    exception='BadException',
                    condition="Because you shouldn't have done that.",
                ),
                docstring_tools.Raise(
                    exception='MissingDescriptionException',
                ),
            ]
        ),
        warns=docstring_tools.Warns(
            elements=[
                docstring_tools.Raise(
                    exception='UserWarning',
                    condition="When the user needs to be warned.",
                ),
                docstring_tools.Raise(
                    exception='MissingDescriptionWarning',
                ),
            ]
        ),
        warnings=docstring_tools.Warnings(
            value="None of this is real!"
        ),
        see_also=docstring_tools.SeeAlso(
            value="""numpy.array : Relationship (optional).
numpy.ndarray : Relationship (optional), which could be fairly long, in
                which case the line wraps here.
numpy.dot, numpy.linalg.norm, numpy.eye"""
        ),
        notes=docstring_tools.Notes(
            value="""Notes about the implementation algorithm (if needed).

This can have multiple paragraphs.

You may include some math:

.. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

And even use a Greek symbol like :math:`\omega` inline."""
        ),
        references=docstring_tools.References(
            value="""Cite the relevant literature, e.g. [1]_.  You may also cite these
references in the notes section above.

.. [1] O. McNoleg, "The integration of GIS, remote sensing,
   expert systems and adaptive co-kriging for environmental habitat
   modelling of the Highland Haggis using object-oriented, fuzzy-logic
   and neural-network techniques," Computers & Geosciences, vol. 22,
   pp. 585-588, 1996."""
        ),
        examples=docstring_tools.Examples(
            value="""These are written in doctest format, and should illustrate how to
use the function.

>>> a = [1, 2, 3]
>>> print([x + 3 for x in a])
[4, 5, 6]
>>> print("a\\nb")
a
b"""
        )
    )


def test_parse_generator_docstring():
    def do_test(docstring, expected_instance):
        parsed = docstring_tools.GeneratorDocstring.from_docstring(docstring)
        _assert_dataclass_eq(parsed, expected_instance)

    yield do_test, "Short description", docstring_tools.GeneratorDocstring(
        summary="Short description"
    )

    yield do_test, "Short description\n\nLong description", docstring_tools.GeneratorDocstring(
        summary="Short description",
        extended_summary="Long description"
    )

    yield do_test, """summary

    extended summary
        multiple lines

    Parameters
    ----------
    arg1
    arg2 : type2, optional
        description 2

    Yields
    ------
    type1
        description 1
    name2 : type2

    Receives
    --------
    receive_arg_1
    receive_arg_2 : type2, optional
        description 2
    """, docstring_tools.GeneratorDocstring(
        summary="summary",
        extended_summary="extended summary\n    multiple lines",
        parameters=docstring_tools.Parameters(
            elements=[
                docstring_tools.Parameter(
                    name='arg1',
                    typ=None,
                    optional=None,
                    description=None
                ),
                docstring_tools.Parameter(
                    name='arg2',
                    typ='type2',
                    optional=True,
                    description="description 2"
                ),
            ]
        ),
        yields=docstring_tools.Yields(
            elements=[
                docstring_tools.Return(
                    name=None,
                    typ='type1',
                    description='description 1'
                ),
                docstring_tools.Return(
                    name='name2',
                    typ='type2',
                    description=None
                ),
            ]
        ),
        receives=docstring_tools.Receives(
            elements=[
                docstring_tools.Parameter(
                    name='receive_arg_1',
                    typ=None,
                    optional=None,
                    description=None
                ),
                docstring_tools.Parameter(
                    name='receive_arg_2',
                    typ='type2',
                    optional=True,
                    description="description 2"
                ),
            ]
        )
    )


def test_parse_class_docstring():
    def do_test(docstring, expected_instance):
        parsed = docstring_tools.ClassDocstring.from_docstring(docstring)
        _assert_dataclass_eq(parsed, expected_instance)

    yield do_test, "Short description", docstring_tools.ClassDocstring(
        summary="Short description"
    )

    yield do_test, "Short description\n\nLong description", docstring_tools.ClassDocstring(
        summary="Short description",
        extended_summary="Long description"
    )

    yield do_test, """summary

    extended summary
        multiple lines

    Parameters
    ----------
    arg1
    arg2 : type2, optional
        description 2

    Attributes
    ----------
    attr1
    attr2 : type2
        description 2
    """, docstring_tools.ClassDocstring(
        summary="summary",
        extended_summary="extended summary\n    multiple lines",
        parameters=docstring_tools.Parameters(
            elements=[
                docstring_tools.Parameter(
                    name='arg1',
                    typ=None,
                    optional=None,
                    description=None
                ),
                docstring_tools.Parameter(
                    name='arg2',
                    typ='type2',
                    optional=True,
                    description="description 2"
                ),
            ]
        ),
        attributes=docstring_tools.Attributes(
            elements=[
                docstring_tools.Parameter(
                    name='attr1',
                    typ=None,
                    description=None
                ),
                docstring_tools.Parameter(
                    name='attr2',
                    typ='type2',
                    optional=False,
                    description="description 2"
                ),
            ]
        )
    )
