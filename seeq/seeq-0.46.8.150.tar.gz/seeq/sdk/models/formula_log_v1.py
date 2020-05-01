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


class FormulaLogV1(object):
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
        'formula_log_entries': 'dict(str, FormulaLogEntry)',
        'formula_token': 'FormulaToken'
    }

    attribute_map = {
        'formula_log_entries': 'formulaLogEntries',
        'formula_token': 'formulaToken'
    }

    def __init__(self, formula_log_entries=None, formula_token=None):
        """
        FormulaLogV1 - a model defined in Swagger
        """

        self._formula_log_entries = None
        self._formula_token = None

        if formula_log_entries is not None:
          self.formula_log_entries = formula_log_entries
        if formula_token is not None:
          self.formula_token = formula_token

    @property
    def formula_log_entries(self):
        """
        Gets the formula_log_entries of this FormulaLogV1.
        The detailed Formula log entries which occurred at this token

        :return: The formula_log_entries of this FormulaLogV1.
        :rtype: dict(str, FormulaLogEntry)
        """
        return self._formula_log_entries

    @formula_log_entries.setter
    def formula_log_entries(self, formula_log_entries):
        """
        Sets the formula_log_entries of this FormulaLogV1.
        The detailed Formula log entries which occurred at this token

        :param formula_log_entries: The formula_log_entries of this FormulaLogV1.
        :type: dict(str, FormulaLogEntry)
        """
        if formula_log_entries is None:
            raise ValueError("Invalid value for `formula_log_entries`, must not be `None`")

        self._formula_log_entries = formula_log_entries

    @property
    def formula_token(self):
        """
        Gets the formula_token of this FormulaLogV1.
        The token where the event took place in the Formula

        :return: The formula_token of this FormulaLogV1.
        :rtype: FormulaToken
        """
        return self._formula_token

    @formula_token.setter
    def formula_token(self, formula_token):
        """
        Sets the formula_token of this FormulaLogV1.
        The token where the event took place in the Formula

        :param formula_token: The formula_token of this FormulaLogV1.
        :type: FormulaToken
        """
        if formula_token is None:
            raise ValueError("Invalid value for `formula_token`, must not be `None`")

        self._formula_token = formula_token

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
        if not isinstance(other, FormulaLogV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
