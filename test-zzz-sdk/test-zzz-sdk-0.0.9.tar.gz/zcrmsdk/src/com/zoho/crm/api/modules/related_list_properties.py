from ..util import Model


class RelatedListProperties(Model):
	def __init__(self):
		self.__sort_by = None
		self.__fields = None
		self.__sort_order = None
		self.__key_modified = dict()

	def get_sort_by(self):
		"""
		The method to get the sort_by

		Returns:
			string: A string value
		"""
		return self.__sort_by

	def set_sort_by(self, sort_by):
		"""
		The method to set the value to sort_by

		Parameters:
			sort_by (string) : A string value
		"""
		self.__sort_by = sort_by
		self.__key_modified["sort_by"] = 1

	def get_fields(self):
		"""
		The method to get the fields

		Returns:
			list: An instance of list
		"""
		return self.__fields

	def set_fields(self, fields):
		"""
		The method to set the value to fields

		Parameters:
			fields (list) : An instance of list
		"""
		self.__fields = fields
		self.__key_modified["fields"] = 1

	def get_sort_order(self):
		"""
		The method to get the sort_order

		Returns:
			string: A string value
		"""
		return self.__sort_order

	def set_sort_order(self, sort_order):
		"""
		The method to set the value to sort_order

		Parameters:
			sort_order (string) : A string value
		"""
		self.__sort_order = sort_order
		self.__key_modified["sort_order"] = 1

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
