from ..util import Model


class Field(Model):
	def __init__(self):
		self.__id = None
		self.__api_name = None
		self.__system_mandatory = None
		self.__webhook = None
		self.__json_type = None
		self.__crypt = None
		self.__field_label = None
		self.__tooltip = None
		self.__field_read_only = None
		self.__display_label = None
		self.__default_value = None
		self.__decimal_place = None
		self.__quick_sequence_number = None
		self.__section_id = None
		self.__read_only = None
		self.__blueprint_supported = None
		self.__length = None
		self.__custom_field = None
		self.__mass_update = None
		self.__visible = None
		self.__association_details = None
		self.__validation_rule = None
		self.__multi_module_lookup = None
		self.__formula = None
		self.__unique = None
		self.__multiselectlookup = None
		self.__auto_number = None
		self.__businesscard_supported = None
		self.__history_tracking = None
		self.__currency = None
		self.__lookup = None
		self.__subform = None
		self.__convert_mapping = None
		self.__pick_list_values = None
		self.__data_type = None
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

	def get_system_mandatory(self):
		"""
		The method to get the system_mandatory

		Returns:
			bool: A bool value
		"""
		return self.__system_mandatory

	def set_system_mandatory(self, system_mandatory):
		"""
		The method to set the value to system_mandatory

		Parameters:
			system_mandatory (bool) : A bool value
		"""
		self.__system_mandatory = system_mandatory
		self.__key_modified["system_mandatory"] = 1

	def get_webhook(self):
		"""
		The method to get the webhook

		Returns:
			bool: A bool value
		"""
		return self.__webhook

	def set_webhook(self, webhook):
		"""
		The method to set the value to webhook

		Parameters:
			webhook (bool) : A bool value
		"""
		self.__webhook = webhook
		self.__key_modified["webhook"] = 1

	def get_json_type(self):
		"""
		The method to get the json_type

		Returns:
			string: A string value
		"""
		return self.__json_type

	def set_json_type(self, json_type):
		"""
		The method to set the value to json_type

		Parameters:
			json_type (string) : A string value
		"""
		self.__json_type = json_type
		self.__key_modified["json_type"] = 1

	def get_crypt(self):
		"""
		The method to get the crypt

		Returns:
			Crypt: An instance of Crypt
		"""
		return self.__crypt

	def set_crypt(self, crypt):
		"""
		The method to set the value to crypt

		Parameters:
			crypt (Crypt) : An instance of Crypt
		"""
		self.__crypt = crypt
		self.__key_modified["crypt"] = 1

	def get_field_label(self):
		"""
		The method to get the field_label

		Returns:
			string: A string value
		"""
		return self.__field_label

	def set_field_label(self, field_label):
		"""
		The method to set the value to field_label

		Parameters:
			field_label (string) : A string value
		"""
		self.__field_label = field_label
		self.__key_modified["field_label"] = 1

	def get_tooltip(self):
		"""
		The method to get the tooltip

		Returns:
			ToolTip: An instance of ToolTip
		"""
		return self.__tooltip

	def set_tooltip(self, tooltip):
		"""
		The method to set the value to tooltip

		Parameters:
			tooltip (ToolTip) : An instance of ToolTip
		"""
		self.__tooltip = tooltip
		self.__key_modified["tooltip"] = 1

	def get_field_read_only(self):
		"""
		The method to get the field_read_only

		Returns:
			bool: A bool value
		"""
		return self.__field_read_only

	def set_field_read_only(self, field_read_only):
		"""
		The method to set the value to field_read_only

		Parameters:
			field_read_only (bool) : A bool value
		"""
		self.__field_read_only = field_read_only
		self.__key_modified["field_read_only"] = 1

	def get_display_label(self):
		"""
		The method to get the display_label

		Returns:
			string: A string value
		"""
		return self.__display_label

	def set_display_label(self, display_label):
		"""
		The method to set the value to display_label

		Parameters:
			display_label (string) : A string value
		"""
		self.__display_label = display_label
		self.__key_modified["display_label"] = 1

	def get_default_value(self):
		"""
		The method to get the default_value

		Returns:
			string: A string value
		"""
		return self.__default_value

	def set_default_value(self, default_value):
		"""
		The method to set the value to default_value

		Parameters:
			default_value (string) : A string value
		"""
		self.__default_value = default_value
		self.__key_modified["default_value"] = 1

	def get_decimal_place(self):
		"""
		The method to get the decimal_place

		Returns:
			int: A int value
		"""
		return self.__decimal_place

	def set_decimal_place(self, decimal_place):
		"""
		The method to set the value to decimal_place

		Parameters:
			decimal_place (int) : A int value
		"""
		self.__decimal_place = decimal_place
		self.__key_modified["decimal_place"] = 1

	def get_quick_sequence_number(self):
		"""
		The method to get the quick_sequence_number

		Returns:
			int: A int value
		"""
		return self.__quick_sequence_number

	def set_quick_sequence_number(self, quick_sequence_number):
		"""
		The method to set the value to quick_sequence_number

		Parameters:
			quick_sequence_number (int) : A int value
		"""
		self.__quick_sequence_number = quick_sequence_number
		self.__key_modified["quick_sequence_number"] = 1

	def get_section_id(self):
		"""
		The method to get the section_id

		Returns:
			int: A int value
		"""
		return self.__section_id

	def set_section_id(self, section_id):
		"""
		The method to set the value to section_id

		Parameters:
			section_id (int) : A int value
		"""
		self.__section_id = section_id
		self.__key_modified["section_id"] = 1

	def get_read_only(self):
		"""
		The method to get the read_only

		Returns:
			bool: A bool value
		"""
		return self.__read_only

	def set_read_only(self, read_only):
		"""
		The method to set the value to read_only

		Parameters:
			read_only (bool) : A bool value
		"""
		self.__read_only = read_only
		self.__key_modified["read_only"] = 1

	def get_blueprint_supported(self):
		"""
		The method to get the blueprint_supported

		Returns:
			bool: A bool value
		"""
		return self.__blueprint_supported

	def set_blueprint_supported(self, blueprint_supported):
		"""
		The method to set the value to blueprint_supported

		Parameters:
			blueprint_supported (bool) : A bool value
		"""
		self.__blueprint_supported = blueprint_supported
		self.__key_modified["blueprint_supported"] = 1

	def get_length(self):
		"""
		The method to get the length

		Returns:
			int: A int value
		"""
		return self.__length

	def set_length(self, length):
		"""
		The method to set the value to length

		Parameters:
			length (int) : A int value
		"""
		self.__length = length
		self.__key_modified["length"] = 1

	def get_custom_field(self):
		"""
		The method to get the custom_field

		Returns:
			bool: A bool value
		"""
		return self.__custom_field

	def set_custom_field(self, custom_field):
		"""
		The method to set the value to custom_field

		Parameters:
			custom_field (bool) : A bool value
		"""
		self.__custom_field = custom_field
		self.__key_modified["custom_field"] = 1

	def get_mass_update(self):
		"""
		The method to get the mass_update

		Returns:
			bool: A bool value
		"""
		return self.__mass_update

	def set_mass_update(self, mass_update):
		"""
		The method to set the value to mass_update

		Parameters:
			mass_update (bool) : A bool value
		"""
		self.__mass_update = mass_update
		self.__key_modified["mass_update"] = 1

	def get_visible(self):
		"""
		The method to get the visible

		Returns:
			bool: A bool value
		"""
		return self.__visible

	def set_visible(self, visible):
		"""
		The method to set the value to visible

		Parameters:
			visible (bool) : A bool value
		"""
		self.__visible = visible
		self.__key_modified["visible"] = 1

	def get_association_details(self):
		"""
		The method to get the association_details

		Returns:
			dict: An instance of dict
		"""
		return self.__association_details

	def set_association_details(self, association_details):
		"""
		The method to set the value to association_details

		Parameters:
			association_details (dict) : An instance of dict
		"""
		self.__association_details = association_details
		self.__key_modified["association_details"] = 1

	def get_validation_rule(self):
		"""
		The method to get the validation_rule

		Returns:
			dict: An instance of dict
		"""
		return self.__validation_rule

	def set_validation_rule(self, validation_rule):
		"""
		The method to set the value to validation_rule

		Parameters:
			validation_rule (dict) : An instance of dict
		"""
		self.__validation_rule = validation_rule
		self.__key_modified["validation_rule"] = 1

	def get_multi_module_lookup(self):
		"""
		The method to get the multi_module_lookup

		Returns:
			dict: An instance of dict
		"""
		return self.__multi_module_lookup

	def set_multi_module_lookup(self, multi_module_lookup):
		"""
		The method to set the value to multi_module_lookup

		Parameters:
			multi_module_lookup (dict) : An instance of dict
		"""
		self.__multi_module_lookup = multi_module_lookup
		self.__key_modified["multi_module_lookup"] = 1

	def get_formula(self):
		"""
		The method to get the formula

		Returns:
			Formula: An instance of Formula
		"""
		return self.__formula

	def set_formula(self, formula):
		"""
		The method to set the value to formula

		Parameters:
			formula (Formula) : An instance of Formula
		"""
		self.__formula = formula
		self.__key_modified["formula"] = 1

	def get_unique(self):
		"""
		The method to get the unique

		Returns:
			Unique: An instance of Unique
		"""
		return self.__unique

	def set_unique(self, unique):
		"""
		The method to set the value to unique

		Parameters:
			unique (Unique) : An instance of Unique
		"""
		self.__unique = unique
		self.__key_modified["unique"] = 1

	def get_multiselectlookup(self):
		"""
		The method to get the multiselectlookup

		Returns:
			MultiSelectLookup: An instance of MultiSelectLookup
		"""
		return self.__multiselectlookup

	def set_multiselectlookup(self, multiselectlookup):
		"""
		The method to set the value to multiselectlookup

		Parameters:
			multiselectlookup (MultiSelectLookup) : An instance of MultiSelectLookup
		"""
		self.__multiselectlookup = multiselectlookup
		self.__key_modified["multiselectlookup"] = 1

	def get_auto_number(self):
		"""
		The method to get the auto_number

		Returns:
			AutoNumber: An instance of AutoNumber
		"""
		return self.__auto_number

	def set_auto_number(self, auto_number):
		"""
		The method to set the value to auto_number

		Parameters:
			auto_number (AutoNumber) : An instance of AutoNumber
		"""
		self.__auto_number = auto_number
		self.__key_modified["auto_number"] = 1

	def get_businesscard_supported(self):
		"""
		The method to get the businesscard_supported

		Returns:
			bool: A bool value
		"""
		return self.__businesscard_supported

	def set_businesscard_supported(self, businesscard_supported):
		"""
		The method to set the value to businesscard_supported

		Parameters:
			businesscard_supported (bool) : A bool value
		"""
		self.__businesscard_supported = businesscard_supported
		self.__key_modified["businesscard_supported"] = 1

	def get_history_tracking(self):
		"""
		The method to get the history_tracking

		Returns:
			bool: A bool value
		"""
		return self.__history_tracking

	def set_history_tracking(self, history_tracking):
		"""
		The method to set the value to history_tracking

		Parameters:
			history_tracking (bool) : A bool value
		"""
		self.__history_tracking = history_tracking
		self.__key_modified["history_tracking"] = 1

	def get_currency(self):
		"""
		The method to get the currency

		Returns:
			Currency: An instance of Currency
		"""
		return self.__currency

	def set_currency(self, currency):
		"""
		The method to set the value to currency

		Parameters:
			currency (Currency) : An instance of Currency
		"""
		self.__currency = currency
		self.__key_modified["currency"] = 1

	def get_lookup(self):
		"""
		The method to get the lookup

		Returns:
			Module: An instance of Module
		"""
		return self.__lookup

	def set_lookup(self, lookup):
		"""
		The method to set the value to lookup

		Parameters:
			lookup (Module) : An instance of Module
		"""
		self.__lookup = lookup
		self.__key_modified["lookup"] = 1

	def get_subform(self):
		"""
		The method to get the subform

		Returns:
			Module: An instance of Module
		"""
		return self.__subform

	def set_subform(self, subform):
		"""
		The method to set the value to subform

		Parameters:
			subform (Module) : An instance of Module
		"""
		self.__subform = subform
		self.__key_modified["subform"] = 1

	def get_convert_mapping(self):
		"""
		The method to get the convert_mapping

		Returns:
			dict: An instance of dict
		"""
		return self.__convert_mapping

	def set_convert_mapping(self, convert_mapping):
		"""
		The method to set the value to convert_mapping

		Parameters:
			convert_mapping (dict) : An instance of dict
		"""
		self.__convert_mapping = convert_mapping
		self.__key_modified["convert_mapping"] = 1

	def get_pick_list_values(self):
		"""
		The method to get the pick_list_values

		Returns:
			list: An instance of list
		"""
		return self.__pick_list_values

	def set_pick_list_values(self, pick_list_values):
		"""
		The method to set the value to pick_list_values

		Parameters:
			pick_list_values (list) : An instance of list
		"""
		self.__pick_list_values = pick_list_values
		self.__key_modified["pick_list_values"] = 1

	def get_data_type(self):
		"""
		The method to get the data_type

		Returns:
			string: A string value
		"""
		return self.__data_type

	def set_data_type(self, data_type):
		"""
		The method to set the value to data_type

		Parameters:
			data_type (string) : A string value
		"""
		self.__data_type = data_type
		self.__key_modified["data_type"] = 1

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
