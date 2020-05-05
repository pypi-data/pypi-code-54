"""
This modules includes all the tests related to Click cubcommands.
"""

from unittest import mock
import pytest
from click.testing import CliRunner

from umbrella_cli import cli
from umbrella_cli.services import ManagementApiService, ApiError
from umbrella_cli.models import Site

class TestSitesCommands:

    @pytest.fixture
    def credentials(self):
        return [
            "--access", "ACCESS_KEY", "--secret",
            "SECRET_KEY", "--org", "1234567"
        ]

    @mock.patch.object(ManagementApiService, "get_sites", autospec=True)
    def test_sites_get_all(self, mock_api_service, credentials):
        """ Test the output of fetching all sites """
        runner = CliRunner()
        mock_api_service.return_value = [
            Site(site_id=1479824, name="BLUE"),
            Site(site_id=1234567, name="Default Site")
        ]

        result = runner.invoke(cli, credentials + ["sites", "get-all"])

        assert "Umbrella Sites for Organization" in result.output
        assert "1479824 | BLUE" in result.output

    @mock.patch.object(ManagementApiService, "get_sites", autospec=True)
    def test_services_exception_handling(self, mock_api_service, credentials):
        """ Test the exception handling of the service layer """
        runner = CliRunner()
        mock_api_service.side_effect = ApiError("An error occured in services.")

        result = runner.invoke(cli, credentials + ["sites", "get-all"])

        assert "An error occured in services." in result.output

    @mock.patch.object(ManagementApiService, "create_site", autospec=True)
    def test_site_create(self, mock_api_service, credentials):
        runner = CliRunner()
        mock_api_service.return_value = Site(site_id=123456, name="TEST")
        
        result = runner.invoke(cli, credentials + ["sites", "create", "TEST"])

        assert "New site created with ID 123456" in result.output