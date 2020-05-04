from ..util import Model

from .response_handler import ResponseHandler

class ResponseWrapper(Model, ResponseHandler):
	def __init__(self):
		self.__taxes = None
		self.__preference = None
		self.__key_modified = dict()

	def get_taxes(self):
		"""
		The method to get the taxes

		Returns:
			list: An instance of list
		"""
		return self.__taxes

	def set_taxes(self, taxes):
		"""
		The method to set the value to taxes

		Parameters:
			taxes (list) : An instance of list
		"""
		self.__taxes = taxes
		self.__key_modified["taxes"] = 1

	def get_preference(self):
		"""
		The method to get the preference

		Returns:
			Preference: An instance of Preference
		"""
		return self.__preference

	def set_preference(self, preference):
		"""
		The method to set the value to preference

		Parameters:
			preference (Preference) : An instance of Preference
		"""
		self.__preference = preference
		self.__key_modified["preference"] = 1

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
