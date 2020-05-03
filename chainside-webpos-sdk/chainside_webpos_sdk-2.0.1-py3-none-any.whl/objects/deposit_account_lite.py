"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject


class DepositAccountLite(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "name": {
                "rules": [
                    "required"
                ],
                "type": "string"
            },
            "type": {
                "rules": [
                    "in:bank,bitcoin",
                    "required"
                ],
                "type": "string"
            },
            "uuid": {
                "rules": [
                    "required"
                ],
                "type": "uuid"
            }
        },
        "type": "object"
    }
    sub_objects = {

    }

    def __init__(self, type, uuid, name):
        super().__init__()
        self.type = type
        self.uuid = uuid
        self.name = name
