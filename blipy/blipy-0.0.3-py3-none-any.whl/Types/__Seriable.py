class Seriable:
	def __init__(self, hashable):
		selfDict = {}
		for key in hashable:
			selfDict[key.capitalize()] = hashable[key]
		self.__dict__.update(selfDict)
