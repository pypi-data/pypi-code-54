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


class ThresholdMetricOutputV1(object):
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
        'aggregation_function': 'str',
        'bounding_condition': 'ItemPreviewWithAssetsV1',
        'bounding_condition_maximum_duration': 'ScalarValueOutputV1',
        'condition_thresholds': 'list[ThresholdOutputV1]',
        'data_id': 'str',
        'datasource_class': 'str',
        'datasource_id': 'str',
        'description': 'str',
        'display_item': 'ItemPreviewV1',
        'duration': 'ScalarValueOutputV1',
        'effective_permissions': 'PermissionsV1',
        'href': 'str',
        'id': 'str',
        'is_archived': 'bool',
        'is_redacted': 'bool',
        'measured_item': 'ItemPreviewWithAssetsV1',
        'measured_item_maximum_duration': 'ScalarValueOutputV1',
        'name': 'str',
        'number_format': 'str',
        'period': 'ScalarValueOutputV1',
        'process_type': 'str',
        'scoped_to': 'str',
        'status_message': 'str',
        'thresholds': 'list[ThresholdOutputV1]',
        'type': 'str',
        'value_unit_of_measure': 'str'
    }

    attribute_map = {
        'aggregation_function': 'aggregationFunction',
        'bounding_condition': 'boundingCondition',
        'bounding_condition_maximum_duration': 'boundingConditionMaximumDuration',
        'condition_thresholds': 'conditionThresholds',
        'data_id': 'dataId',
        'datasource_class': 'datasourceClass',
        'datasource_id': 'datasourceId',
        'description': 'description',
        'display_item': 'displayItem',
        'duration': 'duration',
        'effective_permissions': 'effectivePermissions',
        'href': 'href',
        'id': 'id',
        'is_archived': 'isArchived',
        'is_redacted': 'isRedacted',
        'measured_item': 'measuredItem',
        'measured_item_maximum_duration': 'measuredItemMaximumDuration',
        'name': 'name',
        'number_format': 'numberFormat',
        'period': 'period',
        'process_type': 'processType',
        'scoped_to': 'scopedTo',
        'status_message': 'statusMessage',
        'thresholds': 'thresholds',
        'type': 'type',
        'value_unit_of_measure': 'valueUnitOfMeasure'
    }

    def __init__(self, aggregation_function=None, bounding_condition=None, bounding_condition_maximum_duration=None, condition_thresholds=None, data_id=None, datasource_class=None, datasource_id=None, description=None, display_item=None, duration=None, effective_permissions=None, href=None, id=None, is_archived=False, is_redacted=False, measured_item=None, measured_item_maximum_duration=None, name=None, number_format=None, period=None, process_type=None, scoped_to=None, status_message=None, thresholds=None, type=None, value_unit_of_measure=None):
        """
        ThresholdMetricOutputV1 - a model defined in Swagger
        """

        self._aggregation_function = None
        self._bounding_condition = None
        self._bounding_condition_maximum_duration = None
        self._condition_thresholds = None
        self._data_id = None
        self._datasource_class = None
        self._datasource_id = None
        self._description = None
        self._display_item = None
        self._duration = None
        self._effective_permissions = None
        self._href = None
        self._id = None
        self._is_archived = None
        self._is_redacted = None
        self._measured_item = None
        self._measured_item_maximum_duration = None
        self._name = None
        self._number_format = None
        self._period = None
        self._process_type = None
        self._scoped_to = None
        self._status_message = None
        self._thresholds = None
        self._type = None
        self._value_unit_of_measure = None

        if aggregation_function is not None:
          self.aggregation_function = aggregation_function
        if bounding_condition is not None:
          self.bounding_condition = bounding_condition
        if bounding_condition_maximum_duration is not None:
          self.bounding_condition_maximum_duration = bounding_condition_maximum_duration
        if condition_thresholds is not None:
          self.condition_thresholds = condition_thresholds
        if data_id is not None:
          self.data_id = data_id
        if datasource_class is not None:
          self.datasource_class = datasource_class
        if datasource_id is not None:
          self.datasource_id = datasource_id
        if description is not None:
          self.description = description
        if display_item is not None:
          self.display_item = display_item
        if duration is not None:
          self.duration = duration
        if effective_permissions is not None:
          self.effective_permissions = effective_permissions
        if href is not None:
          self.href = href
        if id is not None:
          self.id = id
        if is_archived is not None:
          self.is_archived = is_archived
        if is_redacted is not None:
          self.is_redacted = is_redacted
        if measured_item is not None:
          self.measured_item = measured_item
        if measured_item_maximum_duration is not None:
          self.measured_item_maximum_duration = measured_item_maximum_duration
        if name is not None:
          self.name = name
        if number_format is not None:
          self.number_format = number_format
        if period is not None:
          self.period = period
        if process_type is not None:
          self.process_type = process_type
        if scoped_to is not None:
          self.scoped_to = scoped_to
        if status_message is not None:
          self.status_message = status_message
        if thresholds is not None:
          self.thresholds = thresholds
        if type is not None:
          self.type = type
        if value_unit_of_measure is not None:
          self.value_unit_of_measure = value_unit_of_measure

    @property
    def aggregation_function(self):
        """
        Gets the aggregation_function of this ThresholdMetricOutputV1.
        Aggregation formula that aggregates the measured item

        :return: The aggregation_function of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._aggregation_function

    @aggregation_function.setter
    def aggregation_function(self, aggregation_function):
        """
        Sets the aggregation_function of this ThresholdMetricOutputV1.
        Aggregation formula that aggregates the measured item

        :param aggregation_function: The aggregation_function of this ThresholdMetricOutputV1.
        :type: str
        """

        self._aggregation_function = aggregation_function

    @property
    def bounding_condition(self):
        """
        Gets the bounding_condition of this ThresholdMetricOutputV1.
        The condition that, if present, will be used to aggregate the measured item

        :return: The bounding_condition of this ThresholdMetricOutputV1.
        :rtype: ItemPreviewWithAssetsV1
        """
        return self._bounding_condition

    @bounding_condition.setter
    def bounding_condition(self, bounding_condition):
        """
        Sets the bounding_condition of this ThresholdMetricOutputV1.
        The condition that, if present, will be used to aggregate the measured item

        :param bounding_condition: The bounding_condition of this ThresholdMetricOutputV1.
        :type: ItemPreviewWithAssetsV1
        """

        self._bounding_condition = bounding_condition

    @property
    def bounding_condition_maximum_duration(self):
        """
        Gets the bounding_condition_maximum_duration of this ThresholdMetricOutputV1.
        The maximum capsule duration that is applied to the bounding condition if it does not have one

        :return: The bounding_condition_maximum_duration of this ThresholdMetricOutputV1.
        :rtype: ScalarValueOutputV1
        """
        return self._bounding_condition_maximum_duration

    @bounding_condition_maximum_duration.setter
    def bounding_condition_maximum_duration(self, bounding_condition_maximum_duration):
        """
        Sets the bounding_condition_maximum_duration of this ThresholdMetricOutputV1.
        The maximum capsule duration that is applied to the bounding condition if it does not have one

        :param bounding_condition_maximum_duration: The bounding_condition_maximum_duration of this ThresholdMetricOutputV1.
        :type: ScalarValueOutputV1
        """

        self._bounding_condition_maximum_duration = bounding_condition_maximum_duration

    @property
    def condition_thresholds(self):
        """
        Gets the condition_thresholds of this ThresholdMetricOutputV1.
        The list of thresholds that are conditions that along with the associated priority. These are used to identify when a threshold excursion has occurred

        :return: The condition_thresholds of this ThresholdMetricOutputV1.
        :rtype: list[ThresholdOutputV1]
        """
        return self._condition_thresholds

    @condition_thresholds.setter
    def condition_thresholds(self, condition_thresholds):
        """
        Sets the condition_thresholds of this ThresholdMetricOutputV1.
        The list of thresholds that are conditions that along with the associated priority. These are used to identify when a threshold excursion has occurred

        :param condition_thresholds: The condition_thresholds of this ThresholdMetricOutputV1.
        :type: list[ThresholdOutputV1]
        """

        self._condition_thresholds = condition_thresholds

    @property
    def data_id(self):
        """
        Gets the data_id of this ThresholdMetricOutputV1.
        The data ID of this asset. Note: This is not the Seeq ID, but the unique identifier that the remote datasource uses.

        :return: The data_id of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._data_id

    @data_id.setter
    def data_id(self, data_id):
        """
        Sets the data_id of this ThresholdMetricOutputV1.
        The data ID of this asset. Note: This is not the Seeq ID, but the unique identifier that the remote datasource uses.

        :param data_id: The data_id of this ThresholdMetricOutputV1.
        :type: str
        """

        self._data_id = data_id

    @property
    def datasource_class(self):
        """
        Gets the datasource_class of this ThresholdMetricOutputV1.
        The datasource class, which is the type of system holding the item, such as OSIsoft PI

        :return: The datasource_class of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._datasource_class

    @datasource_class.setter
    def datasource_class(self, datasource_class):
        """
        Sets the datasource_class of this ThresholdMetricOutputV1.
        The datasource class, which is the type of system holding the item, such as OSIsoft PI

        :param datasource_class: The datasource_class of this ThresholdMetricOutputV1.
        :type: str
        """

        self._datasource_class = datasource_class

    @property
    def datasource_id(self):
        """
        Gets the datasource_id of this ThresholdMetricOutputV1.
        The datasource identifier, which is how the datasource holding this item identifies itself

        :return: The datasource_id of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._datasource_id

    @datasource_id.setter
    def datasource_id(self, datasource_id):
        """
        Sets the datasource_id of this ThresholdMetricOutputV1.
        The datasource identifier, which is how the datasource holding this item identifies itself

        :param datasource_id: The datasource_id of this ThresholdMetricOutputV1.
        :type: str
        """

        self._datasource_id = datasource_id

    @property
    def description(self):
        """
        Gets the description of this ThresholdMetricOutputV1.
        Clarifying information or other plain language description of this item

        :return: The description of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ThresholdMetricOutputV1.
        Clarifying information or other plain language description of this item

        :param description: The description of this ThresholdMetricOutputV1.
        :type: str
        """

        self._description = description

    @property
    def display_item(self):
        """
        Gets the display_item of this ThresholdMetricOutputV1.
        A signal or formula function that evaluates to a signal that can be used to visualize the metric

        :return: The display_item of this ThresholdMetricOutputV1.
        :rtype: ItemPreviewV1
        """
        return self._display_item

    @display_item.setter
    def display_item(self, display_item):
        """
        Sets the display_item of this ThresholdMetricOutputV1.
        A signal or formula function that evaluates to a signal that can be used to visualize the metric

        :param display_item: The display_item of this ThresholdMetricOutputV1.
        :type: ItemPreviewV1
        """
        if display_item is None:
            raise ValueError("Invalid value for `display_item`, must not be `None`")

        self._display_item = display_item

    @property
    def duration(self):
        """
        Gets the duration of this ThresholdMetricOutputV1.
        The duration over which to calculate a moving aggregation

        :return: The duration of this ThresholdMetricOutputV1.
        :rtype: ScalarValueOutputV1
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """
        Sets the duration of this ThresholdMetricOutputV1.
        The duration over which to calculate a moving aggregation

        :param duration: The duration of this ThresholdMetricOutputV1.
        :type: ScalarValueOutputV1
        """

        self._duration = duration

    @property
    def effective_permissions(self):
        """
        Gets the effective_permissions of this ThresholdMetricOutputV1.
        The permissions the current user has to the item.

        :return: The effective_permissions of this ThresholdMetricOutputV1.
        :rtype: PermissionsV1
        """
        return self._effective_permissions

    @effective_permissions.setter
    def effective_permissions(self, effective_permissions):
        """
        Sets the effective_permissions of this ThresholdMetricOutputV1.
        The permissions the current user has to the item.

        :param effective_permissions: The effective_permissions of this ThresholdMetricOutputV1.
        :type: PermissionsV1
        """

        self._effective_permissions = effective_permissions

    @property
    def href(self):
        """
        Gets the href of this ThresholdMetricOutputV1.
        The href that can be used to interact with the item

        :return: The href of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """
        Sets the href of this ThresholdMetricOutputV1.
        The href that can be used to interact with the item

        :param href: The href of this ThresholdMetricOutputV1.
        :type: str
        """
        if href is None:
            raise ValueError("Invalid value for `href`, must not be `None`")

        self._href = href

    @property
    def id(self):
        """
        Gets the id of this ThresholdMetricOutputV1.
        The ID that can be used to interact with the item

        :return: The id of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ThresholdMetricOutputV1.
        The ID that can be used to interact with the item

        :param id: The id of this ThresholdMetricOutputV1.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def is_archived(self):
        """
        Gets the is_archived of this ThresholdMetricOutputV1.
        Whether item is archived

        :return: The is_archived of this ThresholdMetricOutputV1.
        :rtype: bool
        """
        return self._is_archived

    @is_archived.setter
    def is_archived(self, is_archived):
        """
        Sets the is_archived of this ThresholdMetricOutputV1.
        Whether item is archived

        :param is_archived: The is_archived of this ThresholdMetricOutputV1.
        :type: bool
        """

        self._is_archived = is_archived

    @property
    def is_redacted(self):
        """
        Gets the is_redacted of this ThresholdMetricOutputV1.
        Whether item is redacted

        :return: The is_redacted of this ThresholdMetricOutputV1.
        :rtype: bool
        """
        return self._is_redacted

    @is_redacted.setter
    def is_redacted(self, is_redacted):
        """
        Sets the is_redacted of this ThresholdMetricOutputV1.
        Whether item is redacted

        :param is_redacted: The is_redacted of this ThresholdMetricOutputV1.
        :type: bool
        """

        self._is_redacted = is_redacted

    @property
    def measured_item(self):
        """
        Gets the measured_item of this ThresholdMetricOutputV1.
        The input Signal or Condition to measure

        :return: The measured_item of this ThresholdMetricOutputV1.
        :rtype: ItemPreviewWithAssetsV1
        """
        return self._measured_item

    @measured_item.setter
    def measured_item(self, measured_item):
        """
        Sets the measured_item of this ThresholdMetricOutputV1.
        The input Signal or Condition to measure

        :param measured_item: The measured_item of this ThresholdMetricOutputV1.
        :type: ItemPreviewWithAssetsV1
        """
        if measured_item is None:
            raise ValueError("Invalid value for `measured_item`, must not be `None`")

        self._measured_item = measured_item

    @property
    def measured_item_maximum_duration(self):
        """
        Gets the measured_item_maximum_duration of this ThresholdMetricOutputV1.
        The maximum capsule duration that is applied to the measured item if it is a condition without one

        :return: The measured_item_maximum_duration of this ThresholdMetricOutputV1.
        :rtype: ScalarValueOutputV1
        """
        return self._measured_item_maximum_duration

    @measured_item_maximum_duration.setter
    def measured_item_maximum_duration(self, measured_item_maximum_duration):
        """
        Sets the measured_item_maximum_duration of this ThresholdMetricOutputV1.
        The maximum capsule duration that is applied to the measured item if it is a condition without one

        :param measured_item_maximum_duration: The measured_item_maximum_duration of this ThresholdMetricOutputV1.
        :type: ScalarValueOutputV1
        """

        self._measured_item_maximum_duration = measured_item_maximum_duration

    @property
    def name(self):
        """
        Gets the name of this ThresholdMetricOutputV1.
        The human readable name

        :return: The name of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ThresholdMetricOutputV1.
        The human readable name

        :param name: The name of this ThresholdMetricOutputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def number_format(self):
        """
        Gets the number_format of this ThresholdMetricOutputV1.
        The format string used for numbers associated with this signal.

        :return: The number_format of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._number_format

    @number_format.setter
    def number_format(self, number_format):
        """
        Sets the number_format of this ThresholdMetricOutputV1.
        The format string used for numbers associated with this signal.

        :param number_format: The number_format of this ThresholdMetricOutputV1.
        :type: str
        """

        self._number_format = number_format

    @property
    def period(self):
        """
        Gets the period of this ThresholdMetricOutputV1.
        The period at which to sample when creating the moving aggregation

        :return: The period of this ThresholdMetricOutputV1.
        :rtype: ScalarValueOutputV1
        """
        return self._period

    @period.setter
    def period(self, period):
        """
        Sets the period of this ThresholdMetricOutputV1.
        The period at which to sample when creating the moving aggregation

        :param period: The period of this ThresholdMetricOutputV1.
        :type: ScalarValueOutputV1
        """

        self._period = period

    @property
    def process_type(self):
        """
        Gets the process_type of this ThresholdMetricOutputV1.
        The process type of threshold metric. Will be Continuous if duration and period are specified, Condition if boundingCondition is specified, and otherwise Simple.

        :return: The process_type of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._process_type

    @process_type.setter
    def process_type(self, process_type):
        """
        Sets the process_type of this ThresholdMetricOutputV1.
        The process type of threshold metric. Will be Continuous if duration and period are specified, Condition if boundingCondition is specified, and otherwise Simple.

        :param process_type: The process_type of this ThresholdMetricOutputV1.
        :type: str
        """
        if process_type is None:
            raise ValueError("Invalid value for `process_type`, must not be `None`")
        allowed_values = ["Simple", "Condition", "Continuous"]
        if process_type not in allowed_values:
            raise ValueError(
                "Invalid value for `process_type` ({0}), must be one of {1}"
                .format(process_type, allowed_values)
            )

        self._process_type = process_type

    @property
    def scoped_to(self):
        """
        Gets the scoped_to of this ThresholdMetricOutputV1.
        The ID of the workbook to which this item is scoped or null if it is in the global scope.

        :return: The scoped_to of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._scoped_to

    @scoped_to.setter
    def scoped_to(self, scoped_to):
        """
        Sets the scoped_to of this ThresholdMetricOutputV1.
        The ID of the workbook to which this item is scoped or null if it is in the global scope.

        :param scoped_to: The scoped_to of this ThresholdMetricOutputV1.
        :type: str
        """

        self._scoped_to = scoped_to

    @property
    def status_message(self):
        """
        Gets the status_message of this ThresholdMetricOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :return: The status_message of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """
        Sets the status_message of this ThresholdMetricOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :param status_message: The status_message of this ThresholdMetricOutputV1.
        :type: str
        """

        self._status_message = status_message

    @property
    def thresholds(self):
        """
        Gets the thresholds of this ThresholdMetricOutputV1.
        The list of thresholds that are scalars, signals, or conditions along with the associated priority. These thresholds are those that were used as inputs and which are used to generate the condition thresholds

        :return: The thresholds of this ThresholdMetricOutputV1.
        :rtype: list[ThresholdOutputV1]
        """
        return self._thresholds

    @thresholds.setter
    def thresholds(self, thresholds):
        """
        Sets the thresholds of this ThresholdMetricOutputV1.
        The list of thresholds that are scalars, signals, or conditions along with the associated priority. These thresholds are those that were used as inputs and which are used to generate the condition thresholds

        :param thresholds: The thresholds of this ThresholdMetricOutputV1.
        :type: list[ThresholdOutputV1]
        """

        self._thresholds = thresholds

    @property
    def type(self):
        """
        Gets the type of this ThresholdMetricOutputV1.
        The type of the item

        :return: The type of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ThresholdMetricOutputV1.
        The type of the item

        :param type: The type of this ThresholdMetricOutputV1.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")

        self._type = type

    @property
    def value_unit_of_measure(self):
        """
        Gets the value_unit_of_measure of this ThresholdMetricOutputV1.
        The unit of measure of the metric

        :return: The value_unit_of_measure of this ThresholdMetricOutputV1.
        :rtype: str
        """
        return self._value_unit_of_measure

    @value_unit_of_measure.setter
    def value_unit_of_measure(self, value_unit_of_measure):
        """
        Sets the value_unit_of_measure of this ThresholdMetricOutputV1.
        The unit of measure of the metric

        :param value_unit_of_measure: The value_unit_of_measure of this ThresholdMetricOutputV1.
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
        if not isinstance(other, ThresholdMetricOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
