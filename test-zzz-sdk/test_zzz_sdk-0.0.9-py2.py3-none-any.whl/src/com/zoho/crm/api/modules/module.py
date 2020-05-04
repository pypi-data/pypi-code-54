from ..custom_view import CustomView
from ..profile import Profile
from ..users import User
from ..util import Model


class Module(Model):
	def __init__(self):
		self.__id = None
		self.__api_name = None
		self.__module_name = None
		self.__convertable = None
		self.__editable = None
		self.__deletable = None
		self.__web_link = None
		self.__singular_label = None
		self.__modified_time = None
		self.__viewable = None
		self.__api_supported = None
		self.__createable = None
		self.__plural_label = None
		self.__generated_type = None
		self.__modified_by = None
		self.__global_search_supported = None
		self.__presence_sub_menu = None
		self.__triggers_supported = None
		self.__feeds_required = None
		self.__filter_supported = None
		self.__scoring_supported = None
		self.__webform_supported = None
		self.__kanban_view = None
		self.__kanban_view_supported = None
		self.__show_as_tab = None
		self.__filter_status = None
		self.__quick_create = None
		self.__emailtemplate_support = None
		self.__inventory_template_supported = None
		self.__description = None
		self.__display_field = None
		self.__visibility = None
		self.__business_card_field_limit = None
		self.__per_page = None
		self.__sequence_number = None
		self.__profiles = None
		self.__custom_view = None
		self.__related_list_properties = None
		self.__properties = None
		self.__search_layout_fields = None
		self.__parent_module = None
		self.__territory = None
		self.__arguments = None
		self.__key_modified = dict()

	def get_id(self):
		"""
		The method to get the id

		Returns:
			string: A string value
		"""
		return self.__id

	def set_id(self, id):
		"""
		The method to set the value to id

		Parameters:
			id (string) : A string value
		"""
		self.__id = id
		self.__key_modified["id"] = 1

	def get_api_name(self):
		"""
		The method to get the api_name

		Returns:
			string: A string value
		"""
		return self.__api_name

	def set_api_name(self, api_name):
		"""
		The method to set the value to api_name

		Parameters:
			api_name (string) : A string value
		"""
		self.__api_name = api_name
		self.__key_modified["api_name"] = 1

	def get_module_name(self):
		"""
		The method to get the module_name

		Returns:
			string: A string value
		"""
		return self.__module_name

	def set_module_name(self, module_name):
		"""
		The method to set the value to module_name

		Parameters:
			module_name (string) : A string value
		"""
		self.__module_name = module_name
		self.__key_modified["module_name"] = 1

	def get_convertable(self):
		"""
		The method to get the convertable

		Returns:
			bool: A bool value
		"""
		return self.__convertable

	def set_convertable(self, convertable):
		"""
		The method to set the value to convertable

		Parameters:
			convertable (bool) : A bool value
		"""
		self.__convertable = convertable
		self.__key_modified["convertable"] = 1

	def get_editable(self):
		"""
		The method to get the editable

		Returns:
			bool: A bool value
		"""
		return self.__editable

	def set_editable(self, editable):
		"""
		The method to set the value to editable

		Parameters:
			editable (bool) : A bool value
		"""
		self.__editable = editable
		self.__key_modified["editable"] = 1

	def get_deletable(self):
		"""
		The method to get the deletable

		Returns:
			bool: A bool value
		"""
		return self.__deletable

	def set_deletable(self, deletable):
		"""
		The method to set the value to deletable

		Parameters:
			deletable (bool) : A bool value
		"""
		self.__deletable = deletable
		self.__key_modified["deletable"] = 1

	def get_web_link(self):
		"""
		The method to get the web_link

		Returns:
			string: A string value
		"""
		return self.__web_link

	def set_web_link(self, web_link):
		"""
		The method to set the value to web_link

		Parameters:
			web_link (string) : A string value
		"""
		self.__web_link = web_link
		self.__key_modified["web_link"] = 1

	def get_singular_label(self):
		"""
		The method to get the singular_label

		Returns:
			string: A string value
		"""
		return self.__singular_label

	def set_singular_label(self, singular_label):
		"""
		The method to set the value to singular_label

		Parameters:
			singular_label (string) : A string value
		"""
		self.__singular_label = singular_label
		self.__key_modified["singular_label"] = 1

	def get_modified_time(self):
		"""
		The method to get the modified_time

		Returns:
			DateTime: An instance of DateTime
		"""
		return self.__modified_time

	def set_modified_time(self, modified_time):
		"""
		The method to set the value to modified_time

		Parameters:
			modified_time (DateTime) : An instance of DateTime
		"""
		self.__modified_time = modified_time
		self.__key_modified["modified_time"] = 1

	def get_viewable(self):
		"""
		The method to get the viewable

		Returns:
			bool: A bool value
		"""
		return self.__viewable

	def set_viewable(self, viewable):
		"""
		The method to set the value to viewable

		Parameters:
			viewable (bool) : A bool value
		"""
		self.__viewable = viewable
		self.__key_modified["viewable"] = 1

	def get_api_supported(self):
		"""
		The method to get the api_supported

		Returns:
			bool: A bool value
		"""
		return self.__api_supported

	def set_api_supported(self, api_supported):
		"""
		The method to set the value to api_supported

		Parameters:
			api_supported (bool) : A bool value
		"""
		self.__api_supported = api_supported
		self.__key_modified["api_supported"] = 1

	def get_createable(self):
		"""
		The method to get the createable

		Returns:
			bool: A bool value
		"""
		return self.__createable

	def set_createable(self, createable):
		"""
		The method to set the value to createable

		Parameters:
			createable (bool) : A bool value
		"""
		self.__createable = createable
		self.__key_modified["createable"] = 1

	def get_plural_label(self):
		"""
		The method to get the plural_label

		Returns:
			string: A string value
		"""
		return self.__plural_label

	def set_plural_label(self, plural_label):
		"""
		The method to set the value to plural_label

		Parameters:
			plural_label (string) : A string value
		"""
		self.__plural_label = plural_label
		self.__key_modified["plural_label"] = 1

	def get_generated_type(self):
		"""
		The method to get the generated_type

		Returns:
			string: A string value
		"""
		return self.__generated_type

	def set_generated_type(self, generated_type):
		"""
		The method to set the value to generated_type

		Parameters:
			generated_type (string) : A string value
		"""
		self.__generated_type = generated_type
		self.__key_modified["generated_type"] = 1

	def get_modified_by(self):
		"""
		The method to get the modified_by

		Returns:
			User: An instance of User
		"""
		return self.__modified_by

	def set_modified_by(self, modified_by):
		"""
		The method to set the value to modified_by

		Parameters:
			modified_by (User) : An instance of User
		"""
		self.__modified_by = modified_by
		self.__key_modified["modified_by"] = 1

	def get_global_search_supported(self):
		"""
		The method to get the global_search_supported

		Returns:
			bool: A bool value
		"""
		return self.__global_search_supported

	def set_global_search_supported(self, global_search_supported):
		"""
		The method to set the value to global_search_supported

		Parameters:
			global_search_supported (bool) : A bool value
		"""
		self.__global_search_supported = global_search_supported
		self.__key_modified["global_search_supported"] = 1

	def get_presence_sub_menu(self):
		"""
		The method to get the presence_sub_menu

		Returns:
			bool: A bool value
		"""
		return self.__presence_sub_menu

	def set_presence_sub_menu(self, presence_sub_menu):
		"""
		The method to set the value to presence_sub_menu

		Parameters:
			presence_sub_menu (bool) : A bool value
		"""
		self.__presence_sub_menu = presence_sub_menu
		self.__key_modified["presence_sub_menu"] = 1

	def get_triggers_supported(self):
		"""
		The method to get the triggers_supported

		Returns:
			bool: A bool value
		"""
		return self.__triggers_supported

	def set_triggers_supported(self, triggers_supported):
		"""
		The method to set the value to triggers_supported

		Parameters:
			triggers_supported (bool) : A bool value
		"""
		self.__triggers_supported = triggers_supported
		self.__key_modified["triggers_supported"] = 1

	def get_feeds_required(self):
		"""
		The method to get the feeds_required

		Returns:
			bool: A bool value
		"""
		return self.__feeds_required

	def set_feeds_required(self, feeds_required):
		"""
		The method to set the value to feeds_required

		Parameters:
			feeds_required (bool) : A bool value
		"""
		self.__feeds_required = feeds_required
		self.__key_modified["feeds_required"] = 1

	def get_filter_supported(self):
		"""
		The method to get the filter_supported

		Returns:
			bool: A bool value
		"""
		return self.__filter_supported

	def set_filter_supported(self, filter_supported):
		"""
		The method to set the value to filter_supported

		Parameters:
			filter_supported (bool) : A bool value
		"""
		self.__filter_supported = filter_supported
		self.__key_modified["filter_supported"] = 1

	def get_scoring_supported(self):
		"""
		The method to get the scoring_supported

		Returns:
			bool: A bool value
		"""
		return self.__scoring_supported

	def set_scoring_supported(self, scoring_supported):
		"""
		The method to set the value to scoring_supported

		Parameters:
			scoring_supported (bool) : A bool value
		"""
		self.__scoring_supported = scoring_supported
		self.__key_modified["scoring_supported"] = 1

	def get_webform_supported(self):
		"""
		The method to get the webform_supported

		Returns:
			bool: A bool value
		"""
		return self.__webform_supported

	def set_webform_supported(self, webform_supported):
		"""
		The method to set the value to webform_supported

		Parameters:
			webform_supported (bool) : A bool value
		"""
		self.__webform_supported = webform_supported
		self.__key_modified["webform_supported"] = 1

	def get_kanban_view(self):
		"""
		The method to get the kanban_view

		Returns:
			bool: A bool value
		"""
		return self.__kanban_view

	def set_kanban_view(self, kanban_view):
		"""
		The method to set the value to kanban_view

		Parameters:
			kanban_view (bool) : A bool value
		"""
		self.__kanban_view = kanban_view
		self.__key_modified["kanban_view"] = 1

	def get_kanban_view_supported(self):
		"""
		The method to get the kanban_view_supported

		Returns:
			bool: A bool value
		"""
		return self.__kanban_view_supported

	def set_kanban_view_supported(self, kanban_view_supported):
		"""
		The method to set the value to kanban_view_supported

		Parameters:
			kanban_view_supported (bool) : A bool value
		"""
		self.__kanban_view_supported = kanban_view_supported
		self.__key_modified["kanban_view_supported"] = 1

	def get_show_as_tab(self):
		"""
		The method to get the show_as_tab

		Returns:
			bool: A bool value
		"""
		return self.__show_as_tab

	def set_show_as_tab(self, show_as_tab):
		"""
		The method to set the value to show_as_tab

		Parameters:
			show_as_tab (bool) : A bool value
		"""
		self.__show_as_tab = show_as_tab
		self.__key_modified["show_as_tab"] = 1

	def get_filter_status(self):
		"""
		The method to get the filter_status

		Returns:
			bool: A bool value
		"""
		return self.__filter_status

	def set_filter_status(self, filter_status):
		"""
		The method to set the value to filter_status

		Parameters:
			filter_status (bool) : A bool value
		"""
		self.__filter_status = filter_status
		self.__key_modified["filter_status"] = 1

	def get_quick_create(self):
		"""
		The method to get the quick_create

		Returns:
			bool: A bool value
		"""
		return self.__quick_create

	def set_quick_create(self, quick_create):
		"""
		The method to set the value to quick_create

		Parameters:
			quick_create (bool) : A bool value
		"""
		self.__quick_create = quick_create
		self.__key_modified["quick_create"] = 1

	def get_emailtemplate_support(self):
		"""
		The method to get the emailtemplate_support

		Returns:
			bool: A bool value
		"""
		return self.__emailtemplate_support

	def set_emailtemplate_support(self, emailtemplate_support):
		"""
		The method to set the value to emailtemplate_support

		Parameters:
			emailtemplate_support (bool) : A bool value
		"""
		self.__emailtemplate_support = emailtemplate_support
		self.__key_modified["emailTemplate_support"] = 1

	def get_inventory_template_supported(self):
		"""
		The method to get the inventory_template_supported

		Returns:
			bool: A bool value
		"""
		return self.__inventory_template_supported

	def set_inventory_template_supported(self, inventory_template_supported):
		"""
		The method to set the value to inventory_template_supported

		Parameters:
			inventory_template_supported (bool) : A bool value
		"""
		self.__inventory_template_supported = inventory_template_supported
		self.__key_modified["inventory_template_supported"] = 1

	def get_description(self):
		"""
		The method to get the description

		Returns:
			string: A string value
		"""
		return self.__description

	def set_description(self, description):
		"""
		The method to set the value to description

		Parameters:
			description (string) : A string value
		"""
		self.__description = description
		self.__key_modified["description"] = 1

	def get_display_field(self):
		"""
		The method to get the display_field

		Returns:
			string: A string value
		"""
		return self.__display_field

	def set_display_field(self, display_field):
		"""
		The method to set the value to display_field

		Parameters:
			display_field (string) : A string value
		"""
		self.__display_field = display_field
		self.__key_modified["display_field"] = 1

	def get_visibility(self):
		"""
		The method to get the visibility

		Returns:
			int: A int value
		"""
		return self.__visibility

	def set_visibility(self, visibility):
		"""
		The method to set the value to visibility

		Parameters:
			visibility (int) : A int value
		"""
		self.__visibility = visibility
		self.__key_modified["visibility"] = 1

	def get_business_card_field_limit(self):
		"""
		The method to get the business_card_field_limit

		Returns:
			int: A int value
		"""
		return self.__business_card_field_limit

	def set_business_card_field_limit(self, business_card_field_limit):
		"""
		The method to set the value to business_card_field_limit

		Parameters:
			business_card_field_limit (int) : A int value
		"""
		self.__business_card_field_limit = business_card_field_limit
		self.__key_modified["business_card_field_limit"] = 1

	def get_per_page(self):
		"""
		The method to get the per_page

		Returns:
			int: A int value
		"""
		return self.__per_page

	def set_per_page(self, per_page):
		"""
		The method to set the value to per_page

		Parameters:
			per_page (int) : A int value
		"""
		self.__per_page = per_page
		self.__key_modified["per_page"] = 1

	def get_sequence_number(self):
		"""
		The method to get the sequence_number

		Returns:
			int: A int value
		"""
		return self.__sequence_number

	def set_sequence_number(self, sequence_number):
		"""
		The method to set the value to sequence_number

		Parameters:
			sequence_number (int) : A int value
		"""
		self.__sequence_number = sequence_number
		self.__key_modified["sequence_number"] = 1

	def get_profiles(self):
		"""
		The method to get the profiles

		Returns:
			list: An instance of list
		"""
		return self.__profiles

	def set_profiles(self, profiles):
		"""
		The method to set the value to profiles

		Parameters:
			profiles (list) : An instance of list
		"""
		self.__profiles = profiles
		self.__key_modified["profiles"] = 1

	def get_custom_view(self):
		"""
		The method to get the custom_view

		Returns:
			CustomView: An instance of CustomView
		"""
		return self.__custom_view

	def set_custom_view(self, custom_view):
		"""
		The method to set the value to custom_view

		Parameters:
			custom_view (CustomView) : An instance of CustomView
		"""
		self.__custom_view = custom_view
		self.__key_modified["custom_view"] = 1

	def get_related_list_properties(self):
		"""
		The method to get the related_list_properties

		Returns:
			RelatedListProperties: An instance of RelatedListProperties
		"""
		return self.__related_list_properties

	def set_related_list_properties(self, related_list_properties):
		"""
		The method to set the value to related_list_properties

		Parameters:
			related_list_properties (RelatedListProperties) : An instance of RelatedListProperties
		"""
		self.__related_list_properties = related_list_properties
		self.__key_modified["related_list_properties"] = 1

	def get_properties(self):
		"""
		The method to get the properties

		Returns:
			list: An instance of list
		"""
		return self.__properties

	def set_properties(self, properties):
		"""
		The method to set the value to properties

		Parameters:
			properties (list) : An instance of list
		"""
		self.__properties = properties
		self.__key_modified["$properties"] = 1

	def get_search_layout_fields(self):
		"""
		The method to get the search_layout_fields

		Returns:
			list: An instance of list
		"""
		return self.__search_layout_fields

	def set_search_layout_fields(self, search_layout_fields):
		"""
		The method to set the value to search_layout_fields

		Parameters:
			search_layout_fields (list) : An instance of list
		"""
		self.__search_layout_fields = search_layout_fields
		self.__key_modified["search_layout_fields"] = 1

	def get_parent_module(self):
		"""
		The method to get the parent_module

		Returns:
			ParentModule: An instance of ParentModule
		"""
		return self.__parent_module

	def set_parent_module(self, parent_module):
		"""
		The method to set the value to parent_module

		Parameters:
			parent_module (ParentModule) : An instance of ParentModule
		"""
		self.__parent_module = parent_module
		self.__key_modified["parent_module"] = 1

	def get_territory(self):
		"""
		The method to get the territory

		Returns:
			Territory: An instance of Territory
		"""
		return self.__territory

	def set_territory(self, territory):
		"""
		The method to set the value to territory

		Parameters:
			territory (Territory) : An instance of Territory
		"""
		self.__territory = territory
		self.__key_modified["territory"] = 1

	def get_arguments(self):
		"""
		The method to get the arguments

		Returns:
			list: An instance of list
		"""
		return self.__arguments

	def set_arguments(self, arguments):
		"""
		The method to set the value to arguments

		Parameters:
			arguments (list) : An instance of list
		"""
		self.__arguments = arguments
		self.__key_modified["arguments"] = 1

	def is_key_modified(self, key):
		"""
		The method to check if the user has modified the given key

		Parameters:
			key (string) : A string value

		Returns:
			int: A int value
		"""
		return self.__key_modified.get(key)

	def set_key_modified(self, modification, key):
		"""
		The method to mark the given key as modified

		Parameters:
			modification (int) : A int value
			key (string) : A string value
		"""
		self.__key_modified[key] = modification
