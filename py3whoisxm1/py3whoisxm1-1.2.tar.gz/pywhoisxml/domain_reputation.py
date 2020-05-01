from pywhoisxml.conf import URL_DEFAULTS,return_value
from pywhoisxml.exceptions import PyWhoisException
from pywhoisxml.auth import Auth


class DomainReputation(Auth):
    def __init__(self, api_key, domain,**kwargs):
        self.code = 20
        super().__init__(api_key, self.code, **kwargs)
        self.domain = domain

        self.url = URL_DEFAULTS.get('reputation')
        self.params = self.default_params

        self.params.update({
            "domainName": domain
        })
        self.response = self.get_response(self.url, self.params)

    @property
    def data(self):
        return self.response

    @property
    def score(self):
        return return_value(self.response, "reputationScore")

    @property
    def balance(self):
        return get_balance(self.api_key, self.code)
