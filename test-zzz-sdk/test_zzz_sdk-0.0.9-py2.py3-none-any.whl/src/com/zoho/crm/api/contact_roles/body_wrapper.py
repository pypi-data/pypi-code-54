from ..util import Model


class BodyWrapper(Model):
	def __init__(self):
		self.__contact_roles = None
		self.__key_modified = dict()

	def get_contact_roles(self):
		"""
		The method to get the contact_roles

		Returns:
			list: An instance of list
		"""
		return self.__contact_roles

	def set_contact_roles(self, contact_roles):
		"""
		The method to set the value to contact_roles

		Parameters:
			contact_roles (list) : An instance of list
		"""
		self.__contact_roles = contact_roles
		self.__key_modified["contact_roles"] = 1

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
