from ..util import Model

from .count_handler import CountHandler

class CountWrapper(Model, CountHandler):
	def __init__(self):
		self.__count = None
		self.__key_modified = dict()

	def get_count(self):
		"""
		The method to get the count

		Returns:
			string: A string value
		"""
		return self.__count

	def set_count(self, count):
		"""
		The method to set the value to count

		Parameters:
			count (string) : A string value
		"""
		self.__count = count
		self.__key_modified["count"] = 1

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
