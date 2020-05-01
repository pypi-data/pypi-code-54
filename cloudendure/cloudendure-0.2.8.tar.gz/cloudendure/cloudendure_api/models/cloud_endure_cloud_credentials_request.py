# coding: utf-8

"""
    CloudEndure API documentation

    © 2017 CloudEndure All rights reserved  # General Request authentication in CloudEndure's API is done using session cookies. A session cookie is returned upon successful execution of the \"login\" method. This value must then be provided within the request headers of all subsequent API requests.  ## Errors Some errors are not specifically written in every method since they may always return. Those are: 1) 401 (Unauthorized) - for unauthenticated requests. 2) 405 (Method Not Allowed) - for using a method that is not supported (POST instead of GET). 3) 403 (Forbidden) - request is authenticated, but the user is not allowed to access. 4) 422 (Unprocessable Entity) - for invalid input.  ## Formats All strings with date-time format are according to RFC3339.  All strings with \"duration\" format are according to ISO8601. For example, a full day duration can be specified with \"PNNNND\".   # noqa: E501

    OpenAPI spec version: 5
    Contact: https://bit.ly/2T54hSc
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class CloudEndureCloudCredentialsRequest:
    """NOTE: This class is auto generated by the swagger code generator program.

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
        "public_key": "str",
        "name": "str",
        "cloud_id": "str",
        "private_key": "str",
        "account_identifier": "str",
        "id": "str",
    }

    attribute_map = {
        "public_key": "publicKey",
        "name": "name",
        "cloud_id": "cloudId",
        "private_key": "privateKey",
        "account_identifier": "accountIdentifier",
        "id": "id",
    }

    def __init__(
        self,
        public_key=None,
        name=None,
        cloud_id=None,
        private_key=None,
        account_identifier=None,
        id=None,
    ):  # noqa: E501
        """CloudEndureCloudCredentialsRequest - a model defined in Swagger"""  # noqa: E501
        self._public_key = None
        self._name = None
        self._cloud_id = None
        self._private_key = None
        self._account_identifier = None
        self._id = None
        self.discriminator = None
        if public_key is not None:
            self.public_key = public_key
        if name is not None:
            self.name = name
        self.cloud_id = cloud_id
        if private_key is not None:
            self.private_key = private_key
        if account_identifier is not None:
            self.account_identifier = account_identifier
        if id is not None:
            self.id = id

    @property
    def public_key(self):
        """Gets the public_key of this CloudEndureCloudCredentialsRequest.  # noqa: E501

        The public part of the Cloud credentials. For AWS - The access key ID, For GCP and Azure - N/A.  # noqa: E501

        :return: The public_key of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :rtype: str
        """
        return self._public_key

    @public_key.setter
    def public_key(self, public_key):
        """Sets the public_key of this CloudEndureCloudCredentialsRequest.

        The public part of the Cloud credentials. For AWS - The access key ID, For GCP and Azure - N/A.  # noqa: E501

        :param public_key: The public_key of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :type: str
        """

        self._public_key = public_key

    @property
    def name(self):
        """Gets the name of this CloudEndureCloudCredentialsRequest.  # noqa: E501

        An optional (can be empty), user provided, descriptive name.  # noqa: E501

        :return: The name of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CloudEndureCloudCredentialsRequest.

        An optional (can be empty), user provided, descriptive name.  # noqa: E501

        :param name: The name of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def cloud_id(self):
        """Gets the cloud_id of this CloudEndureCloudCredentialsRequest.  # noqa: E501


        :return: The cloud_id of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this CloudEndureCloudCredentialsRequest.


        :param cloud_id: The cloud_id of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :type: str
        """
        if cloud_id is None:
            raise ValueError(
                "Invalid value for `cloud_id`, must not be `None`"
            )  # noqa: E501

        self._cloud_id = cloud_id

    @property
    def private_key(self):
        """Gets the private_key of this CloudEndureCloudCredentialsRequest.  # noqa: E501

        Cloud credentials secret. For AWS - The secret access key, For GCP - The private key in JSON format, For Azure - The certificate file.  # noqa: E501

        :return: The private_key of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :rtype: str
        """
        return self._private_key

    @private_key.setter
    def private_key(self, private_key):
        """Sets the private_key of this CloudEndureCloudCredentialsRequest.

        Cloud credentials secret. For AWS - The secret access key, For GCP - The private key in JSON format, For Azure - The certificate file.  # noqa: E501

        :param private_key: The private_key of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :type: str
        """

        self._private_key = private_key

    @property
    def account_identifier(self):
        """Gets the account_identifier of this CloudEndureCloudCredentialsRequest.  # noqa: E501

        Cloud account identifier. For AWS - N/A, For GCP - The project ID, For Azure - The subscription ID.  # noqa: E501

        :return: The account_identifier of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :rtype: str
        """
        return self._account_identifier

    @account_identifier.setter
    def account_identifier(self, account_identifier):
        """Sets the account_identifier of this CloudEndureCloudCredentialsRequest.

        Cloud account identifier. For AWS - N/A, For GCP - The project ID, For Azure - The subscription ID.  # noqa: E501

        :param account_identifier: The account_identifier of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :type: str
        """

        self._account_identifier = account_identifier

    @property
    def id(self):
        """Gets the id of this CloudEndureCloudCredentialsRequest.  # noqa: E501


        :return: The id of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this CloudEndureCloudCredentialsRequest.


        :param id: The id of this CloudEndureCloudCredentialsRequest.  # noqa: E501
        :type: str
        """

        self._id = id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(CloudEndureCloudCredentialsRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CloudEndureCloudCredentialsRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
