from urllib.parse import quote, urlparse, unquote

BLIP_TAKE_MAX = 100

class URI:
	@staticmethod
	def new(baseuri, params = {}):
		parsed = urlparse(baseuri)
		path, query = unquote(parsed.path), parsed.query
		if len(query) > 0:
			originalParams = URI.parametrize(query)
			params.update(originalParams)
		uri = quote(path)
		if len(params.keys()) > 0:
			uri += f'?{URI.queryStringfy(params)}'
		return uri

	@staticmethod
	def queryStringfy(params):
		return '&'.join(map(lambda key: f'{key}={quote(params[key])}', params))
	
	@staticmethod
	def parametrize(queryString):
		params = {}
		for query in queryString.split('&'):
			key, value = query.split('=')
			params[key] = unquote(value)
		return params
