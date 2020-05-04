from ..util import Model

from .response_handler import ResponseHandler

class ResponseWrapper(Model, ResponseHandler):
	def __init__(self):
		self.__modules = None
		self.__key_modified = dict()

	def get_modules(self):
		"""
		The method to get the modules

		Returns:
			list: An instance of list
		"""
		return self.__modules

	def set_modules(self, modules):
		"""
		The method to set the value to modules

		Parameters:
			modules (list) : An instance of list
		"""
		self.__modules = modules
		self.__key_modified["modules"] = 1

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
