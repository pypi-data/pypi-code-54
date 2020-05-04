from blipy.Http import Postmaster
from blipy.Types import Date, URI

intervalType = {
	'NoInterval': 'NI',
	'Daily': 'D',
	'Monthly': 'M'
}

TRACKINGS = '/event-track'

class AnalyticsPostmaster(Postmaster):
	def __init__(self, authorization):
		super().__init__(authorization, 'analytics')

	def getActiveMessages(self, startDate, endDate, interval = 'NoInterval'):
		baseURI = f'/metrics/active-messages/{intervalType[interval]}'
		uri = URI.new(baseURI, Date.interval(startDate, endDate))
		return super().Get(uri)

	def getCategories(self):
		return super().Get(TRACKINGS)
	
	def getCounters(self, categoryId, startDate, endDate):
		baseURI = f'{TRACKINGS}/{categoryId}'
		params = Date.interval(startDate, endDate)
		uri = URI.new(baseURI, params)
		return super().GetAll(uri)

	def getTrackings(self, categoryId, action, startDate, endDate):
		baseURI = f'{TRACKINGS}/{categoryId}/{action}'
		params = Date.interval(startDate, endDate)
		uri = URI.new(baseURI, params)
		return super().GetAll(uri)
