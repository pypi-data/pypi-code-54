#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019-2020 Airinnova AB and the Model-Framework authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Author: Aaron Dettmann

"""
Model framework
===============

    |    Model     <---   ModelSpec
    |      |                 |
    |      |                 |
    |   Feature   (<---) FeatureSpec
    |      |
    |      |
    |  (Property)
"""

from collections import namedtuple, defaultdict
from uuid import uuid4

from schemadict import schemadict

from ._log import logger

PRIMITIVE_TYPES = (bool, int, float, str, dict, list, tuple)


def is_primitve_type(obj):
    return obj in PRIMITIVE_TYPES


class _BaseSpec:

    _ITEM_SPEC = namedtuple(
        'ItemSpec',
        [
            'spec',
            'singleton',
            'required',
            'doc',
        ]
    )

    def __init__(self):
        """
        Base class to store a collection of item specifications.

        The term 'item' may refer to a property (e.g. the number 5) if this
        class describes a feature, or it may also refer to a feature itself if
        this class describes a model.

        Attrs:
            :uid: (str) unique identifier
            :_specs: (dict) specifications (value) of items (key)
        """

        self.uid = str(uuid4())
        self._specs = {}

    def __repr__(self):
        return f"<Specification for {tuple(self._specs.keys())}>"

    def _add_item_spec(self, key, spec, *, singleton=True, required=False, doc=''):
        """
        Add a specification

        Args:
            :key: (str) name of item to specify
            :spec: (obj) specification
            :singleton: (bool) if True, make item singleton
            :required: (bool) if True, make item required
            :doc: (str) documentation

        Note:
            * When calling from subclass, add a user input check for 'spec'
        """

        for arg, arg_name in zip((key, doc), ('key', 'doc')):
            if not isinstance(key, str):
                raise TypeError(f"{arg_name!r} must be of type string")

        for arg, arg_name in zip((singleton, required), ('singleton', 'required')):
            if not isinstance(arg, bool):
                raise TypeError(f"{arg_name!r} must be of type boolean")

        if key in self._specs.keys():
            raise KeyError(f"specification {key!r} already defined")

        self._specs[key] = self._ITEM_SPEC(spec, singleton, required, doc)

    def _provide_user_class(self, base):
        """
        Return a user space class which subclasses from 'base'

        Args:
            :base: (obj) base class

        Returns:
            :UserSpace: (obj) user space class with specification reference
        """

        class UserSpace(base):
            _parent_specs = self._specs
            _parent_uid = self.uid

        return UserSpace

    def get_docs(self):
        """
        Return user documentation

        Returns:
            :docs: (dict) full documentation
        """

        docs = {}
        for item_key, item_spec in self._specs.items():
            subdocs = None
            if isinstance(getattr(item_spec, 'spec', None), _BaseSpec):
                subdocs = item_spec.spec.get_docs()

            docs[item_key] = {
                'main': self._specs[item_key].doc,
                'sub': subdocs,
            }

        return docs


