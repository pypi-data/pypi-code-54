from ..util import Model


class User(Model):
	def __init__(self):
		self.__name = None
		self.__id = None
		self.__country = None
		self.__city = None
		self.__signature = None
		self.__name_format = None
		self.__language = None
		self.__locale = None
		self.__personal_account = None
		self.__default_tab_group = None
		self.__street = None
		self.__alias = None
		self.__state = None
		self.__country_locale = None
		self.__first_name = None
		self.__email = None
		self.__zip = None
		self.__decimal_separator = None
		self.__website = None
		self.__time_format = None
		self.__mobile = None
		self.__last_name = None
		self.__time_zone = None
		self.__zuid = None
		self.__confirm = None
		self.__full_name = None
		self.__phone = None
		self.__dob = None
		self.__date_format = None
		self.__status = None
		self.__microsoft = None
		self.__isonline = None
		self.__currency = None
		self.__offset = None
		self.__profile = None
		self.__role = None
		self.__territories = None
		self.__theme = None
		self.__customize_info = None
		self.__key_modified = dict()

	def get_name(self):
		"""
		The method to get the name

		Returns:
			string: A string value
		"""
		return self.__name

	def set_name(self, name):
		"""
		The method to set the value to name

		Parameters:
			name (string) : A string value
		"""
		self.__name = name
		self.__key_modified["name"] = 1

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

	def get_country(self):
		"""
		The method to get the country

		Returns:
			string: A string value
		"""
		return self.__country

	def set_country(self, country):
		"""
		The method to set the value to country

		Parameters:
			country (string) : A string value
		"""
		self.__country = country
		self.__key_modified["country"] = 1

	def get_city(self):
		"""
		The method to get the city

		Returns:
			string: A string value
		"""
		return self.__city

	def set_city(self, city):
		"""
		The method to set the value to city

		Parameters:
			city (string) : A string value
		"""
		self.__city = city
		self.__key_modified["city"] = 1

	def get_signature(self):
		"""
		The method to get the signature

		Returns:
			string: A string value
		"""
		return self.__signature

	def set_signature(self, signature):
		"""
		The method to set the value to signature

		Parameters:
			signature (string) : A string value
		"""
		self.__signature = signature
		self.__key_modified["signature"] = 1

	def get_name_format(self):
		"""
		The method to get the name_format

		Returns:
			string: A string value
		"""
		return self.__name_format

	def set_name_format(self, name_format):
		"""
		The method to set the value to name_format

		Parameters:
			name_format (string) : A string value
		"""
		self.__name_format = name_format
		self.__key_modified["name_format"] = 1

	def get_language(self):
		"""
		The method to get the language

		Returns:
			string: A string value
		"""
		return self.__language

	def set_language(self, language):
		"""
		The method to set the value to language

		Parameters:
			language (string) : A string value
		"""
		self.__language = language
		self.__key_modified["language"] = 1

	def get_locale(self):
		"""
		The method to get the locale

		Returns:
			string: A string value
		"""
		return self.__locale

	def set_locale(self, locale):
		"""
		The method to set the value to locale

		Parameters:
			locale (string) : A string value
		"""
		self.__locale = locale
		self.__key_modified["locale"] = 1

	def get_personal_account(self):
		"""
		The method to get the personal_account

		Returns:
			bool: A bool value
		"""
		return self.__personal_account

	def set_personal_account(self, personal_account):
		"""
		The method to set the value to personal_account

		Parameters:
			personal_account (bool) : A bool value
		"""
		self.__personal_account = personal_account
		self.__key_modified["personal_account"] = 1

	def get_default_tab_group(self):
		"""
		The method to get the default_tab_group

		Returns:
			string: A string value
		"""
		return self.__default_tab_group

	def set_default_tab_group(self, default_tab_group):
		"""
		The method to set the value to default_tab_group

		Parameters:
			default_tab_group (string) : A string value
		"""
		self.__default_tab_group = default_tab_group
		self.__key_modified["default_tab_group"] = 1

	def get_street(self):
		"""
		The method to get the street

		Returns:
			string: A string value
		"""
		return self.__street

	def set_street(self, street):
		"""
		The method to set the value to street

		Parameters:
			street (string) : A string value
		"""
		self.__street = street
		self.__key_modified["street"] = 1

	def get_alias(self):
		"""
		The method to get the alias

		Returns:
			string: A string value
		"""
		return self.__alias

	def set_alias(self, alias):
		"""
		The method to set the value to alias

		Parameters:
			alias (string) : A string value
		"""
		self.__alias = alias
		self.__key_modified["alias"] = 1

	def get_state(self):
		"""
		The method to get the state

		Returns:
			string: A string value
		"""
		return self.__state

	def set_state(self, state):
		"""
		The method to set the value to state

		Parameters:
			state (string) : A string value
		"""
		self.__state = state
		self.__key_modified["state"] = 1

	def get_country_locale(self):
		"""
		The method to get the country_locale

		Returns:
			string: A string value
		"""
		return self.__country_locale

	def set_country_locale(self, country_locale):
		"""
		The method to set the value to country_locale

		Parameters:
			country_locale (string) : A string value
		"""
		self.__country_locale = country_locale
		self.__key_modified["country_locale"] = 1

	def get_first_name(self):
		"""
		The method to get the first_name

		Returns:
			string: A string value
		"""
		return self.__first_name

	def set_first_name(self, first_name):
		"""
		The method to set the value to first_name

		Parameters:
			first_name (string) : A string value
		"""
		self.__first_name = first_name
		self.__key_modified["first_name"] = 1

	def get_email(self):
		"""
		The method to get the email

		Returns:
			string: A string value
		"""
		return self.__email

	def set_email(self, email):
		"""
		The method to set the value to email

		Parameters:
			email (string) : A string value
		"""
		self.__email = email
		self.__key_modified["email"] = 1

	def get_zip(self):
		"""
		The method to get the zip

		Returns:
			string: A string value
		"""
		return self.__zip

	def set_zip(self, zip):
		"""
		The method to set the value to zip

		Parameters:
			zip (string) : A string value
		"""
		self.__zip = zip
		self.__key_modified["zip"] = 1

	def get_decimal_separator(self):
		"""
		The method to get the decimal_separator

		Returns:
			string: A string value
		"""
		return self.__decimal_separator

	def set_decimal_separator(self, decimal_separator):
		"""
		The method to set the value to decimal_separator

		Parameters:
			decimal_separator (string) : A string value
		"""
		self.__decimal_separator = decimal_separator
		self.__key_modified["decimal_separator"] = 1

	def get_website(self):
		"""
		The method to get the website

		Returns:
			string: A string value
		"""
		return self.__website

	def set_website(self, website):
		"""
		The method to set the value to website

		Parameters:
			website (string) : A string value
		"""
		self.__website = website
		self.__key_modified["website"] = 1

	def get_time_format(self):
		"""
		The method to get the time_format

		Returns:
			string: A string value
		"""
		return self.__time_format

	def set_time_format(self, time_format):
		"""
		The method to set the value to time_format

		Parameters:
			time_format (string) : A string value
		"""
		self.__time_format = time_format
		self.__key_modified["time_format"] = 1

	def get_mobile(self):
		"""
		The method to get the mobile

		Returns:
			string: A string value
		"""
		return self.__mobile

	def set_mobile(self, mobile):
		"""
		The method to set the value to mobile

		Parameters:
			mobile (string) : A string value
		"""
		self.__mobile = mobile
		self.__key_modified["mobile"] = 1

	def get_last_name(self):
		"""
		The method to get the last_name

		Returns:
			string: A string value
		"""
		return self.__last_name

	def set_last_name(self, last_name):
		"""
		The method to set the value to last_name

		Parameters:
			last_name (string) : A string value
		"""
		self.__last_name = last_name
		self.__key_modified["last_name"] = 1

	def get_time_zone(self):
		"""
		The method to get the time_zone

		Returns:
			string: A string value
		"""
		return self.__time_zone

	def set_time_zone(self, time_zone):
		"""
		The method to set the value to time_zone

		Parameters:
			time_zone (string) : A string value
		"""
		self.__time_zone = time_zone
		self.__key_modified["time_zone"] = 1

	def get_zuid(self):
		"""
		The method to get the zuid

		Returns:
			string: A string value
		"""
		return self.__zuid

	def set_zuid(self, zuid):
		"""
		The method to set the value to zuid

		Parameters:
			zuid (string) : A string value
		"""
		self.__zuid = zuid
		self.__key_modified["zuid"] = 1

	def get_confirm(self):
		"""
		The method to get the confirm

		Returns:
			bool: A bool value
		"""
		return self.__confirm

	def set_confirm(self, confirm):
		"""
		The method to set the value to confirm

		Parameters:
			confirm (bool) : A bool value
		"""
		self.__confirm = confirm
		self.__key_modified["confirm"] = 1

	def get_full_name(self):
		"""
		The method to get the full_name

		Returns:
			string: A string value
		"""
		return self.__full_name

	def set_full_name(self, full_name):
		"""
		The method to set the value to full_name

		Parameters:
			full_name (string) : A string value
		"""
		self.__full_name = full_name
		self.__key_modified["full_name"] = 1

	def get_phone(self):
		"""
		The method to get the phone

		Returns:
			string: A string value
		"""
		return self.__phone

	def set_phone(self, phone):
		"""
		The method to set the value to phone

		Parameters:
			phone (string) : A string value
		"""
		self.__phone = phone
		self.__key_modified["phone"] = 1

	def get_dob(self):
		"""
		The method to get the dob

		Returns:
			string: A string value
		"""
		return self.__dob

	def set_dob(self, dob):
		"""
		The method to set the value to dob

		Parameters:
			dob (string) : A string value
		"""
		self.__dob = dob
		self.__key_modified["dob"] = 1

	def get_date_format(self):
		"""
		The method to get the date_format

		Returns:
			string: A string value
		"""
		return self.__date_format

	def set_date_format(self, date_format):
		"""
		The method to set the value to date_format

		Parameters:
			date_format (string) : A string value
		"""
		self.__date_format = date_format
		self.__key_modified["date_format"] = 1

	def get_status(self):
		"""
		The method to get the status

		Returns:
			string: A string value
		"""
		return self.__status

	def set_status(self, status):
		"""
		The method to set the value to status

		Parameters:
			status (string) : A string value
		"""
		self.__status = status
		self.__key_modified["status"] = 1

	def get_microsoft(self):
		"""
		The method to get the microsoft

		Returns:
			bool: A bool value
		"""
		return self.__microsoft

	def set_microsoft(self, microsoft):
		"""
		The method to set the value to microsoft

		Parameters:
			microsoft (bool) : A bool value
		"""
		self.__microsoft = microsoft
		self.__key_modified["microsoft"] = 1

	def get_isonline(self):
		"""
		The method to get the isonline

		Returns:
			bool: A bool value
		"""
		return self.__isonline

	def set_isonline(self, isonline):
		"""
		The method to set the value to isonline

		Parameters:
			isonline (bool) : A bool value
		"""
		self.__isonline = isonline
		self.__key_modified["Isonline"] = 1

	def get_currency(self):
		"""
		The method to get the currency

		Returns:
			string: A string value
		"""
		return self.__currency

	def set_currency(self, currency):
		"""
		The method to set the value to currency

		Parameters:
			currency (string) : A string value
		"""
		self.__currency = currency
		self.__key_modified["Currency"] = 1

	def get_offset(self):
		"""
		The method to get the offset

		Returns:
			string: A string value
		"""
		return self.__offset

	def set_offset(self, offset):
		"""
		The method to set the value to offset

		Parameters:
			offset (string) : A string value
		"""
		self.__offset = offset
		self.__key_modified["offset"] = 1

	def get_profile(self):
		"""
		The method to get the profile

		Returns:
			Profile: An instance of Profile
		"""
		return self.__profile

	def set_profile(self, profile):
		"""
		The method to set the value to profile

		Parameters:
			profile (Profile) : An instance of Profile
		"""
		self.__profile = profile
		self.__key_modified["profile"] = 1

	def get_role(self):
		"""
		The method to get the role

		Returns:
			Role: An instance of Role
		"""
		return self.__role

	def set_role(self, role):
		"""
		The method to set the value to role

		Parameters:
			role (Role) : An instance of Role
		"""
		self.__role = role
		self.__key_modified["role"] = 1

	def get_territories(self):
		"""
		The method to get the territories

		Returns:
			list: An instance of list
		"""
		return self.__territories

	def set_territories(self, territories):
		"""
		The method to set the value to territories

		Parameters:
			territories (list) : An instance of list
		"""
		self.__territories = territories
		self.__key_modified["territories"] = 1

	def get_theme(self):
		"""
		The method to get the theme

		Returns:
			Theme: An instance of Theme
		"""
		return self.__theme

	def set_theme(self, theme):
		"""
		The method to set the value to theme

		Parameters:
			theme (Theme) : An instance of Theme
		"""
		self.__theme = theme
		self.__key_modified["theme"] = 1

	def get_customize_info(self):
		"""
		The method to get the customize_info

		Returns:
			CustomizeInfo: An instance of CustomizeInfo
		"""
		return self.__customize_info

	def set_customize_info(self, customize_info):
		"""
		The method to set the value to customize_info

		Parameters:
			customize_info (CustomizeInfo) : An instance of CustomizeInfo
		"""
		self.__customize_info = customize_info
		self.__key_modified["customize_info"] = 1

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
