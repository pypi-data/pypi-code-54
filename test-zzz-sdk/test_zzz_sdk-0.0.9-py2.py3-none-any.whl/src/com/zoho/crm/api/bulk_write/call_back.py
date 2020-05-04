from ..util import Model


class CallBack(Model):
	def __init__(self):
		self.__url = None
		self.__post = None
		self.__key_modified = dict()

	def get_url(self):
		"""
		The method to get the url

		Returns:
			string: A string value
		"""
		return self.__url

	def set_url(self, url):
		"""
		The method to set the value to url

		Parameters:
			url (string) : A string value
		"""
		self.__url = url
		self.__key_modified["url"] = 1

	def get_post(self):
		"""
		The method to get the post

		Returns:
			string: A string value
		"""
		return self.__post

	def set_post(self, post):
		"""
		The method to set the value to post

		Parameters:
			post (string) : A string value
		"""
		self.__post = post
		self.__key_modified["post"] = 1

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
