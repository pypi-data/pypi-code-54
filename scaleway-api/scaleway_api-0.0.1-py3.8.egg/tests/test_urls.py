"""Test that our URLs match expectations"""
from unittest import TestCase
from unittest.mock import patch
from scaleway_api import Scaleway

class UrlTests(TestCase):
    """Test that the URLs for the API match expectations"""

    def test_api_version(self):
        scw = Scaleway(version="v99")
        self.assertEqual(
            "https://api.scaleway.com/instance/v99/zones/fr-par-1/servers",
            str(scw.instance.servers))

    @patch("os.environ", {"SCW_API_VERSION": "v100"})
    def test_api_version_environment_variable(self):
        scw = Scaleway()
        self.assertEqual(
            "https://api.scaleway.com/instance/v100/zones/fr-par-1/servers",
            str(scw.instance.servers))

    def test_default_zone(self):
        scw = Scaleway(region="test-region")
        self.assertEqual(
            "https://api.scaleway.com/instance/v1/zones/test-region-1/servers",
            str(scw.instance.servers))

    @patch("os.environ", {"SCW_DEFAULT_REGION": "test-region"})
    def test_region_environment_variable(self):
        scw = Scaleway()
        self.assertEqual(
            "https://api.scaleway.com/instance/v1/zones/test-region-1/servers",
            str(scw.instance.servers))