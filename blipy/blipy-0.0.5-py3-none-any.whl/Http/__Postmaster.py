from blipy.Http import Lime

class Postmaster(Lime):
	def __init__(self, authorization, name):
		super().__init__(authorization)
		self.identity = f'postmaster@{name}'

	def Get(self, uri):
		return super().Get(uri, self.identity)
	
	def Set(self, uri, resourceType, resource):
		return super().Set(uri, self.identity, resourceType, resource)

	def Delete(self, uri):
		return super().Delete(uri, self.identity)
	
	def GetAll(self, uri):
		return super().GetAll(uri, self.identity)
	
	def SetAll(self, uri, resourceType, resources):
		return super().SetAll(uri, self.identity, resourceType, resources)
	
	def DeleteAll(self, uri, ids):
		return super().DeleteAll(uri, self.identity, ids)
