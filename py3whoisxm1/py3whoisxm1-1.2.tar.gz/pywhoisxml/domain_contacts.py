from pywhoisxml.conf import URL_DEFAULTS,return_value
from pywhoisxml.exceptions import PyWhoisException
from pywhoisxml.auth import Auth


class DomainContacts(object):
    def __init__(self, api_key, domain,**kwargs):
        self.code = 20
        super().__init__(api_key, self.code,**kwargs)
        self.domain = domain

        self.url = URL_DEFAULTS.get('reputation')
        self.params = self.defautf_params
        self.params.update({
            "domainName": domain
        })
        self.response = self.get_response(self.url, self.params)

    @property
    def company_names(self):
        return return_value(self.response, 'companyNames')

    @property
    def emails(self):
        return return_value(self.response, "emails")

    @property
    def description(self):
        return self.response['meta']['description']

    @property
    def facebook_link(self):
        return self.response['socialLinks']['facebook']

    @property
    def instagram_link(self):
        return self.response['socialLinks']['instagram']

    @property
    def linkedin_link(self):
        return self.response['socialLinks']['linkedIn']

    @property
    def twitter_link(self):
        return self.response['socialLinks']['twitter']
