# coding: utf-8

"""
    TrueLayer Resource API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1.0
    Contact: rienafairefr@gmail.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

import marshmallow
from marshmallow import Schema, validates, ValidationError, post_load, missing

from truelayer import fields
from truelayer.configuration import Configuration



class MeSchema(Schema):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    client_id = marshmallow.fields.String()

    credentials_id = marshmallow.fields.String()

    provider = fields.Nested('ProviderInfo')('ProviderInfoSchema', )

    provider_id = marshmallow.fields.String()

    @validates("client_id")
    def validates_client_id(self, client_id):
        pass

    @validates("credentials_id")
    def validates_credentials_id(self, credentials_id):
        pass

    @validates("provider")
    def validates_provider(self, provider):
        pass

    @validates("provider_id")
    def validates_provider_id(self, provider_id):
        pass

    @post_load
    def post_load(self, data, **kwargs):
        config = Configuration()
        config.client_side_validation = False
        return Me(local_vars_configuration=config, **data)


class Me(object):
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
        'client_id': 'str',
        'credentials_id': 'str',
        'provider': 'ProviderInfo',
        'provider_id': 'str'
    }

    attribute_map = {
        'client_id': 'client_id',
        'credentials_id': 'credentials_id',
        'provider': 'provider',
        'provider_id': 'provider_id'
    }

    def __init__(self, client_id=missing, credentials_id=missing, provider=missing, provider_id=missing, local_vars_configuration=None):  # noqa: E501
        """Me - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self.discriminator = None
        if self.local_vars_configuration.client_side_validation:
            validated = MeSchema().load({
                'client_id': client_id,
                'credentials_id': credentials_id,
                'provider': provider,
                'provider_id': provider_id
            })
            self.client_id = validated.client_id
            self.credentials_id = validated.credentials_id
            self.provider = validated.provider
            self.provider_id = validated.provider_id
        else:
            self.client_id = client_id
            self.credentials_id = credentials_id
            self.provider = provider
            self.provider_id = provider_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        return MeSchema().dump(self)

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Me):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Me):
            return True

        return self.to_dict() != other.to_dict()
