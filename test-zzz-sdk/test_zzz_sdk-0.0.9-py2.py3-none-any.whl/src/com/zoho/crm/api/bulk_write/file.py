from ..util import Model


class File(Model):
	def __init__(self):
		self.__status = None
		self.__name = None
		self.__added_count = None
		self.__skipped_count = None
		self.__updated_count = None
		self.__total_count = None
		self.__key_modified = dict()

	def get_status(self):
		"""
		The method to get the status

		Returns:
			string: A string value
		"""
		return self.__status

	def set_status(self, status):
		"""
		The method to set the value to status

		Parameters:
			status (string) : A string value
		"""
		self.__status = status
		self.__key_modified["status"] = 1

	def get_name(self):
		"""
		The method to get the name

		Returns:
			string: A string value
		"""
		return self.__name

	def set_name(self, name):
		"""
		The method to set the value to name

		Parameters:
			name (string) : A string value
		"""
		self.__name = name
		self.__key_modified["name"] = 1

	def get_added_count(self):
		"""
		The method to get the added_count

		Returns:
			int: A int value
		"""
		return self.__added_count

	def set_added_count(self, added_count):
		"""
		The method to set the value to added_count

		Parameters:
			added_count (int) : A int value
		"""
		self.__added_count = added_count
		self.__key_modified["added_count"] = 1

	def get_skipped_count(self):
		"""
		The method to get the skipped_count

		Returns:
			int: A int value
		"""
		return self.__skipped_count

	def set_skipped_count(self, skipped_count):
		"""
		The method to set the value to skipped_count

		Parameters:
			skipped_count (int) : A int value
		"""
		self.__skipped_count = skipped_count
		self.__key_modified["skipped_count"] = 1

	def get_updated_count(self):
		"""
		The method to get the updated_count

		Returns:
			int: A int value
		"""
		return self.__updated_count

	def set_updated_count(self, updated_count):
		"""
		The method to set the value to updated_count

		Parameters:
			updated_count (int) : A int value
		"""
		self.__updated_count = updated_count
		self.__key_modified["updated_count"] = 1

	def get_total_count(self):
		"""
		The method to get the total_count

		Returns:
			int: A int value
		"""
		return self.__total_count

	def set_total_count(self, total_count):
		"""
		The method to set the value to total_count

		Parameters:
			total_count (int) : A int value
		"""
		self.__total_count = total_count
		self.__key_modified["total_count"] = 1

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
