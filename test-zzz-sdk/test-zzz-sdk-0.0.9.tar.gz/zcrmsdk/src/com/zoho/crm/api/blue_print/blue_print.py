from ..util import Model


class BluePrint(Model):
	def __init__(self):
		self.__process_info = None
		self.__transitions = None
		self.__key_modified = dict()

	def get_process_info(self):
		"""
		The method to get the process_info

		Returns:
			ProcessInfo: An instance of ProcessInfo
		"""
		return self.__process_info

	def set_process_info(self, process_info):
		"""
		The method to set the value to process_info

		Parameters:
			process_info (ProcessInfo) : An instance of ProcessInfo
		"""
		self.__process_info = process_info
		self.__key_modified["process_info"] = 1

	def get_transitions(self):
		"""
		The method to get the transitions

		Returns:
			list: An instance of list
		"""
		return self.__transitions

	def set_transitions(self, transitions):
		"""
		The method to set the value to transitions

		Parameters:
			transitions (list) : An instance of list
		"""
		self.__transitions = transitions
		self.__key_modified["transitions"] = 1

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
