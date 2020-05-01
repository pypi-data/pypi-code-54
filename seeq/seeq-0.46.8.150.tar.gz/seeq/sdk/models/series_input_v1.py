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


class SeriesInputV1(object):
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
        'additional_properties': 'list[ScalarPropertyV1]',
        'data_id': 'str',
        'data_version_check': 'str',
        'datasource_class': 'str',
        'datasource_id': 'str',
        'description': 'str',
        'formula': 'str',
        'host_id': 'str',
        'interpolation_method': 'str',
        'key_unit_of_measure': 'str',
        'maximum_interpolation': 'str',
        'name': 'str',
        'parameters': 'list[str]',
        'properties': 'list[ScalarPropertyV1]',
        'scoped_to': 'str',
        'security_string': 'str',
        'source_security_string': 'str',
        'sync_token': 'str',
        'value_unit_of_measure': 'str'
    }

    attribute_map = {
        'additional_properties': 'additionalProperties',
        'data_id': 'dataId',
        'data_version_check': 'dataVersionCheck',
        'datasource_class': 'datasourceClass',
        'datasource_id': 'datasourceId',
        'description': 'description',
        'formula': 'formula',
        'host_id': 'hostId',
        'interpolation_method': 'interpolationMethod',
        'key_unit_of_measure': 'keyUnitOfMeasure',
        'maximum_interpolation': 'maximumInterpolation',
        'name': 'name',
        'parameters': 'parameters',
        'properties': 'properties',
        'scoped_to': 'scopedTo',
        'security_string': 'securityString',
        'source_security_string': 'sourceSecurityString',
        'sync_token': 'syncToken',
        'value_unit_of_measure': 'valueUnitOfMeasure'
    }

    def __init__(self, additional_properties=None, data_id=None, data_version_check=None, datasource_class=None, datasource_id=None, description=None, formula=None, host_id=None, interpolation_method=None, key_unit_of_measure=None, maximum_interpolation=None, name=None, parameters=None, properties=None, scoped_to=None, security_string=None, source_security_string=None, sync_token=None, value_unit_of_measure=None):
        """
        SeriesInputV1 - a model defined in Swagger
        """

        self._additional_properties = None
        self._data_id = None
        self._data_version_check = None
        self._datasource_class = None
        self._datasource_id = None
        self._description = None
        self._formula = None
        self._host_id = None
        self._interpolation_method = None
        self._key_unit_of_measure = None
        self._maximum_interpolation = None
        self._name = None
        self._parameters = None
        self._properties = None
        self._scoped_to = None
        self._security_string = None
        self._source_security_string = None
        self._sync_token = None
        self._value_unit_of_measure = None

        if additional_properties is not None:
          self.additional_properties = additional_properties
        if data_id is not None:
          self.data_id = data_id
        if data_version_check is not None:
          self.data_version_check = data_version_check
        if datasource_class is not None:
          self.datasource_class = datasource_class
        if datasource_id is not None:
          self.datasource_id = datasource_id
        if description is not None:
          self.description = description
        if formula is not None:
          self.formula = formula
        if host_id is not None:
          self.host_id = host_id
        if interpolation_method is not None:
          self.interpolation_method = interpolation_method
        if key_unit_of_measure is not None:
          self.key_unit_of_measure = key_unit_of_measure
        if maximum_interpolation is not None:
          self.maximum_interpolation = maximum_interpolation
        if name is not None:
          self.name = name
        if parameters is not None:
          self.parameters = parameters
        if properties is not None:
          self.properties = properties
        if scoped_to is not None:
          self.scoped_to = scoped_to
        if security_string is not None:
          self.security_string = security_string
        if source_security_string is not None:
          self.source_security_string = source_security_string
        if sync_token is not None:
          self.sync_token = sync_token
        if value_unit_of_measure is not None:
          self.value_unit_of_measure = value_unit_of_measure

    @property
    def additional_properties(self):
        """
        Gets the additional_properties of this SeriesInputV1.
        Additional properties to set on this item. A property consists of aname, a value, and a unit of measure.

        :return: The additional_properties of this SeriesInputV1.
        :rtype: list[ScalarPropertyV1]
        """
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, additional_properties):
        """
        Sets the additional_properties of this SeriesInputV1.
        Additional properties to set on this item. A property consists of aname, a value, and a unit of measure.

        :param additional_properties: The additional_properties of this SeriesInputV1.
        :type: list[ScalarPropertyV1]
        """

        self._additional_properties = additional_properties

    @property
    def data_id(self):
        """
        Gets the data_id of this SeriesInputV1.
        The data ID of this item. Note: This is not the Seeq ID, but the unique identifier that the remote datasource uses.

        :return: The data_id of this SeriesInputV1.
        :rtype: str
        """
        return self._data_id

    @data_id.setter
    def data_id(self, data_id):
        """
        Sets the data_id of this SeriesInputV1.
        The data ID of this item. Note: This is not the Seeq ID, but the unique identifier that the remote datasource uses.

        :param data_id: The data_id of this SeriesInputV1.
        :type: str
        """

        self._data_id = data_id

    @property
    def data_version_check(self):
        """
        Gets the data_version_check of this SeriesInputV1.
        The data version check string. When updating an existing series, if the data version check string is unchanged, then the update will be skipped.

        :return: The data_version_check of this SeriesInputV1.
        :rtype: str
        """
        return self._data_version_check

    @data_version_check.setter
    def data_version_check(self, data_version_check):
        """
        Sets the data_version_check of this SeriesInputV1.
        The data version check string. When updating an existing series, if the data version check string is unchanged, then the update will be skipped.

        :param data_version_check: The data_version_check of this SeriesInputV1.
        :type: str
        """

        self._data_version_check = data_version_check

    @property
    def datasource_class(self):
        """
        Gets the datasource_class of this SeriesInputV1.
        Along with the Datasource ID, the Datasource Class uniquely identifies a datasource. For example, a datasource may be a particular instance of an OSIsoft PI historian.

        :return: The datasource_class of this SeriesInputV1.
        :rtype: str
        """
        return self._datasource_class

    @datasource_class.setter
    def datasource_class(self, datasource_class):
        """
        Sets the datasource_class of this SeriesInputV1.
        Along with the Datasource ID, the Datasource Class uniquely identifies a datasource. For example, a datasource may be a particular instance of an OSIsoft PI historian.

        :param datasource_class: The datasource_class of this SeriesInputV1.
        :type: str
        """

        self._datasource_class = datasource_class

    @property
    def datasource_id(self):
        """
        Gets the datasource_id of this SeriesInputV1.
        Along with the Datasource Class, the Datasource ID uniquely identifies a datasource. For example, a datasource may be a particular instance of an OSIsoft PI historian.

        :return: The datasource_id of this SeriesInputV1.
        :rtype: str
        """
        return self._datasource_id

    @datasource_id.setter
    def datasource_id(self, datasource_id):
        """
        Sets the datasource_id of this SeriesInputV1.
        Along with the Datasource Class, the Datasource ID uniquely identifies a datasource. For example, a datasource may be a particular instance of an OSIsoft PI historian.

        :param datasource_id: The datasource_id of this SeriesInputV1.
        :type: str
        """

        self._datasource_id = datasource_id

    @property
    def description(self):
        """
        Gets the description of this SeriesInputV1.
        Clarifying information or other plain language description of this asset. An input of just whitespace is equivalent to a null input.

        :return: The description of this SeriesInputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this SeriesInputV1.
        Clarifying information or other plain language description of this asset. An input of just whitespace is equivalent to a null input.

        :param description: The description of this SeriesInputV1.
        :type: str
        """

        self._description = description

    @property
    def formula(self):
        """
        Gets the formula of this SeriesInputV1.
        Information about the formula used to create a calculated item

        :return: The formula of this SeriesInputV1.
        :rtype: str
        """
        return self._formula

    @formula.setter
    def formula(self, formula):
        """
        Sets the formula of this SeriesInputV1.
        Information about the formula used to create a calculated item

        :param formula: The formula of this SeriesInputV1.
        :type: str
        """

        self._formula = formula

    @property
    def host_id(self):
        """
        Gets the host_id of this SeriesInputV1.
        The ID of the datasource hosting this item. Note that this is a Seeq-generated ID, not the way that the datasource identifies itself.

        :return: The host_id of this SeriesInputV1.
        :rtype: str
        """
        return self._host_id

    @host_id.setter
    def host_id(self, host_id):
        """
        Sets the host_id of this SeriesInputV1.
        The ID of the datasource hosting this item. Note that this is a Seeq-generated ID, not the way that the datasource identifies itself.

        :param host_id: The host_id of this SeriesInputV1.
        :type: str
        """

        self._host_id = host_id

    @property
    def interpolation_method(self):
        """
        Gets the interpolation_method of this SeriesInputV1.
        The interpolation method used when resampling the series. The options are: linear, pilinear, and step.

        :return: The interpolation_method of this SeriesInputV1.
        :rtype: str
        """
        return self._interpolation_method

    @interpolation_method.setter
    def interpolation_method(self, interpolation_method):
        """
        Sets the interpolation_method of this SeriesInputV1.
        The interpolation method used when resampling the series. The options are: linear, pilinear, and step.

        :param interpolation_method: The interpolation_method of this SeriesInputV1.
        :type: str
        """

        self._interpolation_method = interpolation_method

    @property
    def key_unit_of_measure(self):
        """
        Gets the key_unit_of_measure of this SeriesInputV1.
        The unit of measure for the keys in a stored series. Note that the keys are assigned (rather than converted to) these units. Do not set for calculated series.  The units for calculated series are determined by the calculation.

        :return: The key_unit_of_measure of this SeriesInputV1.
        :rtype: str
        """
        return self._key_unit_of_measure

    @key_unit_of_measure.setter
    def key_unit_of_measure(self, key_unit_of_measure):
        """
        Sets the key_unit_of_measure of this SeriesInputV1.
        The unit of measure for the keys in a stored series. Note that the keys are assigned (rather than converted to) these units. Do not set for calculated series.  The units for calculated series are determined by the calculation.

        :param key_unit_of_measure: The key_unit_of_measure of this SeriesInputV1.
        :type: str
        """

        self._key_unit_of_measure = key_unit_of_measure

    @property
    def maximum_interpolation(self):
        """
        Gets the maximum_interpolation of this SeriesInputV1.
        The maximum gap that can exist between samples in the series. This setting affects interpolation behavior when the interpolation period is smaller than the maximum interpolation. If the interpolation period is smaller than the maximum interpolation, the following two statements describe the behavior. When the gap between samples is smaller than the maximum interpolation, the gap will be populated with interpolated samples at the rate specified by the interpolation period. When the gap is larger than the maximum interpolation, the gap will be populated with samples of invalid at the rate specified by the interpolation period. Example settings: 5h, 2min, 3 days, 4 years

        :return: The maximum_interpolation of this SeriesInputV1.
        :rtype: str
        """
        return self._maximum_interpolation

    @maximum_interpolation.setter
    def maximum_interpolation(self, maximum_interpolation):
        """
        Sets the maximum_interpolation of this SeriesInputV1.
        The maximum gap that can exist between samples in the series. This setting affects interpolation behavior when the interpolation period is smaller than the maximum interpolation. If the interpolation period is smaller than the maximum interpolation, the following two statements describe the behavior. When the gap between samples is smaller than the maximum interpolation, the gap will be populated with interpolated samples at the rate specified by the interpolation period. When the gap is larger than the maximum interpolation, the gap will be populated with samples of invalid at the rate specified by the interpolation period. Example settings: 5h, 2min, 3 days, 4 years

        :param maximum_interpolation: The maximum_interpolation of this SeriesInputV1.
        :type: str
        """

        self._maximum_interpolation = maximum_interpolation

    @property
    def name(self):
        """
        Gets the name of this SeriesInputV1.
        Human readable name. Null or whitespace names are not permitted.

        :return: The name of this SeriesInputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this SeriesInputV1.
        Human readable name. Null or whitespace names are not permitted.

        :param name: The name of this SeriesInputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def parameters(self):
        """
        Gets the parameters of this SeriesInputV1.
        The parameters for the formula used to create a calculated item. Each parameter should have a format of 'name=id' where 'name' is the variable identifier, without the leading $ sign, and 'id' is the ID of the item referenced by the variable

        :return: The parameters of this SeriesInputV1.
        :rtype: list[str]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this SeriesInputV1.
        The parameters for the formula used to create a calculated item. Each parameter should have a format of 'name=id' where 'name' is the variable identifier, without the leading $ sign, and 'id' is the ID of the item referenced by the variable

        :param parameters: The parameters of this SeriesInputV1.
        :type: list[str]
        """

        self._parameters = parameters

    @property
    def properties(self):
        """
        Gets the properties of this SeriesInputV1.

        :return: The properties of this SeriesInputV1.
        :rtype: list[ScalarPropertyV1]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this SeriesInputV1.

        :param properties: The properties of this SeriesInputV1.
        :type: list[ScalarPropertyV1]
        """

        self._properties = properties

    @property
    def scoped_to(self):
        """
        Gets the scoped_to of this SeriesInputV1.
        The ID of the workbook to which this item will be scoped.

        :return: The scoped_to of this SeriesInputV1.
        :rtype: str
        """
        return self._scoped_to

    @scoped_to.setter
    def scoped_to(self, scoped_to):
        """
        Sets the scoped_to of this SeriesInputV1.
        The ID of the workbook to which this item will be scoped.

        :param scoped_to: The scoped_to of this SeriesInputV1.
        :type: str
        """

        self._scoped_to = scoped_to

    @property
    def security_string(self):
        """
        Gets the security_string of this SeriesInputV1.
        Security string containing all identities and their permissions for the item. If set, permissions can only be managed by the connector and not in Seeq.

        :return: The security_string of this SeriesInputV1.
        :rtype: str
        """
        return self._security_string

    @security_string.setter
    def security_string(self, security_string):
        """
        Sets the security_string of this SeriesInputV1.
        Security string containing all identities and their permissions for the item. If set, permissions can only be managed by the connector and not in Seeq.

        :param security_string: The security_string of this SeriesInputV1.
        :type: str
        """

        self._security_string = security_string

    @property
    def source_security_string(self):
        """
        Gets the source_security_string of this SeriesInputV1.
        The security string as it was originally found on the source (for debugging ACLs only)

        :return: The source_security_string of this SeriesInputV1.
        :rtype: str
        """
        return self._source_security_string

    @source_security_string.setter
    def source_security_string(self, source_security_string):
        """
        Sets the source_security_string of this SeriesInputV1.
        The security string as it was originally found on the source (for debugging ACLs only)

        :param source_security_string: The source_security_string of this SeriesInputV1.
        :type: str
        """

        self._source_security_string = source_security_string

    @property
    def sync_token(self):
        """
        Gets the sync_token of this SeriesInputV1.
        An arbitrary token (often a date or random ID) that is used during metadata syncs. At the end of a full sync, items with mismatching sync tokens are identified as stale and may be  archived using the Datasources clean-up API.

        :return: The sync_token of this SeriesInputV1.
        :rtype: str
        """
        return self._sync_token

    @sync_token.setter
    def sync_token(self, sync_token):
        """
        Sets the sync_token of this SeriesInputV1.
        An arbitrary token (often a date or random ID) that is used during metadata syncs. At the end of a full sync, items with mismatching sync tokens are identified as stale and may be  archived using the Datasources clean-up API.

        :param sync_token: The sync_token of this SeriesInputV1.
        :type: str
        """

        self._sync_token = sync_token

    @property
    def value_unit_of_measure(self):
        """
        Gets the value_unit_of_measure of this SeriesInputV1.
        The unit of measure for the values in a stored series. Note that the values are assigned (rather than converted to) these units. Do not set for calculated series.  The units for calculated series are determined by the calculation.

        :return: The value_unit_of_measure of this SeriesInputV1.
        :rtype: str
        """
        return self._value_unit_of_measure

    @value_unit_of_measure.setter
    def value_unit_of_measure(self, value_unit_of_measure):
        """
        Sets the value_unit_of_measure of this SeriesInputV1.
        The unit of measure for the values in a stored series. Note that the values are assigned (rather than converted to) these units. Do not set for calculated series.  The units for calculated series are determined by the calculation.

        :param value_unit_of_measure: The value_unit_of_measure of this SeriesInputV1.
        :type: str
        """

        self._value_unit_of_measure = value_unit_of_measure

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
        if not isinstance(other, SeriesInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
