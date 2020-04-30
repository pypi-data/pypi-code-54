# coding: utf-8

"""
    Onshape REST API

    The Onshape REST API consumed by all clients.  # noqa: E501

    The version of the OpenAPI document: 1.113
    Contact: api-support@onshape.zendesk.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import
import re  # noqa: F401
import sys  # noqa: F401

import six  # noqa: F401
import nulltype  # noqa: F401

from onshape_client.oas.model_utils import (  # noqa: F401
    ModelComposed,
    ModelNormal,
    ModelSimple,
    date,
    datetime,
    file_type,
    int,
    none_type,
    str,
    validate_get_composed_info,
)

try:
    from onshape_client.oas.models import customer
except ImportError:
    customer = sys.modules["onshape_client.oas.models.customer"]
try:
    from onshape_client.oas.models import discount
except ImportError:
    discount = sys.modules["onshape_client.oas.models.discount"]
try:
    from onshape_client.oas.models import plan
except ImportError:
    plan = sys.modules["onshape_client.oas.models.plan"]
try:
    from onshape_client.oas.models import subscription_item_collection
except ImportError:
    subscription_item_collection = sys.modules[
        "onshape_client.oas.models.subscription_item_collection"
    ]


class Subscription(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {}

    validations = {}

    additional_properties_type = None

    @staticmethod
    def openapi_types():
        """
        This must be a class method so a model may have properties that are
        of type self, this ensures that we don't create a cyclic import

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            "application_fee_percent": (float,),  # noqa: E501
            "billing": (str,),  # noqa: E501
            "cancel_at_period_end": (bool,),  # noqa: E501
            "canceled_at": (int,),  # noqa: E501
            "created": (int,),  # noqa: E501
            "current_period_end": (int,),  # noqa: E501
            "current_period_start": (int,),  # noqa: E501
            "customer": (str,),  # noqa: E501
            "customer_object": (customer.Customer,),  # noqa: E501
            "days_until_due": (int,),  # noqa: E501
            "discount": (discount.Discount,),  # noqa: E501
            "ended_at": (int,),  # noqa: E501
            "id": (str,),  # noqa: E501
            "metadata": ({str: (str,)},),  # noqa: E501
            "object": (str,),  # noqa: E501
            "plan": (plan.Plan,),  # noqa: E501
            "quantity": (int,),  # noqa: E501
            "start": (int,),  # noqa: E501
            "status": (str,),  # noqa: E501
            "subscription_items": (
                subscription_item_collection.SubscriptionItemCollection,
            ),  # noqa: E501
            "tax_percent": (float,),  # noqa: E501
            "trial_end": (int,),  # noqa: E501
            "trial_start": (int,),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return None

    attribute_map = {
        "application_fee_percent": "applicationFeePercent",  # noqa: E501
        "billing": "billing",  # noqa: E501
        "cancel_at_period_end": "cancelAtPeriodEnd",  # noqa: E501
        "canceled_at": "canceledAt",  # noqa: E501
        "created": "created",  # noqa: E501
        "current_period_end": "currentPeriodEnd",  # noqa: E501
        "current_period_start": "currentPeriodStart",  # noqa: E501
        "customer": "customer",  # noqa: E501
        "customer_object": "customerObject",  # noqa: E501
        "days_until_due": "daysUntilDue",  # noqa: E501
        "discount": "discount",  # noqa: E501
        "ended_at": "endedAt",  # noqa: E501
        "id": "id",  # noqa: E501
        "metadata": "metadata",  # noqa: E501
        "object": "object",  # noqa: E501
        "plan": "plan",  # noqa: E501
        "quantity": "quantity",  # noqa: E501
        "start": "start",  # noqa: E501
        "status": "status",  # noqa: E501
        "subscription_items": "subscriptionItems",  # noqa: E501
        "tax_percent": "taxPercent",  # noqa: E501
        "trial_end": "trialEnd",  # noqa: E501
        "trial_start": "trialStart",  # noqa: E501
    }

    @staticmethod
    def _composed_schemas():
        return None

    required_properties = set(
        [
            "_data_store",
            "_check_type",
            "_from_server",
            "_path_to_item",
            "_configuration",
        ]
    )

    def __init__(
        self,
        _check_type=True,
        _from_server=False,
        _path_to_item=(),
        _configuration=None,
        **kwargs
    ):  # noqa: E501
        """subscription.Subscription - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _from_server (bool): True if the data is from the server
                                False if the data is from the client (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            application_fee_percent (float): [optional]  # noqa: E501
            billing (str): [optional]  # noqa: E501
            cancel_at_period_end (bool): [optional]  # noqa: E501
            canceled_at (int): [optional]  # noqa: E501
            created (int): [optional]  # noqa: E501
            current_period_end (int): [optional]  # noqa: E501
            current_period_start (int): [optional]  # noqa: E501
            customer (str): [optional]  # noqa: E501
            customer_object (customer.Customer): [optional]  # noqa: E501
            days_until_due (int): [optional]  # noqa: E501
            discount (discount.Discount): [optional]  # noqa: E501
            ended_at (int): [optional]  # noqa: E501
            id (str): [optional]  # noqa: E501
            metadata ({str: (str,)}): [optional]  # noqa: E501
            object (str): [optional]  # noqa: E501
            plan (plan.Plan): [optional]  # noqa: E501
            quantity (int): [optional]  # noqa: E501
            start (int): [optional]  # noqa: E501
            status (str): [optional]  # noqa: E501
            subscription_items (subscription_item_collection.SubscriptionItemCollection): [optional]  # noqa: E501
            tax_percent (float): [optional]  # noqa: E501
            trial_end (int): [optional]  # noqa: E501
            trial_start (int): [optional]  # noqa: E501
        """

        self._data_store = {}
        self._check_type = _check_type
        self._from_server = _from_server
        self._path_to_item = _path_to_item
        self._configuration = _configuration

        for var_name, var_value in six.iteritems(kwargs):
            if (
                var_name not in self.attribute_map
                and self._configuration is not None
                and self._configuration.discard_unknown_keys
                and self.additional_properties_type is None
            ):
                # discard variable.
                continue
            setattr(self, var_name, var_value)
