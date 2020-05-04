from ..profile import Profile
from ..users import User
from ..util import Model


class Layout(Model):
	def __init__(self):
		self.__id = None
		self.__name = None
		self.__status = None
		self.__modified_time = None
		self.__created_for = None
		self.__created_by = None
		self.__modified_by = None
		self.__profiles = None
		self.__sections = None
		self.__visible = None
		self.__convert_mapping = None
		self.__key_modified = dict()

	def get_id(self):
		"""
		The method to get the id

		Returns:
			string: A string value
		"""
		return self.__id

	def set_id(self, id):
		"""
		The method to set the value to id

		Parameters:
			id (string) : A string value
		"""
		self.__id = id
		self.__key_modified["id"] = 1

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

	def get_status(self):
		"""
		The method to get the status

		Returns:
			int: A int value
		"""
		return self.__status

	def set_status(self, status):
		"""
		The method to set the value to status

		Parameters:
			status (int) : A int value
		"""
		self.__status = status
		self.__key_modified["status"] = 1

	def get_modified_time(self):
		"""
		The method to get the modified_time

		Returns:
			DateTime: An instance of DateTime
		"""
		return self.__modified_time

	def set_modified_time(self, modified_time):
		"""
		The method to set the value to modified_time

		Parameters:
			modified_time (DateTime) : An instance of DateTime
		"""
		self.__modified_time = modified_time
		self.__key_modified["modified_time"] = 1

	def get_created_for(self):
		"""
		The method to get the created_for

		Returns:
			User: An instance of User
		"""
		return self.__created_for

	def set_created_for(self, created_for):
		"""
		The method to set the value to created_for

		Parameters:
			created_for (User) : An instance of User
		"""
		self.__created_for = created_for
		self.__key_modified["created_for"] = 1

	def get_created_by(self):
		"""
		The method to get the created_by

		Returns:
			User: An instance of User
		"""
		return self.__created_by

	def set_created_by(self, created_by):
		"""
		The method to set the value to created_by

		Parameters:
			created_by (User) : An instance of User
		"""
		self.__created_by = created_by
		self.__key_modified["created_by"] = 1

	def get_modified_by(self):
		"""
		The method to get the modified_by

		Returns:
			User: An instance of User
		"""
		return self.__modified_by

	def set_modified_by(self, modified_by):
		"""
		The method to set the value to modified_by

		Parameters:
			modified_by (User) : An instance of User
		"""
		self.__modified_by = modified_by
		self.__key_modified["modified_by"] = 1

	def get_profiles(self):
		"""
		The method to get the profiles

		Returns:
			list: An instance of list
		"""
		return self.__profiles

	def set_profiles(self, profiles):
		"""
		The method to set the value to profiles

		Parameters:
			profiles (list) : An instance of list
		"""
		self.__profiles = profiles
		self.__key_modified["profiles"] = 1

	def get_sections(self):
		"""
		The method to get the sections

		Returns:
			list: An instance of list
		"""
		return self.__sections

	def set_sections(self, sections):
		"""
		The method to set the value to sections

		Parameters:
			sections (list) : An instance of list
		"""
		self.__sections = sections
		self.__key_modified["sections"] = 1

	def get_visible(self):
		"""
		The method to get the visible

		Returns:
			bool: A bool value
		"""
		return self.__visible

	def set_visible(self, visible):
		"""
		The method to set the value to visible

		Parameters:
			visible (bool) : A bool value
		"""
		self.__visible = visible
		self.__key_modified["visible"] = 1

	def get_convert_mapping(self):
		"""
		The method to get the convert_mapping

		Returns:
			dict: An instance of dict
		"""
		return self.__convert_mapping

	def set_convert_mapping(self, convert_mapping):
		"""
		The method to set the value to convert_mapping

		Parameters:
			convert_mapping (dict) : An instance of dict
		"""
		self.__convert_mapping = convert_mapping
		self.__key_modified["convert_mapping"] = 1

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
