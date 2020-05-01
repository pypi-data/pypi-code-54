from uuid import uuid1
from json import dumps

class Data:
	@staticmethod
	def new(method, uri, toId, resourceType = 'None', resource = None):
		data = {
			'id': str(uuid1()),
			'uri': uri,
			'to': f'{toId}.msging.net' if '@' in toId else f'{toId}@msging.net',
			'method': method
		}
		if resourceType and resource:
			data['type'] = resourceType
			data['resource'] = resource
		return dumps(data)
