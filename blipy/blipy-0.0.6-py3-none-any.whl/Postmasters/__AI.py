from blipy.Http import Postmaster

INTENTS = '/intentions'

class AIPostmaster(Postmaster):
	def __init__(self, authorization):
		super().__init__(authorization, 'ai')
	
	def getIntent(self, intentId):
		return super().Get(f'{INTENTS}/{intentId}?deep=true')

	def getIntents(self):
		return super().GetAll(f'{INTENTS}')

	def getEntity(self, entityId):
		return super().Get(f'/entities/{entityId}')
