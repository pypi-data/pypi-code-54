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


class SubscriptionOutputV1(object):
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
        'parameters': 'list[SubscriptionParameterOutputV1]',
        'session_id': 'str',
        'username': 'str'
    }

    attribute_map = {
        'parameters': 'parameters',
        'session_id': 'sessionId',
        'username': 'username'
    }

    def __init__(self, parameters=None, session_id=None, username=None):
        """
        SubscriptionOutputV1 - a model defined in Swagger
        """

        self._parameters = None
        self._session_id = None
        self._username = None

        if parameters is not None:
          self.parameters = parameters
        if session_id is not None:
          self.session_id = session_id
        if username is not None:
          self.username = username

    @property
    def parameters(self):
        """
        Gets the parameters of this SubscriptionOutputV1.
        The parameters associated with the subscription

        :return: The parameters of this SubscriptionOutputV1.
        :rtype: list[SubscriptionParameterOutputV1]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this SubscriptionOutputV1.
        The parameters associated with the subscription

        :param parameters: The parameters of this SubscriptionOutputV1.
        :type: list[SubscriptionParameterOutputV1]
        """

        self._parameters = parameters

    @property
    def session_id(self):
        """
        Gets the session_id of this SubscriptionOutputV1.
        The session ID that identifies this subscription

        :return: The session_id of this SubscriptionOutputV1.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """
        Sets the session_id of this SubscriptionOutputV1.
        The session ID that identifies this subscription

        :param session_id: The session_id of this SubscriptionOutputV1.
        :type: str
        """

        self._session_id = session_id

    @property
    def username(self):
        """
        Gets the username of this SubscriptionOutputV1.
        The username associated with the subscription

        :return: The username of this SubscriptionOutputV1.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this SubscriptionOutputV1.
        The username associated with the subscription

        :param username: The username of this SubscriptionOutputV1.
        :type: str
        """

        self._username = username

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
        if not isinstance(other, SubscriptionOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
