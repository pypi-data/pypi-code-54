from applauncher.kernel import ConfigurationReadyEvent
from pymongo import MongoClient


class MongoDbBundle(object):
    def __init__(self):
        self.config_mapping = {
            "mongodb": {
                "uri": None,
                "connect": True
            }
        }

        self.event_listeners = [
            (ConfigurationReadyEvent, self.configuration_ready),
        ]

        self.injection_bindings = {}

    def configuration_ready(self, event):
        config = event.configuration.mongodb
        self.injection_bindings[MongoClient] = MongoClient(host=config.uri, connect=config.connect)

