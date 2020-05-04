from ..util import Model

from .action_handler import ActionHandler

class ActionWrapper(Model, ActionHandler):
	def __init__(self):
		self.__tags = None
		self.__key_modified = dict()

	def get_tags(self):
		"""
		The method to get the tags

		Returns:
			list: An instance of list
		"""
		return self.__tags

	def set_tags(self, tags):
		"""
		The method to set the value to tags

		Parameters:
			tags (list) : An instance of list
		"""
		self.__tags = tags
		self.__key_modified["tags"] = 1

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
