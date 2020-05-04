from ..util import APIResponse
from ..util import CommonAPIHandler

class LayoutsOperations(object):
	def __init__(self,module):
		self.__module = module


	def get_layouts(self):
		"""
		The method to get layouts

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/layouts"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.add_param("module", self.__module)
		from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, "application/json")

	def get_layout(self, id):
		"""
		The method to get layout

		Parameters:
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/layouts/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.add_param("module", self.__module)
		from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, "application/json")
