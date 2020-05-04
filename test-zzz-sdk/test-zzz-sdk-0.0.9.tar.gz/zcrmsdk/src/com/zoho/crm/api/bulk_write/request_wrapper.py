from ..util import Model


class RequestWrapper(Model):
	def __init__(self):
		self.__character_encoding = None
		self.__operation = None
		self.__callback = None
		self.__resource = None
		self.__key_modified = dict()

	def get_character_encoding(self):
		"""
		The method to get the character_encoding

		Returns:
			string: A string value
		"""
		return self.__character_encoding

	def set_character_encoding(self, character_encoding):
		"""
		The method to set the value to character_encoding

		Parameters:
			character_encoding (string) : A string value
		"""
		self.__character_encoding = character_encoding
		self.__key_modified["character_encoding"] = 1

	def get_operation(self):
		"""
		The method to get the operation

		Returns:
			string: A string value
		"""
		return self.__operation

	def set_operation(self, operation):
		"""
		The method to set the value to operation

		Parameters:
			operation (string) : A string value
		"""
		self.__operation = operation
		self.__key_modified["operation"] = 1

	def get_callback(self):
		"""
		The method to get the callback

		Returns:
			CallBack: An instance of CallBack
		"""
		return self.__callback

	def set_callback(self, callback):
		"""
		The method to set the value to callback

		Parameters:
			callback (CallBack) : An instance of CallBack
		"""
		self.__callback = callback
		self.__key_modified["callback"] = 1

	def get_resource(self):
		"""
		The method to get the resource

		Returns:
			Resource: An instance of Resource
		"""
		return self.__resource

	def set_resource(self, resource):
		"""
		The method to set the value to resource

		Parameters:
			resource (Resource) : An instance of Resource
		"""
		self.__resource = resource
		self.__key_modified["resource"] = 1

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
