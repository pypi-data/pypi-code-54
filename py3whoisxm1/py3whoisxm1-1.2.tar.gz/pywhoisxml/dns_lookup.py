from pywhoisxml.conf import URL_DEFAULTS,return_value
from pywhoisxml.exceptions import PyWhoisException
from pywhoisxml.auth import Auth


class DnsLookup(Auth):
    def __init__(self, api_key, domain, **kwargs):
        self.code = 26
        super().__init__(api_key, self.code,**kwargs)
        self.domain = domain

        self.url = URL_DEFAULTS.get("dns_lookup")
        self.params =self.default_params
        self.params.update({
            "domainName":self.domain
        })
        self.response = self.get_response(self.url, self.params)

    @property
    def types(self):
        return return_value(self.response, 'types')

    @property
    def dns_records(self):
        return return_value(self.response, 'dnsRecords')
