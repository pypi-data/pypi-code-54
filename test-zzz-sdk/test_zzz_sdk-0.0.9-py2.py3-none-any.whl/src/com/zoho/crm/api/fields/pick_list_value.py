from ..util import Model


class PickListValue(Model):
	def __init__(self):
		self.__display_value = None
		self.__actual_value = None
		self.__key_modified = dict()

	def get_display_value(self):
		"""
		The method to get the display_value

		Returns:
			string: A string value
		"""
		return self.__display_value

	def set_display_value(self, display_value):
		"""
		The method to set the value to display_value

		Parameters:
			display_value (string) : A string value
		"""
		self.__display_value = display_value
		self.__key_modified["display_value"] = 1

	def get_actual_value(self):
		"""
		The method to get the actual_value

		Returns:
			string: A string value
		"""
		return self.__actual_value

	def set_actual_value(self, actual_value):
		"""
		The method to set the value to actual_value

		Parameters:
			actual_value (string) : A string value
		"""
		self.__actual_value = actual_value
		self.__key_modified["actual_value"] = 1

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
