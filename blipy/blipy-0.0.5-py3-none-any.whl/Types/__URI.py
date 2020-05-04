from urllib.parse import quote

class URI:
	@staticmethod
	def new(baseuri, params = None):
		checkForParams = baseuri.split('?')
		base = checkForParams[0]
		if params:
			keyEqualsValue = lambda key: f'{key}={quote(params[key])}'
			base += '?' + '&'.join(map(keyEqualsValue, params))
		if len(checkForParams) == 2:
			base += ('' if params else '?') + '&' + checkForParams[1]
		return base
