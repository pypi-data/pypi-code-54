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
    from onshape_client.oas.models import btm_parameter1
except ImportError:
    btm_parameter1 = sys.modules["onshape_client.oas.models.btm_parameter1"]


class BTMSketchConstraint2(ModelNormal):
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
        ("constraint_type",): {
            "NONE": "NONE",
            "COINCIDENT": "COINCIDENT",
            "PARALLEL": "PARALLEL",
            "VERTICAL": "VERTICAL",
            "HORIZONTAL": "HORIZONTAL",
            "PERPENDICULAR": "PERPENDICULAR",
            "CONCENTRIC": "CONCENTRIC",
            "MIRROR": "MIRROR",
            "MIDPOINT": "MIDPOINT",
            "TANGENT": "TANGENT",
            "EQUAL": "EQUAL",
            "LENGTH": "LENGTH",
            "DISTANCE": "DISTANCE",
            "ANGLE": "ANGLE",
            "RADIUS": "RADIUS",
            "NORMAL": "NORMAL",
            "FIX": "FIX",
            "PROJECTED": "PROJECTED",
            "OFFSET": "OFFSET",
            "CIRCULAR_PATTERN": "CIRCULAR_PATTERN",
            "PIERCE": "PIERCE",
            "LINEAR_PATTERN": "LINEAR_PATTERN",
            "MAJOR_DIAMETER": "MAJOR_DIAMETER",
            "MINOR_DIAMETER": "MINOR_DIAMETER",
            "QUADRANT": "QUADRANT",
            "DIAMETER": "DIAMETER",
            "SILHOUETTED": "SILHOUETTED",
            "CENTERLINE_DIMENSION": "CENTERLINE_DIMENSION",
            "INTERSECTED": "INTERSECTED",
            "RHO": "RHO",
            "EQUAL_CURVATURE": "EQUAL_CURVATURE",
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
            "constraint_type": (str,),  # noqa: E501
            "driven_dimension": (bool,),  # noqa: E501
            "entity_id": (str,),  # noqa: E501
            "entity_id_and_replace_in_dependent_fields": (str,),  # noqa: E501
            "has_offset_data1": (bool,),  # noqa: E501
            "has_offset_data2": (bool,),  # noqa: E501
            "has_pierce_parameter": (bool,),  # noqa: E501
            "help_parameters": ([float],),  # noqa: E501
            "import_microversion": (str,),  # noqa: E501
            "namespace": (str,),  # noqa: E501
            "node_id": (str,),  # noqa: E501
            "offset_distance1": (float,),  # noqa: E501
            "offset_distance2": (float,),  # noqa: E501
            "offset_orientation1": (bool,),  # noqa: E501
            "offset_orientation2": (bool,),  # noqa: E501
            "parameters": ([btm_parameter1.BTMParameter1],),  # noqa: E501
            "pierce_parameter": (float,),  # noqa: E501
        }

    @staticmethod
    def discriminator():
        return None

    attribute_map = {
        "bt_type": "btType",  # noqa: E501
        "constraint_type": "constraintType",  # noqa: E501
        "driven_dimension": "drivenDimension",  # noqa: E501
        "entity_id": "entityId",  # noqa: E501
        "entity_id_and_replace_in_dependent_fields": "entityIdAndReplaceInDependentFields",  # noqa: E501
        "has_offset_data1": "hasOffsetData1",  # noqa: E501
        "has_offset_data2": "hasOffsetData2",  # noqa: E501
        "has_pierce_parameter": "hasPierceParameter",  # noqa: E501
        "help_parameters": "helpParameters",  # noqa: E501
        "import_microversion": "importMicroversion",  # noqa: E501
        "namespace": "namespace",  # noqa: E501
        "node_id": "nodeId",  # noqa: E501
        "offset_distance1": "offsetDistance1",  # noqa: E501
        "offset_distance2": "offsetDistance2",  # noqa: E501
        "offset_orientation1": "offsetOrientation1",  # noqa: E501
        "offset_orientation2": "offsetOrientation2",  # noqa: E501
        "parameters": "parameters",  # noqa: E501
        "pierce_parameter": "pierceParameter",  # noqa: E501
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
        """btm_sketch_constraint2.BTMSketchConstraint2 - a model defined in OpenAPI

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
            constraint_type (str): [optional]  # noqa: E501
            driven_dimension (bool): [optional]  # noqa: E501
            entity_id (str): [optional]  # noqa: E501
            entity_id_and_replace_in_dependent_fields (str): [optional]  # noqa: E501
            has_offset_data1 (bool): [optional]  # noqa: E501
            has_offset_data2 (bool): [optional]  # noqa: E501
            has_pierce_parameter (bool): [optional]  # noqa: E501
            help_parameters ([float]): [optional]  # noqa: E501
            import_microversion (str): [optional]  # noqa: E501
            namespace (str): [optional]  # noqa: E501
            node_id (str): [optional]  # noqa: E501
            offset_distance1 (float): [optional]  # noqa: E501
            offset_distance2 (float): [optional]  # noqa: E501
            offset_orientation1 (bool): [optional]  # noqa: E501
            offset_orientation2 (bool): [optional]  # noqa: E501
            parameters ([btm_parameter1.BTMParameter1]): [optional]  # noqa: E501
            pierce_parameter (float): [optional]  # noqa: E501
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
