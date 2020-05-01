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


class MeterDatumV1(object):
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
        'args': 'list[str]',
        'increments': 'int',
        'monitor': 'str'
    }

    attribute_map = {
        'args': 'args',
        'increments': 'increments',
        'monitor': 'monitor'
    }

    def __init__(self, args=None, increments=None, monitor=None):
        """
        MeterDatumV1 - a model defined in Swagger
        """

        self._args = None
        self._increments = None
        self._monitor = None

        if args is not None:
          self.args = args
        if increments is not None:
          self.increments = increments
        if monitor is not None:
          self.monitor = monitor

    @property
    def args(self):
        """
        Gets the args of this MeterDatumV1.
        List of arguments to include in the monitor path

        :return: The args of this MeterDatumV1.
        :rtype: list[str]
        """
        return self._args

    @args.setter
    def args(self, args):
        """
        Sets the args of this MeterDatumV1.
        List of arguments to include in the monitor path

        :param args: The args of this MeterDatumV1.
        :type: list[str]
        """

        self._args = args

    @property
    def increments(self):
        """
        Gets the increments of this MeterDatumV1.
        Number of increments to the meter. Defaults to 1.

        :return: The increments of this MeterDatumV1.
        :rtype: int
        """
        return self._increments

    @increments.setter
    def increments(self, increments):
        """
        Sets the increments of this MeterDatumV1.
        Number of increments to the meter. Defaults to 1.

        :param increments: The increments of this MeterDatumV1.
        :type: int
        """

        self._increments = increments

    @property
    def monitor(self):
        """
        Gets the monitor of this MeterDatumV1.
        Name of the monitor item this data should apply to.

        :return: The monitor of this MeterDatumV1.
        :rtype: str
        """
        return self._monitor

    @monitor.setter
    def monitor(self, monitor):
        """
        Sets the monitor of this MeterDatumV1.
        Name of the monitor item this data should apply to.

        :param monitor: The monitor of this MeterDatumV1.
        :type: str
        """
        if monitor is None:
            raise ValueError("Invalid value for `monitor`, must not be `None`")

        self._monitor = monitor

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
        if not isinstance(other, MeterDatumV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
