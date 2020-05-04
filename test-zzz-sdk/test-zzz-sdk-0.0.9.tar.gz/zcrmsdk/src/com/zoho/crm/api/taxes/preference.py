from ..util import Model


class Preference(Model):
	def __init__(self):
		self.__auto_populate_tax = None
		self.__modify_tax_rates = None
		self.__key_modified = dict()

	def get_auto_populate_tax(self):
		"""
		The method to get the auto_populate_tax

		Returns:
			bool: A bool value
		"""
		return self.__auto_populate_tax

	def set_auto_populate_tax(self, auto_populate_tax):
		"""
		The method to set the value to auto_populate_tax

		Parameters:
			auto_populate_tax (bool) : A bool value
		"""
		self.__auto_populate_tax = auto_populate_tax
		self.__key_modified["auto_populate_tax"] = 1

	def get_modify_tax_rates(self):
		"""
		The method to get the modify_tax_rates

		Returns:
			bool: A bool value
		"""
		return self.__modify_tax_rates

	def set_modify_tax_rates(self, modify_tax_rates):
		"""
		The method to set the value to modify_tax_rates

		Parameters:
			modify_tax_rates (bool) : A bool value
		"""
		self.__modify_tax_rates = modify_tax_rates
		self.__key_modified["modify_tax_rates"] = 1

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
