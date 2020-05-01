from influxdb_client import InfluxDBClient
from applauncher.kernel import ConfigurationReadyEvent


class InfluxDbBundle(object):
    def __init__(self):
        self.config_mapping = {
            "influxdb": {
                "url": None,
                "org": None,
                "token": None
            }
        }

        self.event_listeners = [
            (ConfigurationReadyEvent, self.configuration_ready)
        ]

        self.injection_bindings = {}

    def configuration_ready(self, event):
        config = event.configuration.influxdb
        self.injection_bindings[InfluxDBClient] = InfluxDBClient(
            url=config.url,
            token=config.token,
            org=config.org
        )

