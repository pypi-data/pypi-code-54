"""
    This module contains the test cases of the different commands supported by
    this tool.
"""

from unittest import mock

import pytest
from requests.auth import HTTPBasicAuth

from umbrella_cli import services
from umbrella_cli import models

class TestManagementApiService:

    @mock.patch("umbrella_cli.services.requests.get")
    def test_get_sites_ok(self, mock_requests):
        """ Test the GET sites with valid data """
        api = services.ManagementApiService("ACCESS", "SECRET", 1234567)

        assert api.org_id == 1234567
        
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = [
                {
                    "originId": 395218748,
                    "isDefault": False,
                    "name": "BLUE",
                    "modifiedAt": "2020-04-05T19:07:38.000Z",
                    "createdAt": "2020-04-05T19:07:38.000Z",
                    "type": "site",
                    "internalNetworkCount": 2,
                    "vaCount": 4,
                    "siteId": 1479824
                },
                {
                    "originId": 136056751,
                    "isDefault": True,
                    "name": "Default Site",
                    "modifiedAt": "2018-03-06T01:23:13.000Z",
                    "createdAt": "2018-03-06T01:23:13.000Z",
                    "type": "site",
                    "internalNetworkCount": 0,
                    "vaCount": 0,
                    "siteId": 635875
                }]

        sites = api.get_sites()

        mock_requests.assert_called_with(
            "https://management.api.umbrella.com/v1/organizations/1234567/sites",
            auth=HTTPBasicAuth("ACCESS", "SECRET"),
            headers=api.HEADERS,
            verify=False
        )

    @mock.patch("umbrella_cli.services.requests.get")
    def test_get_sites_404(self, mock_requests):
        """ Test the ApiNotFoundError exception """
        api = services.ManagementApiService("ACCESS", "SECRET", 1234567)

        mock_requests.return_value.status_code = 404

        with pytest.raises(services.ApiNotFoundError):
            api.get_sites()

    @mock.patch("umbrella_cli.services.requests.post")
    def test_create_site_with_valid_data(self, mock_requests):
        """ Create a site with valid data """
        api = services.ManagementApiService("ACCESS", "SECRET", 1234567)

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
                "originId": 395218748,
                "isDefault": False,
                "name": "Test",
                "modifiedAt": "2020-04-05T19:07:38.000Z",
                "createdAt": "2020-04-05T19:07:38.000Z",
                "type": "site",
                "internalNetworkCount": 2,
                "vaCount": 4,
                "siteId": 1479824
            }

        site = models.Site(name="Test")

        result = api.create_site(site)

        mock_requests.assert_called_with(
            "https://management.api.umbrella.com/v1/organizations/1234567/sites",
            headers=api.HEADERS,
            json={"name":"Test"},
            auth=HTTPBasicAuth("ACCESS", "SECRET"),
            verify=False
        )

        assert result.name == "Test"
        assert result.origin_id == 395218748
        assert result.internal_network_count == 2
        

