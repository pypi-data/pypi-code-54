from ..attachments import Attachment
from ..users import User
from ..util import Model


class Note(Model):
	def __init__(self):
		self.__id = None
		self.__note_title = None
		self.__note_content = None
		self.__modified_time = None
		self.__created_time = None
		self.__parent_id = None
		self.__owner = None
		self.__created_by = None
		self.__modified_by = None
		self.__editable = None
		self.__se_module = None
		self.__is_shared_to_client = None
		self.__size = None
		self.__state = None
		self.__voice_note = None
		self.__attachments = None
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

	def get_note_title(self):
		"""
		The method to get the note_title

		Returns:
			string: A string value
		"""
		return self.__note_title

	def set_note_title(self, note_title):
		"""
		The method to set the value to note_title

		Parameters:
			note_title (string) : A string value
		"""
		self.__note_title = note_title
		self.__key_modified["Note_Title"] = 1

	def get_note_content(self):
		"""
		The method to get the note_content

		Returns:
			string: A string value
		"""
		return self.__note_content

	def set_note_content(self, note_content):
		"""
		The method to set the value to note_content

		Parameters:
			note_content (string) : A string value
		"""
		self.__note_content = note_content
		self.__key_modified["Note_Content"] = 1

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
		self.__key_modified["Modified_Time"] = 1

	def get_created_time(self):
		"""
		The method to get the created_time

		Returns:
			DateTime: An instance of DateTime
		"""
		return self.__created_time

	def set_created_time(self, created_time):
		"""
		The method to set the value to created_time

		Parameters:
			created_time (DateTime) : An instance of DateTime
		"""
		self.__created_time = created_time
		self.__key_modified["Created_Time"] = 1

	def get_parent_id(self):
		"""
		The method to get the parent_id

		Returns:
			dict: An instance of dict
		"""
		return self.__parent_id

	def set_parent_id(self, parent_id):
		"""
		The method to set the value to parent_id

		Parameters:
			parent_id (dict) : An instance of dict
		"""
		self.__parent_id = parent_id
		self.__key_modified["Parent_Id"] = 1

	def get_owner(self):
		"""
		The method to get the owner

		Returns:
			User: An instance of User
		"""
		return self.__owner

	def set_owner(self, owner):
		"""
		The method to set the value to owner

		Parameters:
			owner (User) : An instance of User
		"""
		self.__owner = owner
		self.__key_modified["Owner"] = 1

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
		self.__key_modified["Created_By"] = 1

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
		self.__key_modified["Modified_By"] = 1

	def get_editable(self):
		"""
		The method to get the editable

		Returns:
			bool: A bool value
		"""
		return self.__editable

	def set_editable(self, editable):
		"""
		The method to set the value to editable

		Parameters:
			editable (bool) : A bool value
		"""
		self.__editable = editable
		self.__key_modified["$editable"] = 1

	def get_se_module(self):
		"""
		The method to get the se_module

		Returns:
			string: A string value
		"""
		return self.__se_module

	def set_se_module(self, se_module):
		"""
		The method to set the value to se_module

		Parameters:
			se_module (string) : A string value
		"""
		self.__se_module = se_module
		self.__key_modified["$se_module"] = 1

	def get_is_shared_to_client(self):
		"""
		The method to get the is_shared_to_client

		Returns:
			bool: A bool value
		"""
		return self.__is_shared_to_client

	def set_is_shared_to_client(self, is_shared_to_client):
		"""
		The method to set the value to is_shared_to_client

		Parameters:
			is_shared_to_client (bool) : A bool value
		"""
		self.__is_shared_to_client = is_shared_to_client
		self.__key_modified["$is_shared_to_client"] = 1

	def get_size(self):
		"""
		The method to get the size

		Returns:
			string: A string value
		"""
		return self.__size

	def set_size(self, size):
		"""
		The method to set the value to size

		Parameters:
			size (string) : A string value
		"""
		self.__size = size
		self.__key_modified["$size"] = 1

	def get_state(self):
		"""
		The method to get the state

		Returns:
			string: A string value
		"""
		return self.__state

	def set_state(self, state):
		"""
		The method to set the value to state

		Parameters:
			state (string) : A string value
		"""
		self.__state = state
		self.__key_modified["$state"] = 1

	def get_voice_note(self):
		"""
		The method to get the voice_note

		Returns:
			bool: A bool value
		"""
		return self.__voice_note

	def set_voice_note(self, voice_note):
		"""
		The method to set the value to voice_note

		Parameters:
			voice_note (bool) : A bool value
		"""
		self.__voice_note = voice_note
		self.__key_modified["$voice_note"] = 1

	def get_attachments(self):
		"""
		The method to get the attachments

		Returns:
			list: An instance of list
		"""
		return self.__attachments

	def set_attachments(self, attachments):
		"""
		The method to set the value to attachments

		Parameters:
			attachments (list) : An instance of list
		"""
		self.__attachments = attachments
		self.__key_modified["$attachments"] = 1

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