class _UserSpaceBase:

    _parent_specs = None
    _parent_uid = None

    def __init__(self):
        """
        Base class for user space functionality
        """

        self.uid = str(uuid4())
        self._items = defaultdict(list)

    def from_dict(self, dictionary):
        for key, value in dictionary.items():
            # TODO: check key in specification
            if self._parent_specs[key].singleton:
                self.set(key, value)
            else:
                self.add(key, value)
        return self

    def set(self, key, value):
        self._raise_err_key_not_allowed(key)
        self._raise_err_incorrect_type(key, value)

        if not self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'set()' does not apply to {key!r}, try 'add()'")

        logger.debug(f"Set property {key!r} = {value!r}")
        self._items[key] = [value, ]

    def add(self, key, value):
        self._raise_err_key_not_allowed(key)
        self._raise_err_incorrect_type(key, value)

        if self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'add()' does not apply to {key!r}, try 'set()'")

        logger.debug(f"Add property {key!r} = {value!r} (num: {len(self._items[key])+1})")
        self._items[key].append(value)

    def add_many(self, key, values):
        # TODO: check: values --> list or tuple
        for value in values:
            self.add(key, value)

    def get(self, key):
        if self._parent_specs[key].singleton:
            return self._items[key][0]
        else:
            return self._items[key]

    def iter(self, key):

        if self._parent_specs[key].singleton:
            raise KeyError(f"Method 'iter()' not supported for item {key!r}, try 'get()'")

        yield from self._items[key]

    def len(self, key):
        return len(self._items[key])

    def _raise_err_key_not_allowed(self, key):
        if key not in self._parent_specs.keys():
            raise KeyError(f"Key {key!r} is not in specification")

    def _raise_err_incorrect_type(self, key, value):
        if isinstance(self._parent_specs[key].spec, dict):
            if not isinstance(value, dict):
                schemadict({'v': self._parent_specs[key].spec}).validate({'v': value})
            else:
                schemadict(self._parent_specs[key].spec).validate(value)
        elif not isinstance(value, self._parent_specs[key].spec):
            raise ValueError(f"Value of type {self._parent_specs[key].spec} expected, got {type(value)}")


class FeatureSpec(_BaseSpec):

    def add_prop_spec(self, key, schema, *, singleton=True, required=False, doc=''):
        """
        TODO
        """

        if not (is_primitve_type(schema) or isinstance(schema, dict)):
            raise TypeError(f"'schema' must be a primitive type or a schemadict")

        super()._add_item_spec(
            key,
            schema,
            singleton=singleton,
            required=required,
            doc=doc,
        )

    def provide_user_class(self):
        """
        TODO
        """

        return super()._provide_user_class(_FeatureUserSpace)


class _FeatureUserSpace(_UserSpaceBase):
    pass


class ModelSpec(_BaseSpec):

    def add_feature_spec(self, key, feature_spec, *, singleton=True, required=True, doc=''):

        if not isinstance(feature_spec, FeatureSpec):
            raise TypeError(f"'feature_spec' must be instance of 'FeatureSpec'")

        super()._add_item_spec(
            key,
            feature_spec,
            singleton=singleton,
            required=required,
            doc=doc
        )

    def provide_user_class(self):
        """
        Return a 'Model' class with user and user methods
        """

        return super()._provide_user_class(_ModelUserSpace)


class _ModelUserSpace(_UserSpaceBase):

    def from_dict(self, dictionary):
        for key, feature_dict in dictionary.items():
            # TODO: check key in specification
            if self._parent_specs[key].singleton:
                feature = self.set_feature(key)
            else:
                feature = self.add_feature(key)
            feature.from_dict(feature_dict)
        return self

    def set(self, key, _):
        return NotImplementedError

    def add(self, key, _):
        return NotImplementedError

    def set_feature(self, key):
        """
        Make a singleton feature

        Args:
            :key: (str) name of the feature

        Returns:
            :feature: (obj) feature instance
        """

        # TODO: check: 'key' is string
        # TODO: check: feature exists in specification...

        if not self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'set_feature()' does not apply to {key!r}, try 'add_feature()'")

        logger.debug(f"Set feature {key!r}")
        f_instance = self._parent_specs[key].spec.provide_user_class()()
        self._items[key] = [f_instance, ]  # Store instance as list of length 1
        return f_instance

    def add_feature(self, key):
        """
        Add a non-singleton feature

        Args:
            :key: (str) name of the feature

        Returns:
            :feature: (obj) feature instance
        """

        # TODO: check: 'key' is string
        # TODO: check: feature exists in specification...

        if self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'add_feature()' does not apply to {key!r}, try 'set_feature()'")

        logger.debug(f"Add feature {key!r} (num: {len(self._items[key]) + 1})")
        f_instance = self._parent_specs[key].spec.provide_user_class()()
        self._items[key].append(f_instance)
        return f_instance
