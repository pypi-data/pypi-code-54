from ..util import Model


class ProcessInfo(Model):
	def __init__(self):
		self.__field_id = None
		self.__is_continuous = None
		self.__api_name = None
		self.__continuous = None
		self.__field_label = None
		self.__name = None
		self.__column_name = None
		self.__field_value = None
		self.__id = None
		self.__field_name = None
		self.__key_modified = dict()

	def get_field_id(self):
		"""
		The method to get the field_id

		Returns:
			string: A string value
		"""
		return self.__field_id

	def set_field_id(self, field_id):
		"""
		The method to set the value to field_id

		Parameters:
			field_id (string) : A string value
		"""
		self.__field_id = field_id
		self.__key_modified["field_id"] = 1

	def get_is_continuous(self):
		"""
		The method to get the is_continuous

		Returns:
			bool: A bool value
		"""
		return self.__is_continuous

	def set_is_continuous(self, is_continuous):
		"""
		The method to set the value to is_continuous

		Parameters:
			is_continuous (bool) : A bool value
		"""
		self.__is_continuous = is_continuous
		self.__key_modified["is_continuous"] = 1

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

	def get_continuous(self):
		"""
		The method to get the continuous

		Returns:
			bool: A bool value
		"""
		return self.__continuous

	def set_continuous(self, continuous):
		"""
		The method to set the value to continuous

		Parameters:
			continuous (bool) : A bool value
		"""
		self.__continuous = continuous
		self.__key_modified["continuous"] = 1

	def get_field_label(self):
		"""
		The method to get the field_label

		Returns:
			string: A string value
		"""
		return self.__field_label

	def set_field_label(self, field_label):
		"""
		The method to set the value to field_label

		Parameters:
			field_label (string) : A string value
		"""
		self.__field_label = field_label
		self.__key_modified["field_label"] = 1

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

	def get_column_name(self):
		"""
		The method to get the column_name

		Returns:
			string: A string value
		"""
		return self.__column_name

	def set_column_name(self, column_name):
		"""
		The method to set the value to column_name

		Parameters:
			column_name (string) : A string value
		"""
		self.__column_name = column_name
		self.__key_modified["column_name"] = 1

	def get_field_value(self):
		"""
		The method to get the field_value

		Returns:
			string: A string value
		"""
		return self.__field_value

	def set_field_value(self, field_value):
		"""
		The method to set the value to field_value

		Parameters:
			field_value (string) : A string value
		"""
		self.__field_value = field_value
		self.__key_modified["field_value"] = 1

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

	def get_field_name(self):
		"""
		The method to get the field_name

		Returns:
			string: A string value
		"""
		return self.__field_name

	def set_field_name(self, field_name):
		"""
		The method to set the value to field_name

		Parameters:
			field_name (string) : A string value
		"""
		self.__field_name = field_name
		self.__key_modified["field_name"] = 1

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
