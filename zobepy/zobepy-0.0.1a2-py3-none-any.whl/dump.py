#!/usr/bin/env python
"""Dump to know what it is."""

import inspect
import typing


"""Callback function definition as dump_class

Parameters
----------
target : object
    The target object you want to dump.
indent : int
    Depth to indent
no_print : bool
    If False(Default), immediately output by print().
    If True, no output. Use return value.

Returns
-------
str
    Dump result text.
"""
DumpClassCallback = typing.Callable[[object, int, bool], str]


def dump_class(target: object, indent: int = 0, no_print: bool = False) -> str:
    """Dump class information.

    Parameters
    ----------
    target : object
        The target object you want to dump.
    indent : int
        Depth to indent
    no_print : bool
        If False(Default), immediately output by print().
        If True, no output. Use return value.

    Returns
    -------
    str
        Dump result text.

    """
    dump_string = ''

    if type(target) is not type:
        return dump_string

    s = 'description of {}.{}:'
    s = '  ' * indent + s.format(target.__module__, target.__name__)
    dump_string = s + '\n'
    s = '  ' * (indent + 1) + '__hash__: {}'.format(target.__hash__(target))
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__doc__: {}'.format(target.__doc__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__qualname__: {}'.format(target.__qualname__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__module__: {}'.format(target.__module__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__name__: {}'.format(target.__name__)
    dump_string += s + '\n'

    s = 'methods of {}.{}:'
    s = '  ' * indent + s.format(target.__module__, target.__name__)
    dump_string += s + '\n'
    s = dump_methods(target, indent + 1, no_print)
    s = s.rstrip('\n')
    dump_string += s

    if no_print is False:
        print(dump_string)
    return dump_string + '\n'


def dump_class_simple(target: object, indent: int = 0, no_print: bool = False) -> str:
    """Dump class information (simple).

    A function like dump_class but no output of methods.

    Parameters
    ----------
    target : object
        The target object you want to dump.
    indent : int
        Depth to indent
    no_print : bool
        If False(Default), immediately output by print().
        If True, no output. Use return value.

    Returns
    -------
    str
        Dump result text.

    """
    dump_string = ''

    if type(target) is not type:
        return dump_string

    s = 'description of {}.{}:'
    s = '  ' * indent + s.format(target.__module__, target.__name__)
    dump_string = s + '\n'
    s = '  ' * (indent + 1) + '__hash__: {}'.format(target.__hash__(target))
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__doc__: {}'.format(target.__doc__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__qualname__: {}'.format(target.__qualname__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__module__: {}'.format(target.__module__)
    dump_string += s + '\n'
    s = '  ' * (indent + 1) + '__name__: {}'.format(target.__name__)
    dump_string += s

    if no_print is False:
        print(dump_string)
    return dump_string + '\n'


def dump_class_dummy(target: object, indent: int = 0, no_print: bool = False) -> str:
    """Pseudo implementation of DumpClassCallback outputs and returns nothing.

    Parameters
    ----------
    target: object
    indent: int
    no_print: bool

    Returns
    -------
    str
        Always empty string

    """
    return ''


def dump_class_recursively(target: object, max_depth: int = 10, no_print: bool = False,
                           dump_class_callback: DumpClassCallback = dump_class) -> str:
    """Dump class information, and its ancestors.

    Parameters
    ----------
    target : object
        The target you want to dump.
    max_depth : int, default 10
        Maximum number of ascending.
    no_print: bool, default False
        Set True suspends all print() call.
        Get dump result from return value.
    dump_class_callback: DumpClassCallback, default dump_class

    Returns
    -------
    str
        Dump result text.
    """
    return _dump_class_recursively_internal(
        target, max_depth, 0, None,
        dump_class_callback,
        no_print)


def _dump_class_recursively_internal(target, depth: int = 10, indent: int = 0,
                                     duplication_checker: dict = None,
                                     dump_class_callback: DumpClassCallback = dump_class,
                                     no_print: bool = False):
    dump_string = ''

    if depth <= 0:
        return dump_string
    if type(target) is not type:
        target = target.__class__
    if type(target) is not type:
        return dump_string

    if duplication_checker is None:
        duplication_checker = dict()

    if hasattr(target, '__hash__') is False:
        # do not dump for non-hashed target.
        # (it is not valid class, isn't it?)
        return dump_string

    target_hash = _get_hash_string(target)
    if target_hash in duplication_checker:
        # already dumped class
        duplication_checker[target_hash] += 1
        return dump_string

    duplication_checker[target_hash] = 0

    s = '  ' * indent + '{}.{}:'.format(target.__module__, target.__name__)
    dump_string += s + '\n'
    if no_print is False:
        print(s)

    dump_string += dump_class_callback(target, indent + 1, no_print)

    target_bases = list()
    if hasattr(target, '__bases__') and target.__bases__:
        target_bases = list(target.__bases__)
        try:
            target_bases.remove(object)
        except ValueError:
            pass

    if len(target_bases) > 0:
        s = '{} parent(s) found for [{}.{}]'
        s = s.format(len(target_bases), target.__module__, target.__name__)
        s = '  ' * (indent + 1) + s
        dump_string += s + '\n'
        if no_print is False:
            print(s)
        for c in target_bases:
            s = '  ' * (indent + 2) + '[{}.{}]'.format(c.__module__, c.__name__)
            dump_string += s + '\n'
            if no_print is False:
                print(s)

        for c in target_bases:
            c_hash = _get_hash_string(c)
            if c_hash in duplication_checker:
                # already dump class
                # s = '  '*(indent+2) + 'skipped - already dumped'
                # dump_string += s + '\n'
                # if no_print is False:
                #     print(s)
                duplication_checker[c_hash] += 1
                continue
            dump_string += _dump_class_recursively_internal(
                c, depth - 1, indent + 1, duplication_checker,
                dump_class_callback,
                no_print)
    else:
        s = '  ' * (indent + 1) + 'have no parents'
        dump_string += s + '\n'
        if no_print is False:
            print(s)

    return dump_string


def _get_hash_string(target):
    """Calculate Object hash.

    Parameters
    ----------
    target
        An object. It must implement or inherit __hash__ method.

    Returns
    -------
        The hash string.

    """
    return str(target.__hash__(target))


def dump_attributes(target, indent: int = 0, no_print: bool = False):
    """Dump class attributes.

    Parameters
    ----------
    target : object
        The target you want to dump. Class or Instance is acceptable.
    indent : int
        Depth to indent
    no_print : bool
        If False(Default), immediately output by print().
        If True, no output. Use return value.

    Returns
    -------
    str
        Dump result text.
    """
    dump_string = ''

    if False is inspect.isclass(target)\
            and isinstance(target, object):
        target = target.__class__
    if False is inspect.isclass(target):
        return dump_string

    for a in inspect.classify_class_attrs(target):
        if len(dump_string) > 0:
            dump_string += '\n'
        s = '  ' * indent + str(a)
        dump_string += s
        print(a.kind)
        if a.kind == 'method':
            attr = getattr(target, a.name)
            print('attr: ' + str(attr))
            print('getdoc: ' + str(inspect.getdoc(attr)))
            try:
                print('signature: ' + str(inspect.signature(attr)))
            except ValueError:
                print('signature: Error - inspection failed')
            # print('getmembers: ' + str(inspect.getmembers(attr)))
            # print('method!!')
            # method = a.object
            # print('method: ' + str(method))
            # print(method.__doc__)
            # print(method.__name__)
            # print(method.__func__)
            # print(method.__self__)

    if no_print is False:
        print(dump_string)

    return dump_string + '\n'


def dump_methods(target, indent: int = 0, no_print: bool = False):
    """Dump methods of a class.

    Parameters
    ----------
    target : object
        The target you want to dump. Class or Instance is acceptable.
    indent : int
        Depth to indent
    no_print : bool
        If False(Default), immediately output by print().
        If True, no output. Use return value.

    Returns
    -------
    str
        Dump result text.

    """
    dump_string = ''

    if False is inspect.isclass(target)\
            and isinstance(target, object):
        target = target.__class__
    if False is inspect.isclass(target):
        return dump_string

    for a in inspect.classify_class_attrs(target):
        if a.kind == 'method':
            attr = getattr(target, a.name)
            # target_class = target
            # if a.defining_class:
            #     target_class = a.defining_class
            attr = getattr(a.defining_class, a.name)
            signature = None
            try:
                signature = inspect.signature(attr)
            except ValueError:
                pass
            s = a.name
            if signature is not None:
                s += str(signature)

            if len(dump_string) > 0:
                dump_string += '\n'
            s = '  ' * indent + s
            dump_string += s

    if no_print is False:
        print(dump_string)

    return dump_string + '\n'


if __name__ == '__main__':
    print(dump_class_recursively(True))
