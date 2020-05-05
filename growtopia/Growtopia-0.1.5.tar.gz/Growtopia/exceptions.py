class InvalidGrowtopiaPath(Error):
	"""If the Growtopia Path is invalid or its a file, then raise this"""
class WrongCredential(Error):
	"""If the credential is wrong, raise this"""
class InvalidGrowtopiaVersion(Error):
	"""Raised when user put letter 'V' or anything else instead of
	floating numbers
	"""
class InvalidIntValue(Error):
	"""Raise this when user input something invalid that expected
	to be int
	"""
class InvalidFloatValue(Error):
	"""Raise this when user input something invalid that expected
	to be float
	"""
class InvalidPacketType(Error):
	"""Raise this when there is no packet type available in the list
	"""