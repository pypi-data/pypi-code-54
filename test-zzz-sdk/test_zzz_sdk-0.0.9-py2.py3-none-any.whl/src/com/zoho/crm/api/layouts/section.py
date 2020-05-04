from ..fields import Field
from ..util import Model


class Section(Model):
	def __init__(self):
		self.__display_label = None
		self.__api_name = None
		self.__name = None
		self.__generated_type = None
		self.__sequence_number = None
		self.__column_count = None
		self.__tab_traversal = None
		self.__issubformsection = None
		self.__fields = None
		self.__properties = None
		self.__key_modified = dict()

	def get_display_label(self):
		"""
		The method to get the display_label

		Returns:
			string: A string value
		"""
		return self.__display_label

	def set_display_label(self, display_label):
		"""
		The method to set the value to display_label

		Parameters:
			display_label (string) : A string value
		"""
		self.__display_label = display_label
		self.__key_modified["display_label"] = 1

	def get_api_name(self):
		"""
		The method to get the api_name

		Returns:
			string: A string value
		"""
		return self.__api_name

	def set_api_name(self, api_name):
		"""
		The method to set the value to api_name

		Parameters:
			api_name (string) : A string value
		"""
		self.__api_name = api_name
		self.__key_modified["api_name"] = 1

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

	def get_generated_type(self):
		"""
		The method to get the generated_type

		Returns:
			string: A string value
		"""
		return self.__generated_type

	def set_generated_type(self, generated_type):
		"""
		The method to set the value to generated_type

		Parameters:
			generated_type (string) : A string value
		"""
		self.__generated_type = generated_type
		self.__key_modified["generated_type"] = 1

	def get_sequence_number(self):
		"""
		The method to get the sequence_number

		Returns:
			int: A int value
		"""
		return self.__sequence_number

	def set_sequence_number(self, sequence_number):
		"""
		The method to set the value to sequence_number

		Parameters:
			sequence_number (int) : A int value
		"""
		self.__sequence_number = sequence_number
		self.__key_modified["sequence_number"] = 1

	def get_column_count(self):
		"""
		The method to get the column_count

		Returns:
			int: A int value
		"""
		return self.__column_count

	def set_column_count(self, column_count):
		"""
		The method to set the value to column_count

		Parameters:
			column_count (int) : A int value
		"""
		self.__column_count = column_count
		self.__key_modified["column_count"] = 1

	def get_tab_traversal(self):
		"""
		The method to get the tab_traversal

		Returns:
			int: A int value
		"""
		return self.__tab_traversal

	def set_tab_traversal(self, tab_traversal):
		"""
		The method to set the value to tab_traversal

		Parameters:
			tab_traversal (int) : A int value
		"""
		self.__tab_traversal = tab_traversal
		self.__key_modified["tab_traversal"] = 1

	def get_issubformsection(self):
		"""
		The method to get the issubformsection

		Returns:
			bool: A bool value
		"""
		return self.__issubformsection

	def set_issubformsection(self, issubformsection):
		"""
		The method to set the value to issubformsection

		Parameters:
			issubformsection (bool) : A bool value
		"""
		self.__issubformsection = issubformsection
		self.__key_modified["isSubformSection"] = 1

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

	def get_properties(self):
		"""
		The method to get the properties

		Returns:
			Properties: An instance of Properties
		"""
		return self.__properties

	def set_properties(self, properties):
		"""
		The method to set the value to properties

		Parameters:
			properties (Properties) : An instance of Properties
		"""
		self.__properties = properties
		self.__key_modified["properties"] = 1

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
