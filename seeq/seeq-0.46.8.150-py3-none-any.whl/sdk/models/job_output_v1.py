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


class JobOutputV1(object):
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
        'configuration': 'dict(str, object)',
        'document_id': 'str',
        'document_name': 'str',
        'duration': 'int',
        'group': 'str',
        'id': 'str',
        'next_run_time': 'str',
        'previous_run_time': 'str',
        'status_message': 'str',
        'topic_id': 'str',
        'topic_name': 'str'
    }

    attribute_map = {
        'configuration': 'configuration',
        'document_id': 'documentId',
        'document_name': 'documentName',
        'duration': 'duration',
        'group': 'group',
        'id': 'id',
        'next_run_time': 'nextRunTime',
        'previous_run_time': 'previousRunTime',
        'status_message': 'statusMessage',
        'topic_id': 'topicId',
        'topic_name': 'topicName'
    }

    def __init__(self, configuration=None, document_id=None, document_name=None, duration=None, group=None, id=None, next_run_time=None, previous_run_time=None, status_message=None, topic_id=None, topic_name=None):
        """
        JobOutputV1 - a model defined in Swagger
        """

        self._configuration = None
        self._document_id = None
        self._document_name = None
        self._duration = None
        self._group = None
        self._id = None
        self._next_run_time = None
        self._previous_run_time = None
        self._status_message = None
        self._topic_id = None
        self._topic_name = None

        if configuration is not None:
          self.configuration = configuration
        if document_id is not None:
          self.document_id = document_id
        if document_name is not None:
          self.document_name = document_name
        if duration is not None:
          self.duration = duration
        if group is not None:
          self.group = group
        if id is not None:
          self.id = id
        if next_run_time is not None:
          self.next_run_time = next_run_time
        if previous_run_time is not None:
          self.previous_run_time = previous_run_time
        if status_message is not None:
          self.status_message = status_message
        if topic_id is not None:
          self.topic_id = topic_id
        if topic_name is not None:
          self.topic_name = topic_name

    @property
    def configuration(self):
        """
        Gets the configuration of this JobOutputV1.
        The configuration for the job

        :return: The configuration of this JobOutputV1.
        :rtype: dict(str, object)
        """
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        """
        Sets the configuration of this JobOutputV1.
        The configuration for the job

        :param configuration: The configuration of this JobOutputV1.
        :type: dict(str, object)
        """

        self._configuration = configuration

    @property
    def document_id(self):
        """
        Gets the document_id of this JobOutputV1.
        The ID of the topic document, if supplied, that requested this job

        :return: The document_id of this JobOutputV1.
        :rtype: str
        """
        return self._document_id

    @document_id.setter
    def document_id(self, document_id):
        """
        Sets the document_id of this JobOutputV1.
        The ID of the topic document, if supplied, that requested this job

        :param document_id: The document_id of this JobOutputV1.
        :type: str
        """

        self._document_id = document_id

    @property
    def document_name(self):
        """
        Gets the document_name of this JobOutputV1.
        The name of the topic document, if supplied, which requested this job

        :return: The document_name of this JobOutputV1.
        :rtype: str
        """
        return self._document_name

    @document_name.setter
    def document_name(self, document_name):
        """
        Sets the document_name of this JobOutputV1.
        The name of the topic document, if supplied, which requested this job

        :param document_name: The document_name of this JobOutputV1.
        :type: str
        """

        self._document_name = document_name

    @property
    def duration(self):
        """
        Gets the duration of this JobOutputV1.
        The amount of time, in nanoseconds, that the job took for its last execution

        :return: The duration of this JobOutputV1.
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """
        Sets the duration of this JobOutputV1.
        The amount of time, in nanoseconds, that the job took for its last execution

        :param duration: The duration of this JobOutputV1.
        :type: int
        """

        self._duration = duration

    @property
    def group(self):
        """
        Gets the group of this JobOutputV1.
        The group to which the job belongs

        :return: The group of this JobOutputV1.
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group):
        """
        Sets the group of this JobOutputV1.
        The group to which the job belongs

        :param group: The group of this JobOutputV1.
        :type: str
        """

        self._group = group

    @property
    def id(self):
        """
        Gets the id of this JobOutputV1.
        The id of the job

        :return: The id of this JobOutputV1.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this JobOutputV1.
        The id of the job

        :param id: The id of this JobOutputV1.
        :type: str
        """

        self._id = id

    @property
    def next_run_time(self):
        """
        Gets the next_run_time of this JobOutputV1.
        The next time, as an ISO timestamp, the job is scheduled to run. Empty if it is not scheduled

        :return: The next_run_time of this JobOutputV1.
        :rtype: str
        """
        return self._next_run_time

    @next_run_time.setter
    def next_run_time(self, next_run_time):
        """
        Sets the next_run_time of this JobOutputV1.
        The next time, as an ISO timestamp, the job is scheduled to run. Empty if it is not scheduled

        :param next_run_time: The next_run_time of this JobOutputV1.
        :type: str
        """

        self._next_run_time = next_run_time

    @property
    def previous_run_time(self):
        """
        Gets the previous_run_time of this JobOutputV1.
        The previous time, as an ISO timestamp, at which the job was run. Empty if it has not been run

        :return: The previous_run_time of this JobOutputV1.
        :rtype: str
        """
        return self._previous_run_time

    @previous_run_time.setter
    def previous_run_time(self, previous_run_time):
        """
        Sets the previous_run_time of this JobOutputV1.
        The previous time, as an ISO timestamp, at which the job was run. Empty if it has not been run

        :param previous_run_time: The previous_run_time of this JobOutputV1.
        :type: str
        """

        self._previous_run_time = previous_run_time

    @property
    def status_message(self):
        """
        Gets the status_message of this JobOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation. Null if the status message has not been set.

        :return: The status_message of this JobOutputV1.
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """
        Sets the status_message of this JobOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation. Null if the status message has not been set.

        :param status_message: The status_message of this JobOutputV1.
        :type: str
        """

        self._status_message = status_message

    @property
    def topic_id(self):
        """
        Gets the topic_id of this JobOutputV1.
        The ID of the Topic, if supplied, that requested this job

        :return: The topic_id of this JobOutputV1.
        :rtype: str
        """
        return self._topic_id

    @topic_id.setter
    def topic_id(self, topic_id):
        """
        Sets the topic_id of this JobOutputV1.
        The ID of the Topic, if supplied, that requested this job

        :param topic_id: The topic_id of this JobOutputV1.
        :type: str
        """

        self._topic_id = topic_id

    @property
    def topic_name(self):
        """
        Gets the topic_name of this JobOutputV1.
        The name of the topic, if supplied, that requested this job

        :return: The topic_name of this JobOutputV1.
        :rtype: str
        """
        return self._topic_name

    @topic_name.setter
    def topic_name(self, topic_name):
        """
        Sets the topic_name of this JobOutputV1.
        The name of the topic, if supplied, that requested this job

        :param topic_name: The topic_name of this JobOutputV1.
        :type: str
        """

        self._topic_name = topic_name

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
        if not isinstance(other, JobOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
