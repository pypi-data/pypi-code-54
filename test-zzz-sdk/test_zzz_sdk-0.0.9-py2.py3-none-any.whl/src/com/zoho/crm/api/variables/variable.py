from ..variable_groups import VariableGroup
from ..util import Model


class Variable(Model):
	def __init__(self):
		self.__id = None
		self.__api_name = None
		self.__name = None
		self.__description = None
		self.__type = None
		self.__value = None
		self.__variable_group = None
		self.__key_modified = dict()

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

	def get_name(self):
		"""
		The method to get the name

		Returns:
			string: A string value
		"""
		return self.__name

	def set_name(self, name):
		"""
		The method to set the value to name

		Parameters:
			name (string) : A string value
		"""
		self.__name = name
		self.__key_modified["name"] = 1

	def get_description(self):
		"""
		The method to get the description

		Returns:
			string: A string value
		"""
		return self.__description

	def set_description(self, description):
		"""
		The method to set the value to description

		Parameters:
			description (string) : A string value
		"""
		self.__description = description
		self.__key_modified["description"] = 1

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

	def get_value(self):
		"""
		The method to get the value

		Returns:
			string: A string value
		"""
		return self.__value

	def set_value(self, value):
		"""
		The method to set the value to value

		Parameters:
			value (string) : A string value
		"""
		self.__value = value
		self.__key_modified["value"] = 1

	def get_variable_group(self):
		"""
		The method to get the variable_group

		Returns:
			VariableGroup: An instance of VariableGroup
		"""
		return self.__variable_group

	def set_variable_group(self, variable_group):
		"""
		The method to set the value to variable_group

		Parameters:
			variable_group (VariableGroup) : An instance of VariableGroup
		"""
		self.__variable_group = variable_group
		self.__key_modified["variable_group"] = 1

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
