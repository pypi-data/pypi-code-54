"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject


class PaymentUpdateObject(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "callback": {
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

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
