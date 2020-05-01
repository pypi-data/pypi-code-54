from pywhoisxml.exceptions import PyWhoisException
import requests

class Auth(object):
    
    def __init__(self, api_key, code,**kwargs):

        
        self.api_key = api_key
        self.code = code
        self.default_params = {
            "apiKey":api_key,
            "outputFormat":"JSON"
        }
        self.default_params.update(kwargs)

    @property
    def balance(self):
        res = requests.get(
            "https://user.whoisxmlapi.com/service/account-balance", params={"apiKey": self.api_key}).json()
        res = res.get('data')
        for item in res:
         if item['product_id'] == self.code:
            return item.get('credits')
        return None
    def get_response(self,url, params):
        response = requests.get(url, params=params)
        response = response.json()

        if not 'Error' in response:
            return response
        else :    
         raise PyWhoisException(
            "Make sure you have passed the right params ,Please Try again later",response)
        
