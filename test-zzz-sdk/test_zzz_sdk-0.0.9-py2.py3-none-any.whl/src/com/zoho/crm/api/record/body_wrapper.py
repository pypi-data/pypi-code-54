from ..util import Model


class BodyWrapper(Model):
	def __init__(self):
		self.__data = None
		self.__trigger = None
		self.__lar_id = None
		self.__key_modified = dict()

	def get_data(self):
		"""
		The method to get the data

		Returns:
			list: An instance of list
		"""
		return self.__data

	def set_data(self, data):
		"""
		The method to set the value to data

		Parameters:
			data (list) : An instance of list
		"""
		self.__data = data
		self.__key_modified["data"] = 1

	def get_trigger(self):
		"""
		The method to get the trigger

		Returns:
			list: An instance of list
		"""
		return self.__trigger

	def set_trigger(self, trigger):
		"""
		The method to set the value to trigger

		Parameters:
			trigger (list) : An instance of list
		"""
		self.__trigger = trigger
		self.__key_modified["trigger"] = 1

	def get_lar_id(self):
		"""
		The method to get the lar_id

		Returns:
			string: A string value
		"""
		return self.__lar_id

	def set_lar_id(self, lar_id):
		"""
		The method to set the value to lar_id

		Parameters:
			lar_id (string) : A string value
		"""
		self.__lar_id = lar_id
		self.__key_modified["lar_id"] = 1

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
