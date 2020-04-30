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
    from onshape_client.oas.models import bt_configured_dimension_column_info2168
except ImportError:
    bt_configured_dimension_column_info2168 = sys.modules[
        "onshape_client.oas.models.bt_configured_dimension_column_info2168"
    ]
try:
    from onshape_client.oas.models import bt_configured_feature_column_info1014
except ImportError:
    bt_configured_feature_column_info1014 = sys.modules[
        "onshape_client.oas.models.bt_configured_feature_column_info1014"
    ]
try:
    from onshape_client.oas.models import bt_configured_parameter_column_info2900
except ImportError:
    bt_configured_parameter_column_info2900 = sys.modules[
        "onshape_client.oas.models.bt_configured_parameter_column_info2900"
    ]
try:
    from onshape_client.oas.models import bt_configured_suppression_column_info2498
except ImportError:
    bt_configured_suppression_column_info2498 = sys.modules[
        "onshape_client.oas.models.bt_configured_suppression_column_info2498"
    ]
try:
    from onshape_client.oas.models import bt_configured_values_column_info1025_all_of
except ImportError:
    bt_configured_values_column_info1025_all_of = sys.modules[
        "onshape_client.oas.models.bt_configured_values_column_info1025_all_of"
    ]
try:
    from onshape_client.oas.models import bt_table_column_info1222
except ImportError:
    bt_table_column_info1222 = sys.modules[
        "onshape_client.oas.models.bt_table_column_info1222"
    ]
try:
    from onshape_client.oas.models import bt_table_column_spec1967
except ImportError:
    bt_table_column_spec1967 = sys.modules[
        "onshape_client.oas.models.bt_table_column_spec1967"
    ]


class BTConfiguredValuesColumnInfo1025(ModelComposed):
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

    allowed_values = {
        ("parent_type",): {
            "FEATURE": "FEATURE",
            "INSTANCE": "INSTANCE",
            "MATE": "MATE",
            "MATE_CONNECTOR": "MATE_CONNECTOR",
            "UNKNOWN": "UNKNOWN",
        },
    }

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
            "bt_type": (str,),  # noqa: E501
            "parent_id": (str,),  # noqa: E501
            "parent_name": (str,),  # noqa: E501
            "parent_type": (str,),  # noqa: E501
            "id": (str,),  # noqa: E501
            "node_id": (str,),  # noqa: E501
            "specification": (
                bt_table_column_spec1967.BTTableColumnSpec1967,
            ),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return {
            "bt_type": {
                "BTConfiguredFeatureColumnInfo-1014": bt_configured_feature_column_info1014.BTConfiguredFeatureColumnInfo1014,
                "BTConfiguredDimensionColumnInfo-2168": bt_configured_dimension_column_info2168.BTConfiguredDimensionColumnInfo2168,
                "BTConfiguredSuppressionColumnInfo-2498": bt_configured_suppression_column_info2498.BTConfiguredSuppressionColumnInfo2498,
                "BTConfiguredParameterColumnInfo-2900": bt_configured_parameter_column_info2900.BTConfiguredParameterColumnInfo2900,
            },
        }

    attribute_map = {
        "bt_type": "btType",  # noqa: E501
        "parent_id": "parentId",  # noqa: E501
        "parent_name": "parentName",  # noqa: E501
        "parent_type": "parentType",  # noqa: E501
        "id": "id",  # noqa: E501
        "node_id": "nodeId",  # noqa: E501
        "specification": "specification",  # noqa: E501
    }

    required_properties = set(
        [
            "_data_store",
            "_check_type",
            "_from_server",
            "_path_to_item",
            "_configuration",
            "_composed_instances",
            "_var_name_to_model_instances",
            "_additional_properties_model_instances",
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
        """bt_configured_values_column_info1025.BTConfiguredValuesColumnInfo1025 - a model defined in OpenAPI

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
            bt_type (str): [optional]  # noqa: E501
            parent_id (str): [optional]  # noqa: E501
            parent_name (str): [optional]  # noqa: E501
            parent_type (str): [optional]  # noqa: E501
            id (str): [optional]  # noqa: E501
            node_id (str): [optional]  # noqa: E501
            specification (bt_table_column_spec1967.BTTableColumnSpec1967): [optional]  # noqa: E501
        """

        self._data_store = {}
        self._check_type = _check_type
        self._from_server = _from_server
        self._path_to_item = _path_to_item
        self._configuration = _configuration

        constant_args = {
            "_check_type": _check_type,
            "_path_to_item": _path_to_item,
            "_from_server": _from_server,
            "_configuration": _configuration,
        }
        required_args = {}
        # remove args whose value is Null because they are unset
        required_arg_names = list(required_args.keys())
        for required_arg_name in required_arg_names:
            if required_args[required_arg_name] is nulltype.Null:
                del required_args[required_arg_name]
        model_args = {}
        model_args.update(required_args)
        model_args.update(kwargs)
        composed_info = validate_get_composed_info(constant_args, model_args, self)
        self._composed_instances = composed_info[0]
        self._var_name_to_model_instances = composed_info[1]
        self._additional_properties_model_instances = composed_info[2]
        unused_args = composed_info[3]

        for var_name, var_value in required_args.items():
            setattr(self, var_name, var_value)
        for var_name, var_value in six.iteritems(kwargs):
            if (
                var_name in unused_args
                and self._configuration is not None
                and self._configuration.discard_unknown_keys
                and not self._additional_properties_model_instances
            ):
                # discard variable.
                continue
            setattr(self, var_name, var_value)

    @staticmethod
    def _composed_schemas():
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error beause the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        return {
            "anyOf": [],
            "allOf": [
                bt_configured_values_column_info1025_all_of.BTConfiguredValuesColumnInfo1025AllOf,
                bt_table_column_info1222.BTTableColumnInfo1222,
            ],
            "oneOf": [],
        }

    @classmethod
    def get_discriminator_class(cls, from_server, data):
        """Returns the child class specified by the discriminator"""
        discriminator = cls.discriminator()
        discr_propertyname_py = list(discriminator.keys())[0]
        discr_propertyname_js = cls.attribute_map[discr_propertyname_py]
        if from_server:
            class_name = data[discr_propertyname_js]
        else:
            class_name = data[discr_propertyname_py]
        class_name_to_discr_class = discriminator[discr_propertyname_py]
        return class_name_to_discr_class.get(class_name)
