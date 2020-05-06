#     Copyright 2020. ThingsBoard
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from simplejson import dumps
from thingsboard_gateway.connectors.mqtt.mqtt_uplink_converter import MqttUplinkConverter, log


from thingsboard_gateway.connectors.mqtt.mqtt_uplink_converter import MqttUplinkConverter, log

class CustomMqttUplinkConverter(MqttUplinkConverter):
    def __init__(self, config):
        self.__config = config.get('converter')
        self.dict_result = {}

    def convert(self, topic, body):
        try:
            log.debug("New data received: %s: %s" % (topic,body))
            # if topic = '/devices/buzzer/controls/volume' device name will be 'buzzer'.
            self.dict_result["deviceName"] = topic.split("/")[2]
            # just hardcode this
            self.dict_result["deviceType"] = "buzzer"
            self.dict_result["telemetry"] = {"data": body}
            log.debug("Result: %s" % (self.dict_result))
            return self.dict_result
        except Exception as e:
            log.exception(e)