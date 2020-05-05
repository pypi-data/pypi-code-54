"""
    Umbrella API service class and custom exceptions.
"""

import logging

import requests

from umbrella_cli import serializers


class ApiError(Exception): pass
class ApiAuthenticationError(ApiError): pass
class ApiNotFoundError(ApiError): pass


class ManagementApiService:
    BASE_URL = "https://management.api.umbrella.com/v1"
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    def _authenticate(self, access, secret):
        """ Returns the Basic Authorization object"""
        return requests.auth.HTTPBasicAuth(access, secret)

    def _check_response_code(self, response):
        """ Raises an exception based on the status_code property """
        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            raise ApiAuthenticationError(
                "An authentication error occured. Please check your API keys."
            )
        elif response.status_code == 404:
            raise ApiNotFoundError("The URL is not found. Is your URL valid?")
        else:
            raise ApiError("An error occured with the API: {code}:{body}".format(
                code=response.status_code,
                body=response.text
            ))

    def __init__(self, access, secret, org_id):
        self.org_id = org_id
        self.auth = self._authenticate(access, secret)

    def get_site(self, site_id):
        """ Returns a single site using the site ID"""
        url = self.BASE_URL + "/organizations/{org_id}/sites/{site_id}".format(
            org_id=self.org_id,
            site_id=site_id
        )

        schema = serializers.SiteSerializer()

        response = requests.get(
            url, headers=self.HEADERS, 
            auth=self.auth, verify=False
        )

        if self._check_response_code(response):
            return schema.load(response.json())

    def get_sites(self):
        """ Returns all sites """
        url = self.BASE_URL + "/organizations/{org_id}/sites".format(
            org_id=self.org_id
        )

        schema = serializers.SiteSerializer(many=True)

        response = requests.get(
            url, headers=self.HEADERS, 
            auth=self.auth, verify=False
        )

        if self._check_response_code(response):
            return schema.load(response.json())
        
    def create_site(self, site):
        """ Create a single site from a Site model and returns a new Site"""
        url = self.BASE_URL + "/organizations/{org_id}/sites".format(
            org_id=self.org_id
        )

        schema = serializers.SiteSerializer()

        payload = schema.dump(site)

        response = requests.post(
            url, headers=self.HEADERS, auth=self.auth,
            json=payload, verify=False
        )

        if self._check_response_code(response):
            return schema.load(response.json())