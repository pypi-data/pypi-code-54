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


class FolderOutputV1(object):
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
        'ancestors': 'list[ItemPreviewV1]',
        'created_at': 'str',
        'description': 'str',
        'effective_permissions': 'PermissionsV1',
        'href': 'str',
        'id': 'str',
        'is_archived': 'bool',
        'is_redacted': 'bool',
        'marked_as_favorite': 'bool',
        'name': 'str',
        'owner': 'IdentityPreviewV1',
        'parent_folder_id': 'str',
        'status_message': 'str',
        'type': 'str',
        'updated_at': 'str'
    }

    attribute_map = {
        'ancestors': 'ancestors',
        'created_at': 'createdAt',
        'description': 'description',
        'effective_permissions': 'effectivePermissions',
        'href': 'href',
        'id': 'id',
        'is_archived': 'isArchived',
        'is_redacted': 'isRedacted',
        'marked_as_favorite': 'markedAsFavorite',
        'name': 'name',
        'owner': 'owner',
        'parent_folder_id': 'parentFolderId',
        'status_message': 'statusMessage',
        'type': 'type',
        'updated_at': 'updatedAt'
    }

    def __init__(self, ancestors=None, created_at=None, description=None, effective_permissions=None, href=None, id=None, is_archived=False, is_redacted=False, marked_as_favorite=False, name=None, owner=None, parent_folder_id=None, status_message=None, type=None, updated_at=None):
        """
        FolderOutputV1 - a model defined in Swagger
        """

        self._ancestors = None
        self._created_at = None
        self._description = None
        self._effective_permissions = None
        self._href = None
        self._id = None
        self._is_archived = None
        self._is_redacted = None
        self._marked_as_favorite = None
        self._name = None
        self._owner = None
        self._parent_folder_id = None
        self._status_message = None
        self._type = None
        self._updated_at = None

        if ancestors is not None:
          self.ancestors = ancestors
        if created_at is not None:
          self.created_at = created_at
        if description is not None:
          self.description = description
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
        if marked_as_favorite is not None:
          self.marked_as_favorite = marked_as_favorite
        if name is not None:
          self.name = name
        if owner is not None:
          self.owner = owner
        if parent_folder_id is not None:
          self.parent_folder_id = parent_folder_id
        if status_message is not None:
          self.status_message = status_message
        if type is not None:
          self.type = type
        if updated_at is not None:
          self.updated_at = updated_at

    @property
    def ancestors(self):
        """
        Gets the ancestors of this FolderOutputV1.
        The list of folder ancestors, starting at the topmost folder to which the user has access

        :return: The ancestors of this FolderOutputV1.
        :rtype: list[ItemPreviewV1]
        """
        return self._ancestors

    @ancestors.setter
    def ancestors(self, ancestors):
        """
        Sets the ancestors of this FolderOutputV1.
        The list of folder ancestors, starting at the topmost folder to which the user has access

        :param ancestors: The ancestors of this FolderOutputV1.
        :type: list[ItemPreviewV1]
        """

        self._ancestors = ancestors

    @property
    def created_at(self):
        """
        Gets the created_at of this FolderOutputV1.
        The ISO 8601 date of when the folder, workbook, or project was created (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :return: The created_at of this FolderOutputV1.
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this FolderOutputV1.
        The ISO 8601 date of when the folder, workbook, or project was created (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :param created_at: The created_at of this FolderOutputV1.
        :type: str
        """

        self._created_at = created_at

    @property
    def description(self):
        """
        Gets the description of this FolderOutputV1.
        Clarifying information or other plain language description of this item

        :return: The description of this FolderOutputV1.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FolderOutputV1.
        Clarifying information or other plain language description of this item

        :param description: The description of this FolderOutputV1.
        :type: str
        """

        self._description = description

    @property
    def effective_permissions(self):
        """
        Gets the effective_permissions of this FolderOutputV1.
        The permissions the current user has to the item.

        :return: The effective_permissions of this FolderOutputV1.
        :rtype: PermissionsV1
        """
        return self._effective_permissions

    @effective_permissions.setter
    def effective_permissions(self, effective_permissions):
        """
        Sets the effective_permissions of this FolderOutputV1.
        The permissions the current user has to the item.

        :param effective_permissions: The effective_permissions of this FolderOutputV1.
        :type: PermissionsV1
        """

        self._effective_permissions = effective_permissions

    @property
    def href(self):
        """
        Gets the href of this FolderOutputV1.
        The href that can be used to interact with the item

        :return: The href of this FolderOutputV1.
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """
        Sets the href of this FolderOutputV1.
        The href that can be used to interact with the item

        :param href: The href of this FolderOutputV1.
        :type: str
        """
        if href is None:
            raise ValueError("Invalid value for `href`, must not be `None`")

        self._href = href

    @property
    def id(self):
        """
        Gets the id of this FolderOutputV1.
        The ID that can be used to interact with the item

        :return: The id of this FolderOutputV1.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this FolderOutputV1.
        The ID that can be used to interact with the item

        :param id: The id of this FolderOutputV1.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def is_archived(self):
        """
        Gets the is_archived of this FolderOutputV1.
        Whether item is archived

        :return: The is_archived of this FolderOutputV1.
        :rtype: bool
        """
        return self._is_archived

    @is_archived.setter
    def is_archived(self, is_archived):
        """
        Sets the is_archived of this FolderOutputV1.
        Whether item is archived

        :param is_archived: The is_archived of this FolderOutputV1.
        :type: bool
        """

        self._is_archived = is_archived

    @property
    def is_redacted(self):
        """
        Gets the is_redacted of this FolderOutputV1.
        Whether item is redacted

        :return: The is_redacted of this FolderOutputV1.
        :rtype: bool
        """
        return self._is_redacted

    @is_redacted.setter
    def is_redacted(self, is_redacted):
        """
        Sets the is_redacted of this FolderOutputV1.
        Whether item is redacted

        :param is_redacted: The is_redacted of this FolderOutputV1.
        :type: bool
        """

        self._is_redacted = is_redacted

    @property
    def marked_as_favorite(self):
        """
        Gets the marked_as_favorite of this FolderOutputV1.
        Flag indicating whether this folder, workbook, or project has been marked as a favorite by the current user

        :return: The marked_as_favorite of this FolderOutputV1.
        :rtype: bool
        """
        return self._marked_as_favorite

    @marked_as_favorite.setter
    def marked_as_favorite(self, marked_as_favorite):
        """
        Sets the marked_as_favorite of this FolderOutputV1.
        Flag indicating whether this folder, workbook, or project has been marked as a favorite by the current user

        :param marked_as_favorite: The marked_as_favorite of this FolderOutputV1.
        :type: bool
        """

        self._marked_as_favorite = marked_as_favorite

    @property
    def name(self):
        """
        Gets the name of this FolderOutputV1.
        The human readable name

        :return: The name of this FolderOutputV1.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FolderOutputV1.
        The human readable name

        :param name: The name of this FolderOutputV1.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def owner(self):
        """
        Gets the owner of this FolderOutputV1.
        The owner of this folder, workbook, or project

        :return: The owner of this FolderOutputV1.
        :rtype: IdentityPreviewV1
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """
        Sets the owner of this FolderOutputV1.
        The owner of this folder, workbook, or project

        :param owner: The owner of this FolderOutputV1.
        :type: IdentityPreviewV1
        """

        self._owner = owner

    @property
    def parent_folder_id(self):
        """
        Gets the parent_folder_id of this FolderOutputV1.
        The ID of the parent folder which this folder, workbook, or project is a subfolder of

        :return: The parent_folder_id of this FolderOutputV1.
        :rtype: str
        """
        return self._parent_folder_id

    @parent_folder_id.setter
    def parent_folder_id(self, parent_folder_id):
        """
        Sets the parent_folder_id of this FolderOutputV1.
        The ID of the parent folder which this folder, workbook, or project is a subfolder of

        :param parent_folder_id: The parent_folder_id of this FolderOutputV1.
        :type: str
        """

        self._parent_folder_id = parent_folder_id

    @property
    def status_message(self):
        """
        Gets the status_message of this FolderOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :return: The status_message of this FolderOutputV1.
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """
        Sets the status_message of this FolderOutputV1.
        A plain language status message with information about any issues that may have been encountered during an operation

        :param status_message: The status_message of this FolderOutputV1.
        :type: str
        """

        self._status_message = status_message

    @property
    def type(self):
        """
        Gets the type of this FolderOutputV1.
        The type of the item

        :return: The type of this FolderOutputV1.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this FolderOutputV1.
        The type of the item

        :param type: The type of this FolderOutputV1.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")

        self._type = type

    @property
    def updated_at(self):
        """
        Gets the updated_at of this FolderOutputV1.
        The ISO 8601 date of when the folder, workbook, or project was updated (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :return: The updated_at of this FolderOutputV1.
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """
        Sets the updated_at of this FolderOutputV1.
        The ISO 8601 date of when the folder, workbook, or project was updated (YYYY-MM-DDThh:mm:ss.sssssssss±hh:mm)

        :param updated_at: The updated_at of this FolderOutputV1.
        :type: str
        """

        self._updated_at = updated_at

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
        if not isinstance(other, FolderOutputV1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
