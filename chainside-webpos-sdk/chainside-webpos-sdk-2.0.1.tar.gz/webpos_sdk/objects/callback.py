"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject


class Callback(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "name": {
                "rules": [
                    "required"
                ],
                "type": "string"
            }
        },
        "type": "object"
    }
    sub_objects = {

    }

    def __init__(self, name):
        super().__init__()
        self.name = name
