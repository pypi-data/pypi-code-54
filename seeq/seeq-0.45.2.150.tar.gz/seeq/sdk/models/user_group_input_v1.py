# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.45.02
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class UserGroupInputV1(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'description': 'str',
        'is_enabled': 'bool',
        'mapping': 'bool',
        'mappings': 'list[IdentityMappingV1]',
        'name': 'str',
        'sync_token': 'str'
    }

    attribute_map = {
        'description': 'description',
        'is_enabled': 'isEnabled',
        'mapping': 'mapping',
        'mappings': 'mappings',
        'name': 'name',
        'sync_token': 'syncToken'
    }

    def __init__(self, description=None, is_enabled=True, mapping=False, mappings=None, name=None, sync_token=None):
        """
        UserGroupInputV1 - a model defined in Swagger
        """

        self._description = None
        self._is_enabled = None
        self._mapping = None
        self._mappings = None
        self._name = None
        self._sync_token = None

        if description is not None:
          self.description = description
        if is_enabled is not None:
          self.is_enabled = is_enabled
        if mapping is not None:
          self.mapping = mapping
        if mappings is not None:
          self.mappings = mappings
        if name is not None:
          self.name = name
        if sync_token is not None:
          self.sync_token = sync_token

    @property
    def description(self):
        """
        Gets the description of this UserGroupInputV1.
        Clarifying information or other plain language description of this asset. An input of just whitespace is equivalent to a null input.

        :return: The description of this UserGroupInputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UserGroupInputV1.
        Clarifying information or other plain language description of this asset. An input of just whitespace is equivalent to a null input.

        :param description: The description of this UserGroupInputV1.
        :type: str
        """

        self._description = description

    @property
    def is_enabled(self):
        """
        Gets the is_enabled of this UserGroupInputV1.
        Whether the user group is enabled or disabled (default true).

        :return: The is_enabled of this UserGroupInputV1.
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """
        Sets the is_enabled of this UserGroupInputV1.
        Whether the user group is enabled or disabled (default true).

        :param is_enabled: The is_enabled of this UserGroupInputV1.
        :type: bool
        """

        self._is_enabled = is_enabled

    @property
    def mapping(self):
        """
        Gets the mapping of this UserGroupInputV1.

        :return: The mapping of this UserGroupInputV1.
        :rtype: bool
        """
        return self._mapping

    @mapping.setter
    def mapping(self, mapping):
        """
        Sets the mapping of this UserGroupInputV1.

        :param mapping: The mapping of this UserGroupInputV1.
        :type: bool
        """

        self._mapping = mapping

    @property
    def mappings(self):
        """
        Gets the mappings of this UserGroupInputV1.
        The mappings of the group

        :return: The mappings of this UserGroupInputV1.
        :rtype: list[IdentityMappingV1]
        """
        return self._mappings

    @mappings.setter
    def mappings(self, mappings):
        """
        Sets the mappings of this UserGroupInputV1.
        The mappings of the group

        :param mappings: The mappings of this UserGroupInputV1.
        :type: list[IdentityMappingV1]
        """

        self._mappings = mappings

    @property
    def name(self):
        """
        Gets the name of this UserGroupInputV1.
        Human readable name. Null or whitespace names are not permitted.

        :return: The name of this UserGroupInputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this UserGroupInputV1.
        Human readable name. Null or whitespace names are not permitted.

        :param name: The name of this UserGroupInputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def sync_token(self):
        """
        Gets the sync_token of this UserGroupInputV1.
        An arbitrary token (often a date or random ID) that is used during metadata syncs. At the end of a full sync, items with mismatching sync tokens are identified as stale and may be archived using the Datasources clean-up API.

        :return: The sync_token of this UserGroupInputV1.
        :rtype: str
        """
        return self._sync_token

    @sync_token.setter
    def sync_token(self, sync_token):
        """
        Sets the sync_token of this UserGroupInputV1.
        An arbitrary token (often a date or random ID) that is used during metadata syncs. At the end of a full sync, items with mismatching sync tokens are identified as stale and may be archived using the Datasources clean-up API.

        :param sync_token: The sync_token of this UserGroupInputV1.
        :type: str
        """

        self._sync_token = sync_token

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, UserGroupInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
