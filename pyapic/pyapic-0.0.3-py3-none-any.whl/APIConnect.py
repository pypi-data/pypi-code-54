# -*- coding: utf-8 -*-

import os
import sys
import oyaml as yaml
import json
import logging
import requests
import argparse
import traceback
import dateutil.parser

logger = logging.getLogger(__name__)


class APIConnectError(Exception):
    def __init__(self, message):
        super().__init__(message)


class APIConnect:

    def __init__(self, manager, debug=False):
        self.token = None
        self.manager = manager
        self.debug_requests = debug
        self.verify_ssl = True
        self.consumer_organization = False


    def debug_response(self, response):
        if self.debug_requests:
            logger.debug(json.dumps(response.json(), indent=2))


    def login(self, username, password, realm):
        url = f'https://{self.manager}/api/token'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
        }
        payload = {
            "username": username,
            "password": password,
            "realm": realm,
            "client_id":"caa87d9a-8cd7-4686-8b6e-ee2cdc5ee267",
            "client_secret":"3ecff363-7eb3-44be-9e07-6d4386c48b0b",
            "grant_type":"password"
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        self.token = response.json()['access_token']

        return self.token


    def keystores(self, organization):
        url = f'https://{self.manager}/api/orgs/{organization}/keystores'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(url, headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()['results']


    def create_keystore(self, organization, title, keystore, password=None, summary=None):
        url = f'https://{self.manager}/api/orgs/{organization}/keystores'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        payload = {
            "title": title,
            "summary": summary,
            "password": password,
            "keystore": keystore,
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()


    def delete_keystore(self, organization, name):
        url = f'https://{self.manager}/api/orgs/{organization}/keystores/{name}'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.delete(url, headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return None


    def tls_client_profiles(self, organization):
        url = f'https://{self.manager}/api/orgs/{organization}/tls-client-profiles'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(url, headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()['results']


    def delete_tls_client_profile(self, organization, name):
        url = f'https://{self.manager}/api/orgs/{organization}/tls-client-profiles?confirm={organization}'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.delete(url, headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return None


    def create_tls_client_profile(self, organization, title, keystore, summary=None):
        url = f'https://{self.manager}/api/orgs/{organization}/tls-client-profiles'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        payload = {
            "ciphers": [
                "ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
                "ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                "ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
                "ECDHE_RSA_WITH_AES_256_CBC_SHA384",
                "ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
                "ECDHE_RSA_WITH_AES_256_CBC_SHA",
                "DHE_DSS_WITH_AES_256_GCM_SHA384",
                "DHE_RSA_WITH_AES_256_GCM_SHA384",
                "DHE_RSA_WITH_AES_256_CBC_SHA256",
                "DHE_DSS_WITH_AES_256_CBC_SHA256",
                "DHE_RSA_WITH_AES_256_CBC_SHA",
                "DHE_DSS_WITH_AES_256_CBC_SHA",
                "RSA_WITH_AES_256_GCM_SHA384",
                "RSA_WITH_AES_256_CBC_SHA256",
                "RSA_WITH_AES_256_CBC_SHA",
                "ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
                "ECDHE_RSA_WITH_AES_128_GCM_SHA256",
                "ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
                "ECDHE_RSA_WITH_AES_128_CBC_SHA256",
                "ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
                "ECDHE_RSA_WITH_AES_128_CBC_SHA",
                "DHE_DSS_WITH_AES_128_GCM_SHA256",
                "DHE_RSA_WITH_AES_128_GCM_SHA256",
                "DHE_RSA_WITH_AES_128_CBC_SHA256",
                "DHE_DSS_WITH_AES_128_CBC_SHA256",
                "DHE_RSA_WITH_AES_128_CBC_SHA",
                "DHE_DSS_WITH_AES_128_CBC_SHA",
                "RSA_WITH_AES_128_GCM_SHA256",
                "RSA_WITH_AES_128_CBC_SHA256",
                "RSA_WITH_AES_128_CBC_SHA"
            ],
            "title": title,
            "version": "1.0.0",
            "summary": summary,
            "insecure_server_connections": False,
            "server_name_indication": True,
            "keystore_url": keystore,
            "protocols": [
                "tls_v1.0",
                "tls_v1.1",
                "tls_v1.2"
            ]
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()


    def catalog_tls_client_profiles(self, organization, catalog):
        url = f'https://{self.manager}/api/catalogs/{organization}/{catalog}/configured-tls-client-profiles'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(url, headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()['results']


    def delete_configured_tls_client_profile(self, organization, catalog, name):
        url = f'https://{self.manager}/api/catalogs/{organization}/{catalog}/configured-tls-client-profiles/{name}?confirm={catalog}'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.delete(url, headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return None


    def add_tls_client_profile(self, organization, catalog, tls_client_profile):
        url = f'https://{self.manager}/api/catalogs/{organization}/{catalog}/configured-tls-client-profiles'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        payload = {
            "tls_client_profile_url": tls_client_profile
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()


    def catalog_properties_create(self, organization, catalog, properties):
        url = f'https://{self.manager}/api/catalogs/{organization}/{catalog}/properties'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        payload = properties

        response = requests.patch(url, data=json.dumps(payload), headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()


    def catalog_properties(self, organization, catalog):
        url = f'https://{self.manager}/api/catalogs/{organization}/{catalog}/properties'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(url, headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()


    def catalog_products(self, organization, catalog):
        url = f'https://{self.manager}/api/catalogs/{organization}/{catalog}/products'
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(url, headers=headers, verify=self.verify_ssl)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()


    def product_publish(self, organization, catalog, product, files, space=None):

        if space:
            url = f'https://{self.manager}/api/spaces/{organization}/{catalog}/{space}/publish'
        else:
            url = f'https://{self.manager}/api/catalogs/{organization}/{catalog}/publish'
        headers = {
            # 'Content-Type': 'multipart/form-data', ¡Do not set Content-Type!, requests will do it
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.post(url, headers=headers, files=files, verify=self.verify_ssl, timeout=300)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()


    def product_get(self, organization, catalog, product, version=None):

        url = f"https://{self.manager}/api/catalogs/{organization}/{catalog}/products/{product}"
        if version:
            url += f"/{version}"

        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers, verify=False)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()


    def last_published(self, products):
        # Get the last published product from a list
        published = [p for p in products['results'] if p['state'] == "published"]
        products = sorted(published, key=lambda x: dateutil.parser.isoparse(x['updated_at']), reverse=True)

        return products[0] if products else None


    def subscription_create(self, product, organization, catalog, application, plan, consumer_organization=None):

        consumer_organization = consumer_organization or self.consumer_organization
        if not consumer_organization:
            raise APIConnectError("Consumer organization not specified")

        url = f"https://{self.manager}/api/apps/{organization}/{catalog}/{consumer_organization}/{application}/subscriptions"
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        payload = {
            # "title": "{product} {application} {plan}",
            "plan": plan,
            "product_url": product
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=self.verify_ssl, timeout=300)
        self.debug_response(response)
        response.raise_for_status()

        return response.json()


    def get_subscriptions(self, application, catalog):

        consumer_organization = consumer_organization or self.consumer_organization
        if not consumer_organization:
            raise APIConnectError("Consumer organization not specified")

        url = f"https://{self.manager}/api/apps/{organization}/{catalog}/{consumer_organization}/{application}/subscriptions"
        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Authorization": "Bearer %s" % SESSION['token']
        }
        response = requests.get(url, headers=headers, verify=False)
        # print(json.dumps(response.json(), indent=2))

        response.raise_for_status()

        return response.json()
