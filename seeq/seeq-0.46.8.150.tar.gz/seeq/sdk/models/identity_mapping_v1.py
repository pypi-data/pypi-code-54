# coding: utf-8

"""
    Seeq REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 0.46.08-BETA
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class IdentityMappingV1(object):
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
        'mapped_identity_data_id': 'str',
        'provider_datasource_class': 'str',
        'provider_datasource_id': 'str'
    }

    attribute_map = {
        'mapped_identity_data_id': 'mappedIdentityDataId',
        'provider_datasource_class': 'providerDatasourceClass',
        'provider_datasource_id': 'providerDatasourceId'
    }

    def __init__(self, mapped_identity_data_id=None, provider_datasource_class=None, provider_datasource_id=None):
        """
        IdentityMappingV1 - a model defined in Swagger
        """

        self._mapped_identity_data_id = None
        self._provider_datasource_class = None
        self._provider_datasource_id = None

        if mapped_identity_data_id is not None:
          self.mapped_identity_data_id = mapped_identity_data_id
        if provider_datasource_class is not None:
          self.provider_datasource_class = provider_datasource_class
        if provider_datasource_id is not None:
          self.provider_datasource_id = provider_datasource_id

    @property
    def mapped_identity_data_id(self):
        """
        Gets the mapped_identity_data_id of this IdentityMappingV1.
        A unique identifier for the identity within its datasource.

        :return: The mapped_identity_data_id of this IdentityMappingV1.
        :rtype: str
        """
        return self._mapped_identity_data_id

    @mapped_identity_data_id.setter
    def mapped_identity_data_id(self, mapped_identity_data_id):
        """
        Sets the mapped_identity_data_id of this IdentityMappingV1.
        A unique identifier for the identity within its datasource.

        :param mapped_identity_data_id: The mapped_identity_data_id of this IdentityMappingV1.
        :type: str
        """

        self._mapped_identity_data_id = mapped_identity_data_id

    @property
    def provider_datasource_class(self):
        """
        Gets the provider_datasource_class of this IdentityMappingV1.
        Along with the Provider Datasource ID, the Provider Datasource Class uniquely identifies the datasource who provides the mapped user group. For example, a datasource may be a particular instance of an AD.

        :return: The provider_datasource_class of this IdentityMappingV1.
        :rtype: str
        """
        return self._provider_datasource_class

    @provider_datasource_class.setter
    def provider_datasource_class(self, provider_datasource_class):
        """
        Sets the provider_datasource_class of this IdentityMappingV1.
        Along with the Provider Datasource ID, the Provider Datasource Class uniquely identifies the datasource who provides the mapped user group. For example, a datasource may be a particular instance of an AD.

        :param provider_datasource_class: The provider_datasource_class of this IdentityMappingV1.
        :type: str
        """

        self._provider_datasource_class = provider_datasource_class

    @property
    def provider_datasource_id(self):
        """
        Gets the provider_datasource_id of this IdentityMappingV1.
        Along with the Provider Datasource Class, the Provider Datasource ID uniquely identifies the datasource who provides the mapped user group. For example, a datasource may be a particular instance of an AD.

        :return: The provider_datasource_id of this IdentityMappingV1.
        :rtype: str
        """
        return self._provider_datasource_id

    @provider_datasource_id.setter
    def provider_datasource_id(self, provider_datasource_id):
        """
        Sets the provider_datasource_id of this IdentityMappingV1.
        Along with the Provider Datasource Class, the Provider Datasource ID uniquely identifies the datasource who provides the mapped user group. For example, a datasource may be a particular instance of an AD.

        :param provider_datasource_id: The provider_datasource_id of this IdentityMappingV1.
        :type: str
        """

        self._provider_datasource_id = provider_datasource_id

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
        if not isinstance(other, IdentityMappingV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
