from ..param import Param
from ..param_map import ParameterMap
from ..util import APIResponse
from ..util import CommonAPIHandler

class TagsOperations(object):
	def __init__(self):
		pass


	def get_tags(self, param_instance):
		"""
		The method to get tags

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.param=param_instance
		from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, "application/json")

	def create_tags(self, request, param_instance):
		"""
		The method to create tags

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		handler_instance.param=param_instance
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def update_tags(self, request, param_instance):
		"""
		The method to update tags

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags"
		handler_instance.api_path=api_path
		handler_instance.http_method="PUT"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		handler_instance.param=param_instance
		from .action_wrapper import ActionWrapper
		return handler_instance.api_call(ActionWrapper.__module__, "application/json")

	def update_tag(self, request, param_instance, id):
		"""
		The method to update tag

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			param_instance (ParameterMap) : An instance of ParameterMap
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="PUT"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		handler_instance.param=param_instance
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def delete_tag(self, id):
		"""
		The method to delete tag

		Parameters:
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags/"
		api_path = api_path + id.__str__()
		handler_instance.api_path=api_path
		handler_instance.http_method="DELETE"
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def merge_tags(self, request, id):
		"""
		The method to merge tags

		Parameters:
			request (MergeWrapper) : An instance of MergeWrapper
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags/"
		api_path = api_path + id.__str__()
		api_path = api_path + "/actions/merge"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.content_type="application/json"
		handler_instance.request=request
		from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, "application/json")

	def add_tags_to_record(self, param_instance, module_api_name, record_id):
		"""
		The method to add tags to record

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string value
			record_id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + record_id.__str__()
		api_path = api_path + "/actions/add_tags"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.param=param_instance
		from .record_action_handler import RecordActionHandler
		return handler_instance.api_call(RecordActionHandler.__module__, "application/json")

	def remove_tags_from_record(self, param_instance, module_api_name, record_id):
		"""
		The method to remove tags from record

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string value
			record_id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/"
		api_path = api_path + module_api_name.__str__()
		api_path = api_path + "/"
		api_path = api_path + record_id.__str__()
		api_path = api_path + "/actions/remove_tags"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.param=param_instance
		from .record_action_handler import RecordActionHandler
		return handler_instance.api_call(RecordActionHandler.__module__, "application/json")

	def add_tags_to_multiple_records(self, param_instance, module_api_name):
		"""
		The method to add tags to multiple records

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
		api_path = api_path + "/actions/add_tags"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.param=param_instance
		from .record_action_handler import RecordActionHandler
		return handler_instance.api_call(RecordActionHandler.__module__, "application/json")

	def remove_tags_from_multiple_records(self, param_instance, module_api_name):
		"""
		The method to remove tags from multiple records

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
		api_path = api_path + "/actions/remove_tags"
		handler_instance.api_path=api_path
		handler_instance.http_method="POST"
		handler_instance.param=param_instance
		from .record_action_handler import RecordActionHandler
		return handler_instance.api_call(RecordActionHandler.__module__, "application/json")

	def get_record_count_for_tag(self, param_instance, id):
		"""
		The method to get record count for tag

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			id (string) : A string value

		Returns:
			APIResponse: An instance of APIResponse
		"""
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + "/crm/v2/settings/tags/"
		api_path = api_path + id.__str__()
		api_path = api_path + "/actions/records_count"
		handler_instance.api_path=api_path
		handler_instance.http_method="GET"
		handler_instance.param=param_instance
		from .count_handler import CountHandler
		return handler_instance.api_call(CountHandler.__module__, "application/json")

class GetTagsParam(object):
	module = Param("module")

	my_tags = Param("my_tags")




class CreateTagsParam(object):
	module = Param("module")




class UpdateTagsParam(object):
	module = Param("module")




class UpdateTagParam(object):
	module = Param("module")




class AddTagsToRecordParam(object):
	tag_names = Param("tag_names")




class RemoveTagsFromRecordParam(object):
	tag_names = Param("tag_names")




class AddTagsToMultipleRecordsParam(object):
	tag_names = Param("tag_names")

	ids = Param("ids")

	over_write = Param("over_write")




class RemoveTagsFromMultipleRecordsParam(object):
	tag_names = Param("tag_names")

	ids = Param("ids")




class GetRecordCountForTagParam(object):
	module = Param("module")


