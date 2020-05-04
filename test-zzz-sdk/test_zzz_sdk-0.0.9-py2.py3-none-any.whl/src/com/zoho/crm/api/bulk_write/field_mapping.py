from ..record import Record
from ..util import Model


class FieldMapping(Model):
	def __init__(self):
		self.__api_name = None
		self.__index = None
		self.__format = None
		self.__find_by = None
		self.__default_value = None
		self.__key_modified = dict()

	def get_api_name(self):
		"""
		The method to get the api_name

		Returns:
			string: A string value
		"""
		return self.__api_name

	def set_api_name(self, api_name):
		"""
		The method to set the value to api_name

		Parameters:
			api_name (string) : A string value
		"""
		self.__api_name = api_name
		self.__key_modified["api_name"] = 1

	def get_index(self):
		"""
		The method to get the index

		Returns:
			int: A int value
		"""
		return self.__index

	def set_index(self, index):
		"""
		The method to set the value to index

		Parameters:
			index (int) : A int value
		"""
		self.__index = index
		self.__key_modified["index"] = 1

	def get_format(self):
		"""
		The method to get the format

		Returns:
			string: A string value
		"""
		return self.__format

	def set_format(self, format):
		"""
		The method to set the value to format

		Parameters:
			format (string) : A string value
		"""
		self.__format = format
		self.__key_modified["format"] = 1

	def get_find_by(self):
		"""
		The method to get the find_by

		Returns:
			string: A string value
		"""
		return self.__find_by

	def set_find_by(self, find_by):
		"""
		The method to set the value to find_by

		Parameters:
			find_by (string) : A string value
		"""
		self.__find_by = find_by
		self.__key_modified["find_by"] = 1

	def get_default_value(self):
		"""
		The method to get the default_value

		Returns:
			Record: An instance of Record
		"""
		return self.__default_value

	def set_default_value(self, default_value):
		"""
		The method to set the value to default_value

		Parameters:
			default_value (Record) : An instance of Record
		"""
		self.__default_value = default_value
		self.__key_modified["default_value"] = 1

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
