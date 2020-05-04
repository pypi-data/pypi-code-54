from blipy.Types import Data, Method, Response, URI
from requests import post

BLIP_COMMANDS = 'https://msging.net/commands'
BLIP_TAKE_MAX = 100

class Lime():
	def __init__(self, authorization):
		self.header = {
			'Authorization': f'Key {authorization}',
			'Content-Type': 'application/json'
		}

	def __sendCommand(self, method, uri, toId, resourceType = None, resource = None):
		data = Data.new(method, uri, toId, resourceType, resource)
		return Response(post(BLIP_COMMANDS, data=data, headers=self.header))

	def Get(self, uri, toId):
		return self.__sendCommand(Method.Get, uri, toId)

	def Set(self, uri, toId, resourceType, resource):
		return self.__sendCommand(Method.Set, uri, toId, resourceType, resource)

	def Delete(self, uri, toId):
		return self.__sendCommand(Method.Delete, uri, toId)

	def GetAll(self, uri, toId):
		updateUri = lambda uri, skip: URI.new(uri, { '$skip': str(skip), '$take': str(BLIP_TAKE_MAX) })
		response = self.__sendCommand(Method.Get, updateUri(uri, 0), toId)
		resource = response.Resource
		skip = resource.Total
		getMore = resource.Total == BLIP_TAKE_MAX
		while getMore:
			moreResource = self.__sendCommand(Method.Get, updateUri(uri,skip), toId).Resource
			resource.addItems(moreResource)
			skip += moreResource.Total
			getMore = moreResource.Total == BLIP_TAKE_MAX
		return response

	def SetAll(self, uri, toId, resourceType, resources):
		completed = []
		for resource in resources:
			response = self.__sendCommand(Method.Set, uri, toId, resourceType, resource)
			if response.Success:
				contentId = response.Resource.Id
				completed.append(contentId)
			else:
				self.DeleteAll(uri, toId, completed)
				raise Exception('Error occured while trying to set all resource')
		return completed

	def DeleteAll(self, uri, toId, ids):
		uriWithId = lambda uri, uriId: f'{uri}/{uriId}'
		responses = []
		for uriId in ids:
			responses.append(self.__sendCommand(Method.Delete, uriWithId(uri,uriId), toId))
		return responses
