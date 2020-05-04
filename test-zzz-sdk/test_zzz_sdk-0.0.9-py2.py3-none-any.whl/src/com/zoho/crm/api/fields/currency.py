from ..util import Model


class Currency(Model):
	def __init__(self):
		self.__rounding_option = None
		self.__precision = None
		self.__key_modified = dict()

	def get_rounding_option(self):
		"""
		The method to get the rounding_option

		Returns:
			string: A string value
		"""
		return self.__rounding_option

	def set_rounding_option(self, rounding_option):
		"""
		The method to set the value to rounding_option

		Parameters:
			rounding_option (string) : A string value
		"""
		self.__rounding_option = rounding_option
		self.__key_modified["rounding_option"] = 1

	def get_precision(self):
		"""
		The method to get the precision

		Returns:
			int: A int value
		"""
		return self.__precision

	def set_precision(self, precision):
		"""
		The method to set the value to precision

		Parameters:
			precision (int) : A int value
		"""
		self.__precision = precision
		self.__key_modified["precision"] = 1

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
