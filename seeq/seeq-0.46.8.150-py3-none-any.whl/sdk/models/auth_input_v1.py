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


class AuthInputV1(object):
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
        'auth_provider_class': 'str',
        'auth_provider_id': 'str',
        'code': 'str',
        'password': 'str',
        'state': 'str',
        'username': 'str'
    }

    attribute_map = {
        'auth_provider_class': 'authProviderClass',
        'auth_provider_id': 'authProviderId',
        'code': 'code',
        'password': 'password',
        'state': 'state',
        'username': 'username'
    }

    def __init__(self, auth_provider_class=None, auth_provider_id=None, code=None, password=None, state=None, username=None):
        """
        AuthInputV1 - a model defined in Swagger
        """

        self._auth_provider_class = None
        self._auth_provider_id = None
        self._code = None
        self._password = None
        self._state = None
        self._username = None

        if auth_provider_class is not None:
          self.auth_provider_class = auth_provider_class
        if auth_provider_id is not None:
          self.auth_provider_id = auth_provider_id
        if code is not None:
          self.code = code
        if password is not None:
          self.password = password
        if state is not None:
          self.state = state
        if username is not None:
          self.username = username

    @property
    def auth_provider_class(self):
        """
        Gets the auth_provider_class of this AuthInputV1.
        The class of the auth provider for this user. Leave blank to use the Seeq directory.

        :return: The auth_provider_class of this AuthInputV1.
        :rtype: str
        """
        return self._auth_provider_class

    @auth_provider_class.setter
    def auth_provider_class(self, auth_provider_class):
        """
        Sets the auth_provider_class of this AuthInputV1.
        The class of the auth provider for this user. Leave blank to use the Seeq directory.

        :param auth_provider_class: The auth_provider_class of this AuthInputV1.
        :type: str
        """

        self._auth_provider_class = auth_provider_class

    @property
    def auth_provider_id(self):
        """
        Gets the auth_provider_id of this AuthInputV1.
        The id of the auth provider for this user. Leave blank to use the Seeq directory.

        :return: The auth_provider_id of this AuthInputV1.
        :rtype: str
        """
        return self._auth_provider_id

    @auth_provider_id.setter
    def auth_provider_id(self, auth_provider_id):
        """
        Sets the auth_provider_id of this AuthInputV1.
        The id of the auth provider for this user. Leave blank to use the Seeq directory.

        :param auth_provider_id: The auth_provider_id of this AuthInputV1.
        :type: str
        """

        self._auth_provider_id = auth_provider_id

    @property
    def code(self):
        """
        Gets the code of this AuthInputV1.
        The authorization code for OAuth2 authentication.

        :return: The code of this AuthInputV1.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this AuthInputV1.
        The authorization code for OAuth2 authentication.

        :param code: The code of this AuthInputV1.
        :type: str
        """

        self._code = code

    @property
    def password(self):
        """
        Gets the password of this AuthInputV1.
        The password of the user

        :return: The password of this AuthInputV1.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Sets the password of this AuthInputV1.
        The password of the user

        :param password: The password of this AuthInputV1.
        :type: str
        """

        self._password = password

    @property
    def state(self):
        """
        Gets the state of this AuthInputV1.
        The state for OAuth2 authentication

        :return: The state of this AuthInputV1.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this AuthInputV1.
        The state for OAuth2 authentication

        :param state: The state of this AuthInputV1.
        :type: str
        """

        self._state = state

    @property
    def username(self):
        """
        Gets the username of this AuthInputV1.
        The username of the user

        :return: The username of this AuthInputV1.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this AuthInputV1.
        The username of the user

        :param username: The username of this AuthInputV1.
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
        if not isinstance(other, AuthInputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
