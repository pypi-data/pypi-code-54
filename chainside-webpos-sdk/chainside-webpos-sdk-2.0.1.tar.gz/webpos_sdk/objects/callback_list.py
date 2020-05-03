"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject
from .callback import Callback


class CallbackList(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "callbacks": {
                "elements": {
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
                },
                "rules": [
                    "required"
                ],
                "type": "array"
            }
        },
        "type": "object"
    }
    sub_objects = {
        'callbacks': [Callback],

    }

    def __init__(self, callbacks):
        super().__init__()
        self.callbacks = callbacks
