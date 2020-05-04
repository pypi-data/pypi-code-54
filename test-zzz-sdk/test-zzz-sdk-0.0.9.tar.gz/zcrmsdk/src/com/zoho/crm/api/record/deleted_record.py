from ..users import User
from ..util import Model

from .deleted_records_response import DeletedRecordsResponse

class DeletedRecord(Model, DeletedRecordsResponse):
	def __init__(self):
		self.__deleted_by = None
		self.__created_by = None
		self.__id = None
		self.__display_name = None
		self.__type = None
		self.__deleted_time = None
		self.__key_modified = dict()

	def get_deleted_by(self):
		"""
		The method to get the deleted_by

		Returns:
			User: An instance of User
		"""
		return self.__deleted_by

	def set_deleted_by(self, deleted_by):
		"""
		The method to set the value to deleted_by

		Parameters:
			deleted_by (User) : An instance of User
		"""
		self.__deleted_by = deleted_by
		self.__key_modified["deleted_by"] = 1

	def get_created_by(self):
		"""
		The method to get the created_by

		Returns:
			User: An instance of User
		"""
		return self.__created_by

	def set_created_by(self, created_by):
		"""
		The method to set the value to created_by

		Parameters:
			created_by (User) : An instance of User
		"""
		self.__created_by = created_by
		self.__key_modified["created_by"] = 1

	def get_id(self):
		"""
		The method to get the id

		Returns:
			string: A string value
		"""
		return self.__id

	def set_id(self, id):
		"""
		The method to set the value to id

		Parameters:
			id (string) : A string value
		"""
		self.__id = id
		self.__key_modified["id"] = 1

	def get_display_name(self):
		"""
		The method to get the display_name

		Returns:
			string: A string value
		"""
		return self.__display_name

	def set_display_name(self, display_name):
		"""
		The method to set the value to display_name

		Parameters:
			display_name (string) : A string value
		"""
		self.__display_name = display_name
		self.__key_modified["display_name"] = 1

	def get_type(self):
		"""
		The method to get the type

		Returns:
			string: A string value
		"""
		return self.__type

	def set_type(self, type):
		"""
		The method to set the value to type

		Parameters:
			type (string) : A string value
		"""
		self.__type = type
		self.__key_modified["type"] = 1

	def get_deleted_time(self):
		"""
		The method to get the deleted_time

		Returns:
			DateTime: An instance of DateTime
		"""
		return self.__deleted_time

	def set_deleted_time(self, deleted_time):
		"""
		The method to set the value to deleted_time

		Parameters:
			deleted_time (DateTime) : An instance of DateTime
		"""
		self.__deleted_time = deleted_time
		self.__key_modified["deleted_time"] = 1

	def is_key_modified(self, key):
		"""
		The method to check if the user has modified the given key

		Parameters:
			key (string) : A string value

		Returns:
			int: A int value
		"""
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		"""
		The method to mark the given key as modified

		Parameters:
			modification (int) : A int value
			key (string) : A string value
		"""
		self.__key_modified[key] = modification
