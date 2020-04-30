from ..HTTP.Requests import *
from .hubspot import BASE_URL
from .hubspot import HEADERS

def search_contacts_by_property_value(property_name, property_value, property_names, after=None):
  filters = [
    {
      'propertyName': property_name,
      'operator': 'EQ',
      'value': property_value
    }
  ]
  return search_contacts(property_names, filters, after)

def search_contacts_by_property_known(property_name, property_names, after=None):
  filters = [
    {
      'propertyName': property_name,
      'operator': 'HAS_PROPERTY'
    }
  ]
  return search_contacts(property_names, filters, after)

def search_contacts_by_property_less_than(property_name, property_value, property_names, after=None):
  filters = [
    {
      'propertyName': property_name,
      'operator': 'LT',
      'value': property_value
    }
  ]
  return search_contacts(property_names, filters, after)

def search_contacts_by_property_greater_than(property_name, property_value, property_names, after=None):
  filters = [
    {
      'propertyName': property_name,
      'operator': 'GT',
      'value': property_value
    }
  ]
  return search_contacts(property_names, filters, after)

def search_contacts_by_property_values(property_name, property_values, property_names, after=None):
  filters = [
    {
      'propertyName': property_name,
      'operator': 'IN',
      'values': property_values
    }
  ]
  return search_contacts(property_names, filters, after)

def search_contacts(property_names, filters, after=None):
  post_url = f"{BASE_URL}crm/v3/objects/contacts/search"
  if after:
    post_url = f"{post_url}?after={after}"
  post_body = {
    'filterGroups': [
      {
        'filters': filters
      }
    ],
    'sorts': [],
    'properties': property_names,
    'limit': 100
  }
  result = post(post_url, HEADERS, json.dumps(post_body))
  if not Utils.is_success(result['status_code']):
    raise Exception(f"Failed to search contacts. Result: {result}")
  return result

def get_contact(contact_id, property_names=None, associations=None):
  post_url = f"{BASE_URL}crm/v3/objects/contacts/{contact_id}?archived=false"
  if property_names:
    post_url = f"{post_url}&properties={'%2C'.join(property_names)}"
    
  if associations:
    post_url = f"{post_url}&associations={'%2C'.join(associations)}"
  result = get(post_url, HEADERS)
  if not Utils.is_success(result['status_code']):
    raise Exception(f"Failed to retrieve contact. Result: {result}")
  return result

def create_contact(properties):
  post_url = f"{BASE_URL}crm/v3/objects/companies"
  post_body = {
    'properties': properties
  }
  result = post(post_url, HEADERS, json.dumps(post_body))
  if not Utils.is_success(result['status_code']):
    raise Exception(f"Failed to create contact. Result: {result}")
  return result

def update_contact(contact_id, properties):
  post_url = f"{BASE_URL}crm/v3/objects/contacts/{contact_id}?"
  post_body = {
    'properties': properties
  }
  result = patch(post_url, HEADERS, json.dumps(post_body))
  if not Utils.is_success(result['status_code']):
    raise Exception(f"Failed to update contact. Result: {result}")
  return result