import os
from hammock import Hammock


class Scaleway(Hammock):
    """Thin wrapper around the Scaleway API"""

    REGIONS = ["fr-par", "nl-ams"]
    APIS = [
        "baremetal",
        "instance",
        "iot",
        "k8s",
        "lbs",
        "rdb",
        "registry",
    ]

    def __init__(self, region=None, token=None, version=None, zone=None, **kwargs):
        """Constructor takes optional region and access token"""

        self._headers = {
            "X-Auth-Token": token if token else os.environ.get("SCW_SECRET_KEY")
        }
        self._headers.update(kwargs["headers"] if "headers" in kwargs else {})

        super().__init__(**kwargs)
        self._name = kwargs["name"] if "name" in kwargs else "https://api.scaleway.com"
        self._region = (
            region if region else os.environ.get("SCW_DEFAULT_REGION", self.REGIONS[0])
        )
        self._zone = (
            zone if zone else os.environ.get("SCW_DEFAULT_ZONE", f"{self._region}-1")
        )
        self._version = version if version else os.environ.get("SCW_API_VERSION", "v1")

    def _request(self, method, *args, **kwargs):
        """
        Makes the HTTP request using requests module
        """
        if not "headers" in kwargs:
            kwargs["headers"] = self._headers
        return self._session.request(method, self._url(*args), **kwargs)

    def __getattr__(self, name):
        if name in self.APIS and name not in [n._name for n in self]:
            return getattr(self, f"_{name}")()
        return super().__getattr__(name)

    @property
    def _iot(self):
        return self._spawn("iot").v1beta1.regions(self._region)

    @property
    def _lbs(self):
        return self._spawn("lbs")._spawn(self._version).regions(self._region)

    @property
    def _k8s(self):
        return self._spawn("k8s")._spawn(self._version).regions(self._region)

    @property
    def _rdb(self):
        return self._spawn("rdb")._spawn(self._version).regions(self._region)

    @property
    def _registry(self):
        return self._spawn("registry")._spawn(self._version).regions(self._region)

    @property
    def _instance(self):
        return self._spawn("instance")._spawn(self._version).zones(self._zone)

    @property
    def _baremetal(self):
        return self._spawn("baremetal")._spawn(self._version).zones(self._zone)
