#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Polyaxon SDKs and REST API specification.

    Polyaxon SDKs and REST API specification.  # noqa: E501

    The version of the OpenAPI document: 1.0.84
    Contact: contact@polyaxon.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from polyaxon_sdk.configuration import Configuration


class V1Component(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        "version": "float",
        "kind": "str",
        "name": "str",
        "tag": "str",
        "description": "str",
        "tags": "list[str]",
        "profile": "str",
        "queue": "str",
        "cache": "V1Cache",
        "termination": "V1Termination",
        "plugins": "V1Plugins",
        "inputs": "list[V1IO]",
        "outputs": "list[V1IO]",
        "run": "object",
    }

    attribute_map = {
        "version": "version",
        "kind": "kind",
        "name": "name",
        "tag": "tag",
        "description": "description",
        "tags": "tags",
        "profile": "profile",
        "queue": "queue",
        "cache": "cache",
        "termination": "termination",
        "plugins": "plugins",
        "inputs": "inputs",
        "outputs": "outputs",
        "run": "run",
    }

    def __init__(
        self,
        version=None,
        kind=None,
        name=None,
        tag=None,
        description=None,
        tags=None,
        profile=None,
        queue=None,
        cache=None,
        termination=None,
        plugins=None,
        inputs=None,
        outputs=None,
        run=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """V1Component - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._version = None
        self._kind = None
        self._name = None
        self._tag = None
        self._description = None
        self._tags = None
        self._profile = None
        self._queue = None
        self._cache = None
        self._termination = None
        self._plugins = None
        self._inputs = None
        self._outputs = None
        self._run = None
        self.discriminator = None

        if version is not None:
            self.version = version
        if kind is not None:
            self.kind = kind
        if name is not None:
            self.name = name
        if tag is not None:
            self.tag = tag
        if description is not None:
            self.description = description
        if tags is not None:
            self.tags = tags
        if profile is not None:
            self.profile = profile
        if queue is not None:
            self.queue = queue
        if cache is not None:
            self.cache = cache
        if termination is not None:
            self.termination = termination
        if plugins is not None:
            self.plugins = plugins
        if inputs is not None:
            self.inputs = inputs
        if outputs is not None:
            self.outputs = outputs
        if run is not None:
            self.run = run

    @property
    def version(self):
        """Gets the version of this V1Component.  # noqa: E501


        :return: The version of this V1Component.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this V1Component.


        :param version: The version of this V1Component.  # noqa: E501
        :type: float
        """

        self._version = version

    @property
    def kind(self):
        """Gets the kind of this V1Component.  # noqa: E501


        :return: The kind of this V1Component.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this V1Component.


        :param kind: The kind of this V1Component.  # noqa: E501
        :type: str
        """

        self._kind = kind

    @property
    def name(self):
        """Gets the name of this V1Component.  # noqa: E501


        :return: The name of this V1Component.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1Component.


        :param name: The name of this V1Component.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def tag(self):
        """Gets the tag of this V1Component.  # noqa: E501


        :return: The tag of this V1Component.  # noqa: E501
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Sets the tag of this V1Component.


        :param tag: The tag of this V1Component.  # noqa: E501
        :type: str
        """

        self._tag = tag

    @property
    def description(self):
        """Gets the description of this V1Component.  # noqa: E501


        :return: The description of this V1Component.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this V1Component.


        :param description: The description of this V1Component.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def tags(self):
        """Gets the tags of this V1Component.  # noqa: E501


        :return: The tags of this V1Component.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this V1Component.


        :param tags: The tags of this V1Component.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def profile(self):
        """Gets the profile of this V1Component.  # noqa: E501


        :return: The profile of this V1Component.  # noqa: E501
        :rtype: str
        """
        return self._profile

    @profile.setter
    def profile(self, profile):
        """Sets the profile of this V1Component.


        :param profile: The profile of this V1Component.  # noqa: E501
        :type: str
        """

        self._profile = profile

    @property
    def queue(self):
        """Gets the queue of this V1Component.  # noqa: E501


        :return: The queue of this V1Component.  # noqa: E501
        :rtype: str
        """
        return self._queue

    @queue.setter
    def queue(self, queue):
        """Sets the queue of this V1Component.


        :param queue: The queue of this V1Component.  # noqa: E501
        :type: str
        """

        self._queue = queue

    @property
    def cache(self):
        """Gets the cache of this V1Component.  # noqa: E501


        :return: The cache of this V1Component.  # noqa: E501
        :rtype: V1Cache
        """
        return self._cache

    @cache.setter
    def cache(self, cache):
        """Sets the cache of this V1Component.


        :param cache: The cache of this V1Component.  # noqa: E501
        :type: V1Cache
        """

        self._cache = cache

    @property
    def termination(self):
        """Gets the termination of this V1Component.  # noqa: E501


        :return: The termination of this V1Component.  # noqa: E501
        :rtype: V1Termination
        """
        return self._termination

    @termination.setter
    def termination(self, termination):
        """Sets the termination of this V1Component.


        :param termination: The termination of this V1Component.  # noqa: E501
        :type: V1Termination
        """

        self._termination = termination

    @property
    def plugins(self):
        """Gets the plugins of this V1Component.  # noqa: E501


        :return: The plugins of this V1Component.  # noqa: E501
        :rtype: V1Plugins
        """
        return self._plugins

    @plugins.setter
    def plugins(self, plugins):
        """Sets the plugins of this V1Component.


        :param plugins: The plugins of this V1Component.  # noqa: E501
        :type: V1Plugins
        """

        self._plugins = plugins

    @property
    def inputs(self):
        """Gets the inputs of this V1Component.  # noqa: E501


        :return: The inputs of this V1Component.  # noqa: E501
        :rtype: list[V1IO]
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this V1Component.


        :param inputs: The inputs of this V1Component.  # noqa: E501
        :type: list[V1IO]
        """

        self._inputs = inputs

    @property
    def outputs(self):
        """Gets the outputs of this V1Component.  # noqa: E501


        :return: The outputs of this V1Component.  # noqa: E501
        :rtype: list[V1IO]
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        """Sets the outputs of this V1Component.


        :param outputs: The outputs of this V1Component.  # noqa: E501
        :type: list[V1IO]
        """

        self._outputs = outputs

    @property
    def run(self):
        """Gets the run of this V1Component.  # noqa: E501


        :return: The run of this V1Component.  # noqa: E501
        :rtype: object
        """
        return self._run

    @run.setter
    def run(self, run):
        """Sets the run of this V1Component.


        :param run: The run of this V1Component.  # noqa: E501
        :type: object
        """

        self._run = run

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1Component):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1Component):
            return True

        return self.to_dict() != other.to_dict()
