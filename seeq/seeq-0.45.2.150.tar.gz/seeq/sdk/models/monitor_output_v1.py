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


class MonitorOutputV1(object):
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
        'monitor_values': 'MonitorValues'
    }

    attribute_map = {
        'monitor_values': 'monitorValues'
    }

    def __init__(self, monitor_values=None):
        """
        MonitorOutputV1 - a model defined in Swagger
        """

        self._monitor_values = None

        if monitor_values is not None:
          self.monitor_values = monitor_values

    @property
    def monitor_values(self):
        """
        Gets the monitor_values of this MonitorOutputV1.

        :return: The monitor_values of this MonitorOutputV1.
        :rtype: MonitorValues
        """
        return self._monitor_values

    @monitor_values.setter
    def monitor_values(self, monitor_values):
        """
        Sets the monitor_values of this MonitorOutputV1.

        :param monitor_values: The monitor_values of this MonitorOutputV1.
        :type: MonitorValues
        """

        self._monitor_values = monitor_values

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
        if not isinstance(other, MonitorOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
