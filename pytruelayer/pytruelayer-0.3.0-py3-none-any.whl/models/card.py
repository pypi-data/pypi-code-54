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



class CardSchema(Schema):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    account_id = marshmallow.fields.String()

    card_network = marshmallow.fields.String()

    card_type = marshmallow.fields.String()

    currency = marshmallow.fields.String()

    display_name = marshmallow.fields.String()

    name_on_card = marshmallow.fields.String()

    partial_card_number = marshmallow.fields.String()

    provider = fields.Nested('ProviderInfo')('ProviderInfoSchema', )

    update_timestamp = fields.DateTime()

    valid_from = marshmallow.fields.String()

    valid_to = marshmallow.fields.String()

    @validates("account_id")
    def validates_account_id(self, account_id):
        pass

    @validates("card_network")
    def validates_card_network(self, card_network):
        pass

    @validates("card_type")
    def validates_card_type(self, card_type):
        pass

    @validates("currency")
    def validates_currency(self, currency):
        pass

    @validates("display_name")
    def validates_display_name(self, display_name):
        pass

    @validates("name_on_card")
    def validates_name_on_card(self, name_on_card):
        pass

    @validates("partial_card_number")
    def validates_partial_card_number(self, partial_card_number):
        pass

    @validates("provider")
    def validates_provider(self, provider):
        pass

    @validates("update_timestamp")
    def validates_update_timestamp(self, update_timestamp):
        pass

    @validates("valid_from")
    def validates_valid_from(self, valid_from):
        pass

    @validates("valid_to")
    def validates_valid_to(self, valid_to):
        pass

    @post_load
    def post_load(self, data, **kwargs):
        config = Configuration()
        config.client_side_validation = False
        return Card(local_vars_configuration=config, **data)


class Card(object):
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
        'account_id': 'str',
        'card_network': 'str',
        'card_type': 'str',
        'currency': 'str',
        'display_name': 'str',
        'name_on_card': 'str',
        'partial_card_number': 'str',
        'provider': 'ProviderInfo',
        'update_timestamp': 'datetime',
        'valid_from': 'str',
        'valid_to': 'str'
    }

    attribute_map = {
        'account_id': 'account_id',
        'card_network': 'card_network',
        'card_type': 'card_type',
        'currency': 'currency',
        'display_name': 'display_name',
        'name_on_card': 'name_on_card',
        'partial_card_number': 'partial_card_number',
        'provider': 'provider',
        'update_timestamp': 'update_timestamp',
        'valid_from': 'valid_from',
        'valid_to': 'valid_to'
    }

    def __init__(self, account_id=missing, card_network=missing, card_type=missing, currency=missing, display_name=missing, name_on_card=missing, partial_card_number=missing, provider=missing, update_timestamp=missing, valid_from=missing, valid_to=missing, local_vars_configuration=None):  # noqa: E501
        """Card - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self.discriminator = None
        if self.local_vars_configuration.client_side_validation:
            validated = CardSchema().load({
                'account_id': account_id,
                'card_network': card_network,
                'card_type': card_type,
                'currency': currency,
                'display_name': display_name,
                'name_on_card': name_on_card,
                'partial_card_number': partial_card_number,
                'provider': provider,
                'update_timestamp': update_timestamp,
                'valid_from': valid_from,
                'valid_to': valid_to
            })
            self.account_id = validated.account_id
            self.card_network = validated.card_network
            self.card_type = validated.card_type
            self.currency = validated.currency
            self.display_name = validated.display_name
            self.name_on_card = validated.name_on_card
            self.partial_card_number = validated.partial_card_number
            self.provider = validated.provider
            self.update_timestamp = validated.update_timestamp
            self.valid_from = validated.valid_from
            self.valid_to = validated.valid_to
        else:
            self.account_id = account_id
            self.card_network = card_network
            self.card_type = card_type
            self.currency = currency
            self.display_name = display_name
            self.name_on_card = name_on_card
            self.partial_card_number = partial_card_number
            self.provider = provider
            self.update_timestamp = update_timestamp
            self.valid_from = valid_from
            self.valid_to = valid_to

    def to_dict(self):
        """Returns the model properties as a dict"""
        return CardSchema().dump(self)

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Card):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Card):
            return True

        return self.to_dict() != other.to_dict()
