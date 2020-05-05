from blipy.Types import Serializable

keyValueOrDefault = lambda source, key, default: source[key] if key in source else default

class Resource(Serializable):
	def __init__(self, rawResource):
		super().__init__(rawResource)
		self.Total = keyValueOrDefault(rawResource, 'total', 0)
		self.Items = keyValueOrDefault(rawResource, 'items', [])
		self.Id = keyValueOrDefault(rawResource, 'id', None)

	def addItems(self, resource):
		self.Total += resource.Total
		self.Items += resource.Items

class Response(Serializable):
	def __init__(self, rawResponse):
		response = rawResponse.json()
		super().__init__(response)
		self.Status = keyValueOrDefault(response, 'status', None)
		self.Resource = Resource(self.Resource)
		self.Success = self.Status == 'success'
