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


class MonitorValues(object):
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
        'count': 'int',
        'fifteen_minute_rate': 'float',
        'five_minute_rate': 'float',
        'max': 'float',
        'mean': 'float',
        'min': 'float',
        'one_minute_rate': 'float',
        'p50': 'float',
        'p75': 'float',
        'p95': 'float',
        'p98': 'float',
        'p99': 'float',
        'p999': 'float',
        'stddev': 'float',
        'value': 'float'
    }

    attribute_map = {
        'count': 'count',
        'fifteen_minute_rate': 'fifteenMinuteRate',
        'five_minute_rate': 'fiveMinuteRate',
        'max': 'max',
        'mean': 'mean',
        'min': 'min',
        'one_minute_rate': 'oneMinuteRate',
        'p50': 'p50',
        'p75': 'p75',
        'p95': 'p95',
        'p98': 'p98',
        'p99': 'p99',
        'p999': 'p999',
        'stddev': 'stddev',
        'value': 'value'
    }

    def __init__(self, count=None, fifteen_minute_rate=None, five_minute_rate=None, max=None, mean=None, min=None, one_minute_rate=None, p50=None, p75=None, p95=None, p98=None, p99=None, p999=None, stddev=None, value=None):
        """
        MonitorValues - a model defined in Swagger
        """

        self._count = None
        self._fifteen_minute_rate = None
        self._five_minute_rate = None
        self._max = None
        self._mean = None
        self._min = None
        self._one_minute_rate = None
        self._p50 = None
        self._p75 = None
        self._p95 = None
        self._p98 = None
        self._p99 = None
        self._p999 = None
        self._stddev = None
        self._value = None

        if count is not None:
          self.count = count
        if fifteen_minute_rate is not None:
          self.fifteen_minute_rate = fifteen_minute_rate
        if five_minute_rate is not None:
          self.five_minute_rate = five_minute_rate
        if max is not None:
          self.max = max
        if mean is not None:
          self.mean = mean
        if min is not None:
          self.min = min
        if one_minute_rate is not None:
          self.one_minute_rate = one_minute_rate
        if p50 is not None:
          self.p50 = p50
        if p75 is not None:
          self.p75 = p75
        if p95 is not None:
          self.p95 = p95
        if p98 is not None:
          self.p98 = p98
        if p99 is not None:
          self.p99 = p99
        if p999 is not None:
          self.p999 = p999
        if stddev is not None:
          self.stddev = stddev
        if value is not None:
          self.value = value

    @property
    def count(self):
        """
        Gets the count of this MonitorValues.
        If a timer, the number of timed events

        :return: The count of this MonitorValues.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """
        Sets the count of this MonitorValues.
        If a timer, the number of timed events

        :param count: The count of this MonitorValues.
        :type: int
        """

        self._count = count

    @property
    def fifteen_minute_rate(self):
        """
        Gets the fifteen_minute_rate of this MonitorValues.
        Rate observed over the last 15 minutes

        :return: The fifteen_minute_rate of this MonitorValues.
        :rtype: float
        """
        return self._fifteen_minute_rate

    @fifteen_minute_rate.setter
    def fifteen_minute_rate(self, fifteen_minute_rate):
        """
        Sets the fifteen_minute_rate of this MonitorValues.
        Rate observed over the last 15 minutes

        :param fifteen_minute_rate: The fifteen_minute_rate of this MonitorValues.
        :type: float
        """

        self._fifteen_minute_rate = fifteen_minute_rate

    @property
    def five_minute_rate(self):
        """
        Gets the five_minute_rate of this MonitorValues.
        Rate observed over the last 5 minutes

        :return: The five_minute_rate of this MonitorValues.
        :rtype: float
        """
        return self._five_minute_rate

    @five_minute_rate.setter
    def five_minute_rate(self, five_minute_rate):
        """
        Sets the five_minute_rate of this MonitorValues.
        Rate observed over the last 5 minutes

        :param five_minute_rate: The five_minute_rate of this MonitorValues.
        :type: float
        """

        self._five_minute_rate = five_minute_rate

    @property
    def max(self):
        """
        Gets the max of this MonitorValues.

        :return: The max of this MonitorValues.
        :rtype: float
        """
        return self._max

    @max.setter
    def max(self, max):
        """
        Sets the max of this MonitorValues.

        :param max: The max of this MonitorValues.
        :type: float
        """

        self._max = max

    @property
    def mean(self):
        """
        Gets the mean of this MonitorValues.

        :return: The mean of this MonitorValues.
        :rtype: float
        """
        return self._mean

    @mean.setter
    def mean(self, mean):
        """
        Sets the mean of this MonitorValues.

        :param mean: The mean of this MonitorValues.
        :type: float
        """

        self._mean = mean

    @property
    def min(self):
        """
        Gets the min of this MonitorValues.

        :return: The min of this MonitorValues.
        :rtype: float
        """
        return self._min

    @min.setter
    def min(self, min):
        """
        Sets the min of this MonitorValues.

        :param min: The min of this MonitorValues.
        :type: float
        """

        self._min = min

    @property
    def one_minute_rate(self):
        """
        Gets the one_minute_rate of this MonitorValues.
        Rate observed over the last 1 minute

        :return: The one_minute_rate of this MonitorValues.
        :rtype: float
        """
        return self._one_minute_rate

    @one_minute_rate.setter
    def one_minute_rate(self, one_minute_rate):
        """
        Sets the one_minute_rate of this MonitorValues.
        Rate observed over the last 1 minute

        :param one_minute_rate: The one_minute_rate of this MonitorValues.
        :type: float
        """

        self._one_minute_rate = one_minute_rate

    @property
    def p50(self):
        """
        Gets the p50 of this MonitorValues.
        50th percentile (also known as median)

        :return: The p50 of this MonitorValues.
        :rtype: float
        """
        return self._p50

    @p50.setter
    def p50(self, p50):
        """
        Sets the p50 of this MonitorValues.
        50th percentile (also known as median)

        :param p50: The p50 of this MonitorValues.
        :type: float
        """

        self._p50 = p50

    @property
    def p75(self):
        """
        Gets the p75 of this MonitorValues.
        75th percentile

        :return: The p75 of this MonitorValues.
        :rtype: float
        """
        return self._p75

    @p75.setter
    def p75(self, p75):
        """
        Sets the p75 of this MonitorValues.
        75th percentile

        :param p75: The p75 of this MonitorValues.
        :type: float
        """

        self._p75 = p75

    @property
    def p95(self):
        """
        Gets the p95 of this MonitorValues.
        95th percentile

        :return: The p95 of this MonitorValues.
        :rtype: float
        """
        return self._p95

    @p95.setter
    def p95(self, p95):
        """
        Sets the p95 of this MonitorValues.
        95th percentile

        :param p95: The p95 of this MonitorValues.
        :type: float
        """

        self._p95 = p95

    @property
    def p98(self):
        """
        Gets the p98 of this MonitorValues.
        98th percentile

        :return: The p98 of this MonitorValues.
        :rtype: float
        """
        return self._p98

    @p98.setter
    def p98(self, p98):
        """
        Sets the p98 of this MonitorValues.
        98th percentile

        :param p98: The p98 of this MonitorValues.
        :type: float
        """

        self._p98 = p98

    @property
    def p99(self):
        """
        Gets the p99 of this MonitorValues.
        99th percentile

        :return: The p99 of this MonitorValues.
        :rtype: float
        """
        return self._p99

    @p99.setter
    def p99(self, p99):
        """
        Sets the p99 of this MonitorValues.
        99th percentile

        :param p99: The p99 of this MonitorValues.
        :type: float
        """

        self._p99 = p99

    @property
    def p999(self):
        """
        Gets the p999 of this MonitorValues.
        99.9th percentile

        :return: The p999 of this MonitorValues.
        :rtype: float
        """
        return self._p999

    @p999.setter
    def p999(self, p999):
        """
        Sets the p999 of this MonitorValues.
        99.9th percentile

        :param p999: The p999 of this MonitorValues.
        :type: float
        """

        self._p999 = p999

    @property
    def stddev(self):
        """
        Gets the stddev of this MonitorValues.
        Standard deviation

        :return: The stddev of this MonitorValues.
        :rtype: float
        """
        return self._stddev

    @stddev.setter
    def stddev(self, stddev):
        """
        Sets the stddev of this MonitorValues.
        Standard deviation

        :param stddev: The stddev of this MonitorValues.
        :type: float
        """

        self._stddev = stddev

    @property
    def value(self):
        """
        Gets the value of this MonitorValues.
        Gauge's current value

        :return: The value of this MonitorValues.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this MonitorValues.
        Gauge's current value

        :param value: The value of this MonitorValues.
        :type: float
        """

        self._value = value

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
        if not isinstance(other, MonitorValues):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
