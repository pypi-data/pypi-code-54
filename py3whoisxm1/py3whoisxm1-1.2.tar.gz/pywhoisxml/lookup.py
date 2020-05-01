from pywhoisxml.conf import URL_DEFAULTS
from pywhoisxml.auth import Auth
from pywhoisxml.exceptions import PyWhoisException


class Lookup(Auth):
    def __init__(self, api_key, domain,**kwargs):
        self.code = 1
        super().__init__(api_key,self.code,**kwargs)
        self.domain = domain
        self.url = URL_DEFAULTS.get('lookup_url')
        self.params = self.default_params
        self.params.update({
            "da":1,
            "domainName":domain
        })
        self.response = self.get_response(self.url, self.params)['WhoisRecord']
        self.is_com = self.check_is_com()

    def check_is_com(self):
        try:
            ext = self.domain.split('.')[1]
            if ext == "com":
                return True
            return False
        except Exception as e:
            raise PyWhoisException("Enter a valid domain")

    @property
    def data(self):
        return self.response

    @property
    def registered_by(self):
        if self.is_com:

            return self.response["registrant"]["organization"]
        return self.response['registrarName']

    @property
    def is_available(self):
        if self.response['domainAvailability'] == "UNAVAILABLE":
            return False
        return True

    @property
    def created_at(self):
        if self.is_com:
            return self.response['createdDate']
        return self.response['audit']['createdDate']

    @property
    def raw_text(self):
        return self.response['rawText']
