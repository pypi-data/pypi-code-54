from ..util import Model


class AutoNumber(Model):
	def __init__(self):
		self.__prefix = None
		self.__suffix = None
		self.__start_number = None
		self.__key_modified = dict()

	def get_prefix(self):
		"""
		The method to get the prefix

		Returns:
			string: A string value
		"""
		return self.__prefix

	def set_prefix(self, prefix):
		"""
		The method to set the value to prefix

		Parameters:
			prefix (string) : A string value
		"""
		self.__prefix = prefix
		self.__key_modified["prefix"] = 1

	def get_suffix(self):
		"""
		The method to get the suffix

		Returns:
			string: A string value
		"""
		return self.__suffix

	def set_suffix(self, suffix):
		"""
		The method to set the value to suffix

		Parameters:
			suffix (string) : A string value
		"""
		self.__suffix = suffix
		self.__key_modified["suffix"] = 1

	def get_start_number(self):
		"""
		The method to get the start_number

		Returns:
			int: A int value
		"""
		return self.__start_number

	def set_start_number(self, start_number):
		"""
		The method to set the value to start_number

		Parameters:
			start_number (int) : A int value
		"""
		self.__start_number = start_number
		self.__key_modified["start_number"] = 1

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
