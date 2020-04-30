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
    from onshape_client.oas.models import btm_database_parameter2229
except ImportError:
    btm_database_parameter2229 = sys.modules[
        "onshape_client.oas.models.btm_database_parameter2229"
    ]
try:
    from onshape_client.oas.models import btm_parameter_appearance627
except ImportError:
    btm_parameter_appearance627 = sys.modules[
        "onshape_client.oas.models.btm_parameter_appearance627"
    ]
try:
    from onshape_client.oas.models import btm_parameter_array2025
except ImportError:
    btm_parameter_array2025 = sys.modules[
        "onshape_client.oas.models.btm_parameter_array2025"
    ]
try:
    from onshape_client.oas.models import btm_parameter_blob_reference1679
except ImportError:
    btm_parameter_blob_reference1679 = sys.modules[
        "onshape_client.oas.models.btm_parameter_blob_reference1679"
    ]
try:
    from onshape_client.oas.models import btm_parameter_boolean144
except ImportError:
    btm_parameter_boolean144 = sys.modules[
        "onshape_client.oas.models.btm_parameter_boolean144"
    ]
try:
    from onshape_client.oas.models import btm_parameter_configured2222
except ImportError:
    btm_parameter_configured2222 = sys.modules[
        "onshape_client.oas.models.btm_parameter_configured2222"
    ]
try:
    from onshape_client.oas.models import btm_parameter_derived864
except ImportError:
    btm_parameter_derived864 = sys.modules[
        "onshape_client.oas.models.btm_parameter_derived864"
    ]
try:
    from onshape_client.oas.models import btm_parameter_enum145
except ImportError:
    btm_parameter_enum145 = sys.modules[
        "onshape_client.oas.models.btm_parameter_enum145"
    ]
try:
    from onshape_client.oas.models import btm_parameter_feature_list1749
except ImportError:
    btm_parameter_feature_list1749 = sys.modules[
        "onshape_client.oas.models.btm_parameter_feature_list1749"
    ]
try:
    from onshape_client.oas.models import btm_parameter_foreign_id146
except ImportError:
    btm_parameter_foreign_id146 = sys.modules[
        "onshape_client.oas.models.btm_parameter_foreign_id146"
    ]
try:
    from onshape_client.oas.models import btm_parameter_invalid1664
except ImportError:
    btm_parameter_invalid1664 = sys.modules[
        "onshape_client.oas.models.btm_parameter_invalid1664"
    ]
try:
    from onshape_client.oas.models import btm_parameter_lookup_table_path1419
except ImportError:
    btm_parameter_lookup_table_path1419 = sys.modules[
        "onshape_client.oas.models.btm_parameter_lookup_table_path1419"
    ]
try:
    from onshape_client.oas.models import btm_parameter_material1388
except ImportError:
    btm_parameter_material1388 = sys.modules[
        "onshape_client.oas.models.btm_parameter_material1388"
    ]
try:
    from onshape_client.oas.models import btm_parameter_quantity147
except ImportError:
    btm_parameter_quantity147 = sys.modules[
        "onshape_client.oas.models.btm_parameter_quantity147"
    ]
try:
    from onshape_client.oas.models import btm_parameter_query_list148
except ImportError:
    btm_parameter_query_list148 = sys.modules[
        "onshape_client.oas.models.btm_parameter_query_list148"
    ]
try:
    from onshape_client.oas.models import btm_parameter_query_with_occurrence_list67
except ImportError:
    btm_parameter_query_with_occurrence_list67 = sys.modules[
        "onshape_client.oas.models.btm_parameter_query_with_occurrence_list67"
    ]
try:
    from onshape_client.oas.models import btm_parameter_reference2434
except ImportError:
    btm_parameter_reference2434 = sys.modules[
        "onshape_client.oas.models.btm_parameter_reference2434"
    ]
try:
    from onshape_client.oas.models import btm_parameter_string149
except ImportError:
    btm_parameter_string149 = sys.modules[
        "onshape_client.oas.models.btm_parameter_string149"
    ]


class BTMParameter1(ModelNormal):
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
            "bt_type": (str,),  # noqa: E501
            "import_microversion": (str,),  # noqa: E501
            "node_id": (str,),  # noqa: E501
            "parameter_id": (str,),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return {
            "bt_type": {
                "BTMParameterQuantity-147": btm_parameter_quantity147.BTMParameterQuantity147,
                "BTMParameterLookupTablePath-1419": btm_parameter_lookup_table_path1419.BTMParameterLookupTablePath1419,
                "BTMParameterMaterial-1388": btm_parameter_material1388.BTMParameterMaterial1388,
                "BTMParameterEnum-145": btm_parameter_enum145.BTMParameterEnum145,
                "BTMParameterDerived-864": btm_parameter_derived864.BTMParameterDerived864,
                "BTMParameterBoolean-144": btm_parameter_boolean144.BTMParameterBoolean144,
                "BTMParameterFeatureList-1749": btm_parameter_feature_list1749.BTMParameterFeatureList1749,
                "BTMParameterConfigured-2222": btm_parameter_configured2222.BTMParameterConfigured2222,
                "BTMParameterString-149": btm_parameter_string149.BTMParameterString149,
                "BTMDatabaseParameter-2229": btm_database_parameter2229.BTMDatabaseParameter2229,
                "BTMParameterReference-2434": btm_parameter_reference2434.BTMParameterReference2434,
                "BTMParameterForeignId-146": btm_parameter_foreign_id146.BTMParameterForeignId146,
                "BTMParameterQueryList-148": btm_parameter_query_list148.BTMParameterQueryList148,
                "BTMParameterBlobReference-1679": btm_parameter_blob_reference1679.BTMParameterBlobReference1679,
                "BTMParameterQueryWithOccurrenceList-67": btm_parameter_query_with_occurrence_list67.BTMParameterQueryWithOccurrenceList67,
                "BTMParameterArray-2025": btm_parameter_array2025.BTMParameterArray2025,
                "BTMParameterInvalid-1664": btm_parameter_invalid1664.BTMParameterInvalid1664,
                "BTMParameterAppearance-627": btm_parameter_appearance627.BTMParameterAppearance627,
            },
        }

    attribute_map = {
        "bt_type": "btType",  # noqa: E501
        "import_microversion": "importMicroversion",  # noqa: E501
        "node_id": "nodeId",  # noqa: E501
        "parameter_id": "parameterId",  # noqa: E501
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
        """btm_parameter1.BTMParameter1 - a model defined in OpenAPI

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
            import_microversion (str): [optional]  # noqa: E501
            node_id (str): [optional]  # noqa: E501
            parameter_id (str): [optional]  # noqa: E501
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
