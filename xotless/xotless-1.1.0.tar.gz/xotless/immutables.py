#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from typing import Type

import immutables
from collections.abc import Mapping
from functools import partial

from .pickablenv import PickableRecordset

# I won't depend on Odoo, but if it installed ImmutableWrapper will be
# intelligent about it.
try:
    from odoo import models

    BaseModel: Type = models.BaseModel
except ImportError:

    class BaseModel:  # type: ignore
        pass


class ImmutableWrapper:
    """Wraps a `target` object so that it can be used immutably.

    Some external objects (most likely Odoo recordsets) are used within the
    pricing programs immutably but *copies* of such objects are created (e.g
    by splitters) while updating or changing some of its attributes.

    Example usage:

    .. code-block:: python

       >>> Commodity = self.env['operation.commodity']                         # doctest: +SKIP
       >>> target = Commodity.search([('start_date', '!=', False)], limit=1)   # doctest: +SKIP

       >>> wrapped = ImmutableWrapper(target)                                  # doctest: +SKIP
       >>> new = wrapped.replace(start_date=target.start_date + timedelta(1),  # doctest: +SKIP
       ...                       duration=timedelta(1))

       >>> assert new.start_date == target.start_date + timedelta(1)           # doctest: +SKIP

    Immutable wrappers are always flattened.  If the `target` object is
    another instance of ImmutableWrapper, we extracts its enclosed object and
    "inherit" the overrides:

    .. code-block:: python

       >>> class new:
       ...     pass

       >>> target = new()
       >>> wrapper = ImmutableWrapper(target, overrides=dict(a="a", c="c"))
       >>> wrapper2 = ImmutableWrapper(wrapper, overrides=dict(b="b"))

       >>> wrapper2._ImmutableWrapper__target is target
       True

       >>> wrapper2.a, wrapper2.b, wrapper2.c
       ('a', 'b', 'c')

    Trying to mutate an attribute raises a TypeError:

    .. code-block:: python

       >>> wrapper2.a = 1
       Traceback (most recent call last):
       ...
       TypeError: Cannot mutate an immutable wrapped object...

    """

    def __new__(self, target, *, overrides=None, wrap_callables=False):
        if overrides is None:
            overrides = {}
        if isinstance(target, PickableRecordset):
            target = target.instance
        if isinstance(target, ImmutableWrapper):
            attrs = dict(target.__overrides, **overrides)
            target = target.__target
        else:
            attrs = overrides
        result = super().__new__(self)
        # Avoid calling __setattr__ which would fail
        result.__dict__["_ImmutableWrapper__target"] = target
        result.__dict__["_ImmutableWrapper__overrides"] = immutables.Map(attrs)
        result.__dict__["_ImmutableWrapper__cache"] = {}
        result.__dict__["_ImmutableWrapper__wrap_callables"] = wrap_callables
        return result

    def __getattr__(self, attr):
        from xotl.tools.symbols import Unset

        res = self.__overrides.get(attr, Unset)
        if res is Unset:
            res = self.__cache.get(attr, Unset)
        if res is Unset:
            res = getattr(self.__target, attr)
        if (
            self.__wrap_callables
            and callable(res)
            and getattr(res, "__self__", None) is self.__target
        ):
            # If `res` a bound method of __target, extract the underlying
            # fuction so that `self` in the method is the ImmutableWrapper.
            res = partial(res.__func__, self)
        if isinstance(res, BaseModel):
            res = ImmutableWrapper(res, wrap_callables=self.__wrap_callables)
        self.__cache[attr] = res
        return res

    def __setattr__(self, attr, value):
        raise TypeError(
            "Cannot mutate an immutable wrapped object.  Use method 'replace'."
        )

    def replace(self, **attrs):
        """Return a new wrapper of the same object with updates.

        """
        overrides = dict(self.__overrides, **attrs)
        return ImmutableWrapper(
            self.__target,
            overrides=overrides,
            wrap_callables=self.__wrap_callables,
        )

    # IMPORTANT: The __cache can't be part of the hash nor of eq because is
    # just an optimization and not a part of the *identity* of the object.
    #
    # Also, there's a minor problem in __eq__ which allows to compare an
    # ImmutableWrapper with the underlying object; this means that instances
    # of ImmutableWrapper and the target object will hash differently despite
    # being equal.  This is only an issue if you mix ImmutableWrappers with
    # wrapped objects in the same collection (set, dict, etc...)
    def __hash__(self):
        return hash((self.__target, self.__overrides))

    def __eq__(self, other):
        if isinstance(other, ImmutableWrapper):
            return (
                self.__target == other.__target
                and self.__overrides == other.__overrides
            )
        elif isinstance(other, type(self.__target)):
            # We allow for a wrapper to be equal to its underlying target
            # object, but only if there are no overrides.
            return self.__target == other and not self.__overrides
        else:
            return NotImplemented

    def __repr__(self):
        return (
            f"<ImmutableWrapper of '{self.__target!r}' with {self.__overrides}; "
            f"cache: {self.__cache}; wrap_callables: {self.__wrap_callables}>"
        )

    def __getnewargs__(self):
        if isinstance(self.__target, BaseModel):
            return (PickableRecordset.from_recordset(self.__target),)
        else:
            return (self.__target,)

    def __getstate__(self):
        cache = self.__cache
        overrides = self.__overrides
        return (overrides, cache)

    def __setstate__(self, state):
        overrides, cache = state
        self.__dict__["_ImmutableWrapper__overrides"] = overrides
        self.__dict__["_ImmutableWrapper__cache"] = cache


class ImmutableChainMap(Mapping):  # noqa
    def __init__(self, *maps):
        self.maps = maps
        self._cache = None

    def _fill_cache(self):
        if self._cache is None:
            self._cache = cache = {}
            for mapping in reversed(self.maps):
                cache.update(mapping)

    def __hash__(self):
        return hash(tuple(hash(mapping) for mapping in self.maps))

    def __eq__(self, other):
        if isinstance(other, ImmutableChainMap):
            other._fill_cache()
            self._fill_cache()
            return self._cache == other._cache
        else:
            return NotImplemented

    def __getitem__(self, key):
        self._fill_cache()
        return self._cache[key]

    def __len__(self):
        self._fill_cache()
        return len(self._cache)

    def __iter__(self):
        self._fill_cache()
        return iter(self._cache)

    def __getstate__(self):
        return self.maps

    def __setstate__(self, state):
        self.__init__(*state)
