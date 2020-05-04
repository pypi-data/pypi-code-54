from ..util import Model


class BodyWrapper(Model):
	def __init__(self):
		self.__users = None
		self.__key_modified = dict()

	def get_users(self):
		"""
		The method to get the users

		Returns:
			list: An instance of list
		"""
		return self.__users

	def set_users(self, users):
		"""
		The method to set the value to users

		Parameters:
			users (list) : An instance of list
		"""
		self.__users = users
		self.__key_modified["users"] = 1

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
