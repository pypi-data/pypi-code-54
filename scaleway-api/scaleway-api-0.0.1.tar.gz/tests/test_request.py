"""Test that our URLs match expectations"""
from unittest import TestCase
from unittest.mock import patch
from scaleway_api import Scaleway
import responses


class RequestTests(TestCase):
    """Test that the URLs for the API match expectations"""

    @responses.activate
    def test_token_arg(self):
        scw = Scaleway(name="https://example.net", token="this-is-a-test-key")

        responses.add(
            responses.GET,
            "https://example.net/k8s/v1/regions/fr-par/clusters",
            json={},
            status=200,
        )
        resp = scw.k8s.clusters.GET()

        self.assertIn("X-Auth-Token", resp.request.headers)
        self.assertEqual(resp.request.headers["X-Auth-Token"], "this-is-a-test-key")

    @responses.activate
    @patch("os.environ", {"SCW_SECRET_KEY": "this-is-a-test-key"})
    def test_secret_environment_variable(self):
        scw = Scaleway(name="https://example.net")

        responses.add(
            responses.GET,
            "https://example.net/registry/v1/regions/fr-par/images",
            json={},
            status=200,
        )
        resp = scw.registry.images.GET()

        self.assertIn("X-Auth-Token", resp.request.headers)
        self.assertEqual(resp.request.headers["X-Auth-Token"], "this-is-a-test-key")
