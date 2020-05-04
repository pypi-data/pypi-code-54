from ..util import Model


class Resource(Model):
	def __init__(self):
		self.__type = None
		self.__module = None
		self.__file_id = None
		self.__ignore_empty = None
		self.__find_by = None
		self.__field_mappings = None
		self.__file = None
		self.__key_modified = dict()

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

	def get_module(self):
		"""
		The method to get the module

		Returns:
			string: A string value
		"""
		return self.__module

	def set_module(self, module):
		"""
		The method to set the value to module

		Parameters:
			module (string) : A string value
		"""
		self.__module = module
		self.__key_modified["module"] = 1

	def get_file_id(self):
		"""
		The method to get the file_id

		Returns:
			string: A string value
		"""
		return self.__file_id

	def set_file_id(self, file_id):
		"""
		The method to set the value to file_id

		Parameters:
			file_id (string) : A string value
		"""
		self.__file_id = file_id
		self.__key_modified["file_id"] = 1

	def get_ignore_empty(self):
		"""
		The method to get the ignore_empty

		Returns:
			bool: A bool value
		"""
		return self.__ignore_empty

	def set_ignore_empty(self, ignore_empty):
		"""
		The method to set the value to ignore_empty

		Parameters:
			ignore_empty (bool) : A bool value
		"""
		self.__ignore_empty = ignore_empty
		self.__key_modified["ignore_empty"] = 1

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

	def get_field_mappings(self):
		"""
		The method to get the field_mappings

		Returns:
			list: An instance of list
		"""
		return self.__field_mappings

	def set_field_mappings(self, field_mappings):
		"""
		The method to set the value to field_mappings

		Parameters:
			field_mappings (list) : An instance of list
		"""
		self.__field_mappings = field_mappings
		self.__key_modified["field_mappings"] = 1

	def get_file(self):
		"""
		The method to get the file

		Returns:
			File: An instance of File
		"""
		return self.__file

	def set_file(self, file):
		"""
		The method to set the value to file

		Parameters:
			file (File) : An instance of File
		"""
		self.__file = file
		self.__key_modified["file"] = 1

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
