"""Gateway connecting to ATAG thermostat."""
import aiohttp
import logging
import datetime
import re, uuid
import asyncio
import logging
from .errors import raise_error
from .entities import Report, Climate, DHW

_LOGGER = logging.getLogger(__name__)


class AtagOne:
    """Central data store entity."""

    def __init__(self, host, session=None, *, device=None, email=None, port=10000):

        self.host = host
        self.email = email or ""
        self.port = port
        if email is None:
            _LOGGER.info("Running without Mail may lead to authorization issues.")
        self.session = session or aiohttp.ClientSession()
        self._device = device
        self._authorized = device is not None
        self._mac = ":".join(re.findall("..", "%012x" % uuid.getnode()))
        self._last_call = datetime.datetime(1970, 1, 1)
        self._lock = asyncio.Lock()

        self.climate = None
        self.dhw = None
        self.report = None

    @property
    def id(self):
        """Return the ID of the bridge."""
        if self.report:
            return self.report["device_id"].state
        return self._device

    @property
    def apiversion(self):
        """Return the ID of the bridge."""
        if self.report:
            return self.report["download_url"].state

    async def authorize(self):
        """Check auth status."""
        json = {
            "pair_message": {
                "seqnr": 1,
                "account_auth": {"user_account": self.email, "mac_address": self._mac},
                "accounts": {
                    "entries": [
                        {
                            "user_account": self.email,
                            "mac_address": self._mac,
                            "device_name": "HomeAssistant",
                            "account_type": 1,
                        }
                    ]
                },
            }
        }
        await self.request("post", "pair", json)
        self.authorized = True
        _LOGGER.debug(f"Authorized: {self.authorized}")
        return self.authorized

    async def request(self, method, path, json=None):
        """Make a request to the API."""
        url = f"http://{self.host}:{self.port}/{path}"
        async with self._lock:
            slept = (datetime.datetime.utcnow() - self._last_call).total_seconds()
            if slept < 5:
                await asyncio.sleep(5 - slept)
            self._last_call = datetime.datetime.utcnow()
            try:
                async with self.session.request(method, url, json=json) as res:
                    data = await res.json()
                    _raise_on_error(data)
                    return data
            except aiohttp.ClientConnectorError as err:
                raise_error(err, 2)
            except Exception as err:
                raise_error(err, 5)

    async def update(self, info=71, force=False):
        """Get latest data from API"""
        if (datetime.datetime.utcnow() - self._last_call).total_seconds() > 15 or force:
            json = {
                "retrieve_message": {
                    "seqnr": 1,
                    "account_auth": {
                        "user_account": self.email,
                        "mac_address": self._mac,
                    },
                    "info": info,
                }
            }
            res = await self.request("get", "retrieve", json)
            res = res["retrieve_reply"]
            res["report"].update(res["report"].pop("details"))
            if self.report is None:
                self.report = Report(res, self.update, self.setter)
                self.climate = Climate(self.report)
                self.dhw = DHW(self.report)
            self.report.update(res)
            return self.report
        return None

    async def setter(self, **kwargs):
        """Set control items."""
        json = {
            "update_message": {
                "seqnr": 1,
                "account_auth": {"user_account": self.email, "mac_address": self._mac},
                "control": {},
                "configuration": {},
            }
        }

        for key, val in kwargs.items():
            json["update_message"]["control"][key] = val
            if key == "ch_mode" and val == 3:
                json["update_message"]["control"]["vacation_duration"] = int(
                    datetime.timedelta(days=1).total_seconds()
                )
                json["update_message"]["configuration"]["start_vacation"] = int(
                    (
                        datetime.datetime.utcnow() - datetime.datetime(2000, 1, 1)
                    ).total_seconds()
                )
        res = await self.request("post", "update", json)
        return res["update_reply"]


def _raise_on_error(data):
    """Check response for error message."""
    if data[list(data.keys())[0]]["acc_status"] != 2:
        raise_error(data, 1)

    if isinstance(data, list):
        data = data[0]

    if isinstance(data, dict) and "error" in data:
        raise_error(data)
