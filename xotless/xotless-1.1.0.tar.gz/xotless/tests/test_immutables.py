#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import doctest
import xotless.immutables
from xotless.immutables import ImmutableWrapper

from .support import captured_stdout, captured_stderr


def test_doctests():
    with captured_stdout() as stdout, captured_stderr() as stderr:
        failure_count, test_count = doctest.testmod(
            xotless.immutables,
            verbose=True,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            raise_on_error=False,
        )
    if test_count and failure_count:  # pragma: no cover
        print(stdout.getvalue())
        print(stderr.getvalue())
        raise AssertionError("ImmutableWrapper doctest failed")


def test_wrap_callable():
    class Bar:
        def return_self(self):
            return self

    class Foo(Bar):
        pass

    obj = Foo()
    wrapper = ImmutableWrapper(obj)
    assert wrapper.return_self() is obj

    wrapper2 = ImmutableWrapper(obj, wrap_callables=True)
    assert wrapper2.return_self() is wrapper2
