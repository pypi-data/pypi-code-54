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
            str(scw.instance.servers),
        )

    @patch("os.environ", {"SCW_API_VERSION": "v100"})
    def test_api_version_environment_variable(self):
        scw = Scaleway()
        self.assertEqual(
            "https://api.scaleway.com/baremetal/v100/zones/fr-par-1/servers",
            str(scw.baremetal.servers),
        )

    def test_default_zone(self):
        scw = Scaleway(region="test-region")
        self.assertEqual(
            "https://api.scaleway.com/baremetal/v1/zones/test-region-1/servers",
            str(scw.baremetal.servers),
        )

    @patch("os.environ", {"SCW_DEFAULT_REGION": "test-region"})
    def test_region_environment_variable(self):
        scw = Scaleway()
        self.assertEqual(
            "https://api.scaleway.com/lbs/v1/regions/test-region/ips", str(scw.lbs.ips)
        )

    def test_iot_beta(self):
        scw = Scaleway()
        self.assertEqual(
            "https://api.scaleway.com/iot/v1beta1/regions/fr-par/hubs",
            str(scw.iot.hubs),
        )

    def test_api_name(self):
        scw = Scaleway(name="https://example.net/api")
        self.assertEqual(
            "https://example.net/api/rdb/v1/regions/fr-par/backups",
            str(scw.rdb.backups),
        )

    def test_version_and_region_only_added_once(self):
        scw = Scaleway()
        self.assertEqual(
            "https://api.scaleway.com/lbs/v1/regions/fr-par/lbs",
            str(scw.lbs.lbs),
        )
    
    def test_zone_arg(self):
        scw = Scaleway(zone="test-region-3")
        self.assertEqual(
            "https://api.scaleway.com/instance/v1/zones/test-region-3/servers",
            str(scw.instance.servers),
        )

    @patch("os.environ", {"SCW_DEFAULT_ZONE": "test-region-2"})
    def test_default_zone_environment_variable(self):
        scw = Scaleway()
        self.assertEqual(
            "https://api.scaleway.com/instance/v1/zones/test-region-2/servers",
            str(scw.instance.servers),
        )