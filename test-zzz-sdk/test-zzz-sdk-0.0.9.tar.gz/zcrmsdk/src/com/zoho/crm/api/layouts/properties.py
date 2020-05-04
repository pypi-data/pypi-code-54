from ..fields import ToolTip
from ..util import Model


class Properties(Model):
	def __init__(self):
		self.__reorder_rows = None
		self.__tooltip = None
		self.__maximum_rows = None
		self.__key_modified = dict()

	def get_reorder_rows(self):
		"""
		The method to get the reorder_rows

		Returns:
			bool: A bool value
		"""
		return self.__reorder_rows

	def set_reorder_rows(self, reorder_rows):
		"""
		The method to set the value to reorder_rows

		Parameters:
			reorder_rows (bool) : A bool value
		"""
		self.__reorder_rows = reorder_rows
		self.__key_modified["reorder_rows"] = 1

	def get_tooltip(self):
		"""
		The method to get the tooltip

		Returns:
			ToolTip: An instance of ToolTip
		"""
		return self.__tooltip

	def set_tooltip(self, tooltip):
		"""
		The method to set the value to tooltip

		Parameters:
			tooltip (ToolTip) : An instance of ToolTip
		"""
		self.__tooltip = tooltip
		self.__key_modified["tooltip"] = 1

	def get_maximum_rows(self):
		"""
		The method to get the maximum_rows

		Returns:
			int: A int value
		"""
		return self.__maximum_rows

	def set_maximum_rows(self, maximum_rows):
		"""
		The method to set the value to maximum_rows

		Parameters:
			maximum_rows (int) : A int value
		"""
		self.__maximum_rows = maximum_rows
		self.__key_modified["maximum_rows"] = 1

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
