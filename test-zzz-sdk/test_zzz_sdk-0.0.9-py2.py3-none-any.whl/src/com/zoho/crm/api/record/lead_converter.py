from ..util import Model


class LeadConverter(Model):
	def __init__(self):
		self.__overwrite = None
		self.__notify_lead_owner = None
		self.__notify_new_entity_owner = None
		self.__accounts = None
		self.__contacts = None
		self.__assign_to = None
		self.__deals = None
		self.__key_modified = dict()

	def get_overwrite(self):
		"""
		The method to get the overwrite

		Returns:
			bool: A bool value
		"""
		return self.__overwrite

	def set_overwrite(self, overwrite):
		"""
		The method to set the value to overwrite

		Parameters:
			overwrite (bool) : A bool value
		"""
		self.__overwrite = overwrite
		self.__key_modified["overwrite"] = 1

	def get_notify_lead_owner(self):
		"""
		The method to get the notify_lead_owner

		Returns:
			bool: A bool value
		"""
		return self.__notify_lead_owner

	def set_notify_lead_owner(self, notify_lead_owner):
		"""
		The method to set the value to notify_lead_owner

		Parameters:
			notify_lead_owner (bool) : A bool value
		"""
		self.__notify_lead_owner = notify_lead_owner
		self.__key_modified["notify_lead_owner"] = 1

	def get_notify_new_entity_owner(self):
		"""
		The method to get the notify_new_entity_owner

		Returns:
			bool: A bool value
		"""
		return self.__notify_new_entity_owner

	def set_notify_new_entity_owner(self, notify_new_entity_owner):
		"""
		The method to set the value to notify_new_entity_owner

		Parameters:
			notify_new_entity_owner (bool) : A bool value
		"""
		self.__notify_new_entity_owner = notify_new_entity_owner
		self.__key_modified["notify_new_entity_owner"] = 1

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

	def get_assign_to(self):
		"""
		The method to get the assign_to

		Returns:
			string: A string value
		"""
		return self.__assign_to

	def set_assign_to(self, assign_to):
		"""
		The method to set the value to assign_to

		Parameters:
			assign_to (string) : A string value
		"""
		self.__assign_to = assign_to
		self.__key_modified["assign_to"] = 1

	def get_deals(self):
		"""
		The method to get the deals

		Returns:
			Record: An instance of Record
		"""
		return self.__deals

	def set_deals(self, deals):
		"""
		The method to set the value to deals

		Parameters:
			deals (Record) : An instance of Record
		"""
		self.__deals = deals
		self.__key_modified["Deals"] = 1

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
