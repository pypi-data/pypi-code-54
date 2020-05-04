from ..util import Model

from .convert_action_response import ConvertActionResponse

class SuccessfulConvert(Model, ConvertActionResponse):
	def __init__(self):
		self.__contacts = None
		self.__deals = None
		self.__accounts = None
		self.__key_modified = dict()

	def get_contacts(self):
		"""
		The method to get the contacts

		Returns:
			string: A string value
		"""
		return self.__contacts

	def set_contacts(self, contacts):
		"""
		The method to set the value to contacts

		Parameters:
			contacts (string) : A string value
		"""
		self.__contacts = contacts
		self.__key_modified["Contacts"] = 1

	def get_deals(self):
		"""
		The method to get the deals

		Returns:
			string: A string value
		"""
		return self.__deals

	def set_deals(self, deals):
		"""
		The method to set the value to deals

		Parameters:
			deals (string) : A string value
		"""
		self.__deals = deals
		self.__key_modified["Deals"] = 1

	def get_accounts(self):
		"""
		The method to get the accounts

		Returns:
			string: A string value
		"""
		return self.__accounts

	def set_accounts(self, accounts):
		"""
		The method to set the value to accounts

		Parameters:
			accounts (string) : A string value
		"""
		self.__accounts = accounts
		self.__key_modified["Accounts"] = 1

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
