import socket
import json
import os
import sys

if sys.version_info[0] == 2:
    import httplib as http_client
    from urlparse import urlparse
elif sys.version_info[0] == 3:
    import http.client as http_client
    from urllib.parse import urlparse

from .errors import *


class BuddyNSAPI:
    def __init__(self, key, endpoint='https://www.buddyns.com/api/v2/', validate_auth=True, timeout=4):
        """Construct a client to the BuddyNS API.
        
        @param key          authentication token
        @param endpoint     optional custom API base URL"""
        # permit overriding default API base with environment variable
        if 'BUDDYNS_API_DESTINATION' in os.environ:
            endpoint = os.environ['BUDDYNS_API_DESTINATION']
        self.endpoint = self.parse_base(endpoint)
        self.apikey = key
        self.base_path = self.endpoint[3].rstrip('/') + '/'
        self.timeout = timeout
        self.conn = None
        self.authenticated = False
        if validate_auth:
            self.validate_authentication()
   
    def validate_authentication(self):
        # issue one request to validate authentication
        if not self.conn:
            self.conn = self.connect()
        if self.authenticated:
            return True
        
        try:
            self.conn.request('GET', self.resource_path('user'), headers=self.get_headers())
            resp = self.conn.getresponse()
        except BuddyNSAPIError:
            self.conn = None
            self.authenticated = False
            raise AuthenticationFailed("Provided API key '%s' fails to authenticate." % self.apikey)
        except socket.timeout as e:
            self.conn = None
            self.authenticated = False
            raise
        except:
            self.conn = None
            self.authenticated = False
            raise

        else:
            resp_content = resp.read()
            if resp.status == 200:
                self.authenticated = True
                return True
            elif resp.status == 401:
                self.authenticated = False
                raise AuthenticationFailed("Provided API key '%s' fails to authenticate." % self.apikey)

    def __del__(self):
        self.close()

    def parse_base(self, base):
        up = urlparse(base)
        return (up.scheme, up.hostname, up.port or (443 if up.scheme == 'https' else 80), up.path)

    def reconn(fun):
        def _conrun(self, *args, **kwargs):
            if not self.conn:
                self.conn = self.connect()
            try:
                return fun(self, *args, **kwargs)
            except http_client.ImproperConnectionState:
                # reconnect and try again, once
                self.conn = self.connect()
                return fun(self, *args, **kwargs)
        return _conrun

    def connect(self):
        """Return a connection obj to the API host."""
        if self.endpoint[0] == 'https':
            return http_client.HTTPSConnection(host=self.endpoint[1], port=self.endpoint[2], timeout=self.timeout)
        return http_client.HTTPConnection(host=self.endpoint[1], port=self.endpoint[2], timeout=self.timeout)

    def close(self):
        if self.conn:
            self.conn.close()

    def get_headers(self, add_custom_headers={}):
        """Return the required headers to query API."""
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Authorization": "Token %s" % self.apikey,
            }
        headers.update(add_custom_headers)
        return headers

    def validate_status(self, status, body, wanted_status, errtype=BuddyNSAPIError, custom_msg=None):
        """Verify that a response has the wanted_status code or raise an exception with a given message.
        
        Returns nothing if response status == wanted_status. Else, it raises exceptions:
        - AuthenticationFailed if response status is 401.
        - What's indicated in errtype otherwise.

        @param errtype      is dict() or a specific Exception type. If dict, it associates status:exception_type,
                            or None:exception_type as default.
        """

        if status == wanted_status:
            return
        elif status == 401:
            raise AuthenticationFailed("Authentication failed. Check your API token!")
        
        msg = custom_msg or ('API call failed: code %d, msg "%s".' % (status, body.decode()[:200]))
        if type(errtype) is not dict:
            raise errtype(msg)
        if status in errtype:
            raise errtype[status](msg)
        elif None in errtype:
            raise errtype[None](msg)
        
        raise BuddyNSAPIError(msg)

    def element_path(self, *args):
        """Compose the path for an element (ends without /)."""
        return self.base_path + '/'.join(args)

    def resource_path(self, *args):
        """Compose the path for a resource (ends in /)."""
        return self.base_path + '/'.join(args) + '/'

    def _process_request(self, method, route, body=None, custom_headers={}, wanted_status=200, 
                         errtype=BuddyNSAPIError, error_msg=None):

        self.conn.request(method, route, body=body, headers=self.get_headers(custom_headers))
        try:
            resp = self.conn.getresponse()
        except socket.timeout as e:
            self.conn = None
            raise e
        except:
            self.conn = None
            raise
        else:
            resp_body = resp.read()
            self.validate_status(resp.status, resp_body, wanted_status, errtype, error_msg)
            if resp_body:
                return json.loads(resp_body)
            else:
                return {}

    @reconn
    def add_domain(self, domain, master):
        """Issue API call to add one domain.
        
        @param domain       (string) domain to add
        @param master       (string) IPv4 or IPv6 address of DNS master
        
        @return     (dictionary) outcome from server"""
        postbody = 'master=%s&name=%s' % (master, domain)
        method = 'POST'
        route = self.resource_path('zone')
        return self._process_request(method, route, body=postbody, wanted_status=201, 
                                     errtype=PermissionDenied)

    @reconn
    def remove_domain(self, domain):
        """Issue API call to remove a domain.
        
        @param domain   (string) name of domain to remove"""

        method = 'DELETE'
        route = self.element_path('zone', domain)
        return self._process_request(method, route, wanted_status=204, 
                                     errtype={404: DoesNotExist, 400: PermissionDenied})
    
    @reconn
    def list_domains(self):
        """Return the list of domains currently registered.
        
        @return     (list of dictionaries) domain entries registered"""
        method = 'GET'
        route = self.resource_path('zone')
        return self._process_request(method, route, wanted_status=200)

    @reconn
    def get_domain(self, domain):
        """Return the properties of a currently registered domain.

        @param domain   (string) name of domain
        
        @return     (dictionary) properties of domain."""
        method = 'GET'
        route = self.element_path('zone', domain)
        return self._process_request(method, route, wanted_status=200, errtype=DoesNotExist)

    @reconn
    def get_domain_status(self, domain):
        """Return the status properties of a currently registered domain.

        @param domain   (string) name of domain

        @return     (dictionary) status properties of domain."""
        method = 'GET'
        route = self.resource_path('zone', domain, 'status')
        return self._process_request(method, route, wanted_status=200, errtype=DoesNotExist)

    @reconn
    def get_domain_delegation(self, domain):
        """Return the delegation properties of a currently registered domain.

        @param domain   (string) name of domain

        @return     (dictionary) delegation properties of domain."""
        method = 'GET'
        route = self.resource_path('zone', domain, 'delegation')
        return self._process_request(method, route, wanted_status=200, errtype=DoesNotExist)

    @reconn
    def sync_domain(self, domain):
        """Request immediate synchronization for a domain.

        @param domain   (string) name of domain
        """
        method = 'GET'
        route = self.element_path('sync', domain)
        return self._process_request(method, route, wanted_status=204, errtype=DoesNotExist)
    
    @reconn
    def get_user(self):
        method = 'GET'
        route = self.resource_path('user')
        return self._process_request(method, route, wanted_status=200)
