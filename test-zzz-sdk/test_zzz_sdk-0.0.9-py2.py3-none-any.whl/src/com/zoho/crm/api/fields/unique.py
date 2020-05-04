from ..util import Model


class Unique(Model):
	def __init__(self):
		self.__casesensitive = None
		self.__key_modified = dict()

	def get_casesensitive(self):
		"""
		The method to get the casesensitive

		Returns:
			string: A string value
		"""
		return self.__casesensitive

	def set_casesensitive(self, casesensitive):
		"""
		The method to set the value to casesensitive

		Parameters:
			casesensitive (string) : A string value
		"""
		self.__casesensitive = casesensitive
		self.__key_modified["casesensitive"] = 1

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
