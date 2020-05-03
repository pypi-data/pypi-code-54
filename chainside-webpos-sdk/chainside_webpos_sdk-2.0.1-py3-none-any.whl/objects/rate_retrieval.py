"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject


class RateRetrieval(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "created_at": {
                "rules": [
                    "required"
                ],
                "type": "ISO_8601_date"
            },
            "from": {
                "rules": [],
                "type": "string"
            },
            "source": {
                "rules": [
                    "required"
                ],
                "type": "string"
            },
            "to": {
                "rules": [],
                "type": "string"
            },
            "value": {
                "rules": [
                    "decimal",
                    "required"
                ],
                "type": "string"
            }
        },
        "type": "object"
    }
    sub_objects = {

    }

    def __init__(self, created_at, value, source, to=None, from_=None):
        super().__init__()
        self.created_at = created_at
        self.value = value
        self.to = to
        self.from_ = from_
        self.source = source
