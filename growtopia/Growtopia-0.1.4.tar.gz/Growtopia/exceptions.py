class InvalidGrowtopiaPath(self, Error):
	"""If the Growtopia Path is invalid or its a file, then raise this"""
class WrongCredential(self, Error):
	"""If the credential is wrong, raise this"""
class InvalidGrowtopiaVersion(self, Error):
	"""Raised when user put letter 'V' or anything else instead of
	floating numbers
	"""
class InvalidIntValue(self, Error):
	"""Raise this when user input something invalid that expected
	to be int
	"""
class InvalidFloatValue(self, Error):
	"""Raise this when user input something invalid that expected
	to be float
	"""
class InvalidPacketType(self, Error):
	"""Raise this when there is no packet type available in the list
	"""