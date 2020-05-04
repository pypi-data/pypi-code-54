from ..header import Header
from ..header_map import HeaderMap
from ..param import Param
from ..param_map import ParameterMap
from ..util import APIResponse
from ..util import CommonAPIHandler
from ..util import Utility

class RecordOperations(object):
	def __init__(self):
		pass


	def get_record(self, param_instance, module_api_name, id):
		"""
		The method to get record

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string value
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.param=param_instance
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name=module_api_name
		from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, "application/json")

	def update_record(self, request, module_api_name, id):
		"""
		The method to update record

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			module_api_name (string) : A string value
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="PUT"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name=module_api_name
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def delete_record(self, param_instance, module_api_name, id):
		"""
		The method to delete record

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string value
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="DELETE"
		handler_instance.param=param_instance
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name=module_api_name
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def get_records(self, param_instance, header_instance, module_api_name):
		"""
		The method to get records

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			header_instance (HeaderMap) : An instance of HeaderMap
			module_api_name (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.param=param_instance
		handler_instance.header=header_instance
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name=module_api_name
		from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, "application/json")

	def create_records(self, request, module_api_name):
		"""
		The method to create records

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			module_api_name (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name=module_api_name
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def update_records(self, request, module_api_name):
		"""
		The method to update records

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			module_api_name (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="PUT"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name=module_api_name
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def delete_records(self, param_instance, module_api_name):
		"""
		The method to delete records

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="DELETE"
		handler_instance.param=param_instance
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name=module_api_name
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def upsert_records(self, request, module_api_name):
		"""
		The method to upsert records

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			module_api_name (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/upsert"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name=module_api_name
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def get_deleted_records(self, param_instance, header_instance, module_api_name):
		"""
		The method to get deleted records

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			header_instance (HeaderMap) : An instance of HeaderMap
			module_api_name (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/deleted"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.param=param_instance
		handler_instance.header=header_instance
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name=module_api_name
		from .deleted_records_handler import DeletedRecordsHandler
		return handler_instance.api_call(DeletedRecordsHandler.__module__, "application/json")

	def search_records(self, param_instance, module_api_name):
		"""
		The method to search records

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/search"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.param=param_instance
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name=module_api_name
		from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, "application/json")

	def convert_lead(self, request, id):
		"""
		The method to convert lead

		Parameters:
			request (ConvertBodyWrapper) : An instance of ConvertBodyWrapper
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/Leads/"
		api_path = api_path + id.__str__()
		api_path = api_path + "/actions/convert"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		from .convert_action_handler import ConvertActionHandler
		return handler_instance.api_call(ConvertActionHandler.__module__, "application/json")

	def get_photo(self, module_api_name, id):
		"""
		The method to get photo

		Parameters:
			module_api_name (string) : A string value
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + id.__str__()
		api_path = api_path + "/photo"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		from .download_handler import DownloadHandler
		return handler_instance.api_call(DownloadHandler.__module__, "application/x-download")

	def upload_photo(self, request, module_api_name, id):
		"""
		The method to upload photo

		Parameters:
			request (FileBodyWrapper) : An instance of FileBodyWrapper
			module_api_name (string) : A string value
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + id.__str__()
		api_path = api_path + "/photo"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.content_type="multipart/form-data"
		handler_instance.request=request
		from .file_handler import FileHandler
		return handler_instance.api_call(FileHandler.__module__, "application/json")

	def delete_photo(self, module_api_name, id):
		"""
		The method to delete photo

		Parameters:
			module_api_name (string) : A string value
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + id.__str__()
		api_path = api_path + "/photo"
		handler_instance.api_path=api_path
		handler_instance.http_method="DELETE"
		from .file_handler import FileHandler
		return handler_instance.api_call(FileHandler.__module__, "application/json")

class GetRecordParam(object):
	approved = Param("approved")

	converted = Param("converted")




class DeleteRecordParam(object):
	wf_trigger = Param("wf_trigger")




class GetRecordsParam(object):
	ids = Param("ids")

	converted = Param("converted")

	approved = Param("approved")

	page = Param("page")

	per_page = Param("per_page")

	fields = Param("fields")

	sort_by = Param("sort_by")

	sort_order = Param("sort_order")

	cvid = Param("cvid")

	territory_id = Param("territory_id")

	include_child = Param("include_child")




class GetRecordsHeader(object):
	If_modified_since = Header("If-Modified-Since")




class DeleteRecordsParam(object):
	ids = Param("ids")

	wf_trigger = Param("wf_trigger")




class GetDeletedRecordsParam(object):
	page = Param("page")

	per_page = Param("per_page")

	type = Param("type")




class GetDeletedRecordsHeader(object):
	If_modified_since = Header("If-Modified-Since")




class SearchRecordsParam(object):
	criteria = Param("criteria")

	email = Param("email")

	phone = Param("phone")

	word = Param("word")

	converted = Param("converted")

	approved = Param("approved")

	page = Param("page")

	per_page = Param("per_page")


