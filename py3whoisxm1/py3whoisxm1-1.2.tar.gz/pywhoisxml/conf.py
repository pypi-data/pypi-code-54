import requests
from pywhoisxml.exceptions import PyWhoisException
URL_DEFAULTS = {
    "lookup_url": "https://www.whoisxmlapi.com/whoisserver/WhoisService",
    "email_verification":"https://emailverification.whoisxmlapi.com/api/v1",
    "screenshot":"https://website-screenshot.whoisxmlapi.com/api/v1",
    "ip_address":"https://ip-geolocation.whoisxmlapi.com/api/v1",
    "reputation":"https://domain-reputation.whoisxmlapi.com/api/v1",
    "balance":"https://user.whoisxmlapi.com/service/account-balance",
    "dns_lookup":"https://www.whoisxmlapi.com/whoisserver/DNSService",
    "contacts_list":"https://website-contacts.whoisxmlapi.com/api/v1"
}


def get_response(url, params):
    response = requests.get(url, params=params)
    response = response.json()

    if not 'Error' in response:
        return response
    else :    
      raise PyWhoisException(
        "Make sure you have passed the right params ,Please Try again later",response)
  
def return_value(response,key):
        return response.get(key)


  