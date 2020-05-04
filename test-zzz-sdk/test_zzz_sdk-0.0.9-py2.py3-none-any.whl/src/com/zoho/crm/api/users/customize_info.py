from ..util import Model


class CustomizeInfo(Model):
	def __init__(self):
		self.__notes_desc = None
		self.__show_right_panel = None
		self.__unpin_recent_item = None
		self.__bc_view = None
		self.__show_home = None
		self.__show_detail_view = None
		self.__key_modified = dict()

	def get_notes_desc(self):
		"""
		The method to get the notes_desc

		Returns:
			bool: A bool value
		"""
		return self.__notes_desc

	def set_notes_desc(self, notes_desc):
		"""
		The method to set the value to notes_desc

		Parameters:
			notes_desc (bool) : A bool value
		"""
		self.__notes_desc = notes_desc
		self.__key_modified["notes_desc"] = 1

	def get_show_right_panel(self):
		"""
		The method to get the show_right_panel

		Returns:
			string: A string value
		"""
		return self.__show_right_panel

	def set_show_right_panel(self, show_right_panel):
		"""
		The method to set the value to show_right_panel

		Parameters:
			show_right_panel (string) : A string value
		"""
		self.__show_right_panel = show_right_panel
		self.__key_modified["show_right_panel"] = 1

	def get_unpin_recent_item(self):
		"""
		The method to get the unpin_recent_item

		Returns:
			string: A string value
		"""
		return self.__unpin_recent_item

	def set_unpin_recent_item(self, unpin_recent_item):
		"""
		The method to set the value to unpin_recent_item

		Parameters:
			unpin_recent_item (string) : A string value
		"""
		self.__unpin_recent_item = unpin_recent_item
		self.__key_modified["unpin_recent_item"] = 1

	def get_bc_view(self):
		"""
		The method to get the bc_view

		Returns:
			string: A string value
		"""
		return self.__bc_view

	def set_bc_view(self, bc_view):
		"""
		The method to set the value to bc_view

		Parameters:
			bc_view (string) : A string value
		"""
		self.__bc_view = bc_view
		self.__key_modified["bc_view"] = 1

	def get_show_home(self):
		"""
		The method to get the show_home

		Returns:
			bool: A bool value
		"""
		return self.__show_home

	def set_show_home(self, show_home):
		"""
		The method to set the value to show_home

		Parameters:
			show_home (bool) : A bool value
		"""
		self.__show_home = show_home
		self.__key_modified["show_home"] = 1

	def get_show_detail_view(self):
		"""
		The method to get the show_detail_view

		Returns:
			bool: A bool value
		"""
		return self.__show_detail_view

	def set_show_detail_view(self, show_detail_view):
		"""
		The method to set the value to show_detail_view

		Parameters:
			show_detail_view (bool) : A bool value
		"""
		self.__show_detail_view = show_detail_view
		self.__key_modified["show_detail_view"] = 1

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
