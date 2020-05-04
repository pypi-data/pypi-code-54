from ..util import Model


class ResponseWrapper(Model):
	def __init__(self):
		self.__blueprint = None
		self.__key_modified = dict()

	def get_blueprint(self):
		"""
		The method to get the blueprint

		Returns:
			list: An instance of list
		"""
		return self.__blueprint

	def set_blueprint(self, blueprint):
		"""
		The method to set the value to blueprint

		Parameters:
			blueprint (list) : An instance of list
		"""
		self.__blueprint = blueprint
		self.__key_modified["blueprint"] = 1

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
