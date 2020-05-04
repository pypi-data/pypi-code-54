from ..util import Model


class ConflictWrapper(Model):
	def __init__(self):
		self.__conflict_id = None
		self.__key_modified = dict()

	def get_conflict_id(self):
		"""
		The method to get the conflict_id

		Returns:
			string: A string value
		"""
		return self.__conflict_id

	def set_conflict_id(self, conflict_id):
		"""
		The method to set the value to conflict_id

		Parameters:
			conflict_id (string) : A string value
		"""
		self.__conflict_id = conflict_id
		self.__key_modified["conflict_id"] = 1

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
