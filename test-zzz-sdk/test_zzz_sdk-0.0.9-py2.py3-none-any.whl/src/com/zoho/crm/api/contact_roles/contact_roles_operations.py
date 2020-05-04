from ..param import Param
from ..param_map import ParameterMap
from ..util import APIResponse
from ..util import CommonAPIHandler

class ContactRolesOperations(object):
	def __init__(self):
		pass


	def get_contact_roles(self):
		"""
		The method to get contact roles

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, "application/json")

	def create_contact_roles(self, request):
		"""
		The method to create contact roles

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def update_contact_roles(self, request):
		"""
		The method to update contact roles

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles"
		handler_instance.api_path=api_path
		handler_instance.http_method="PUT"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def delete_contact_roles(self, param_instance):
		"""
		The method to delete contact roles

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles"
		handler_instance.api_path=api_path
		handler_instance.http_method="DELETE"
		handler_instance.param=param_instance
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def get_contact_role(self, id):
		"""
		The method to get contact role

		Parameters:
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, "application/json")

	def update_contact_role(self, request, id):
		"""
		The method to update contact role

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="PUT"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def delete_contact_role(self, id):
		"""
		The method to delete contact role

		Parameters:
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Contacts/roles/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="DELETE"
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

class DeleteContactRolesParam(object):
	ids = Param("ids")


