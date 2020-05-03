"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject
from .rate_retrieval import RateRetrieval


class PaymentOrderResponse(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "address": {
                "rules": [
                    "regex:^",
                    "required"
                ],
                "type": "string"
            },
            "amount": {
                "rules": [
                    "required"
                ],
                "type": "integer"
            },
            "created_at": {
                "rules": [
                    "nullable"
                ],
                "type": "ISO_8601_date"
            },
            "expiration_time": {
                "rules": [
                    "required"
                ],
                "type": "ISO_8601_date"
            },
            "expires_in": {
                "rules": [
                    "required"
                ],
                "type": "integer"
            },
            "rate": {
                "rules": [
                    "required"
                ],
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
            },
            "redirect_url": {
                "rules": [
                    "regex[https_url]:^https://",
                    "required",
                    "nullable"
                ],
                "type": "url"
            },
            "reference": {
                "rules": [
                    "nullable"
                ],
                "type": "string"
            },
            "uri": {
                "rules": [
                    "regex:^",
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
        'rate': RateRetrieval,

    }

    def __init__(self, address, expires_in, uri, rate, amount, expiration_time, uuid, redirect_url=None, created_at=None, reference=None):
        super().__init__()
        self.address = address
        self.redirect_url = redirect_url
        self.expires_in = expires_in
        self.uri = uri
        self.rate = rate
        self.created_at = created_at
        self.amount = amount
        self.expiration_time = expiration_time
        self.uuid = uuid
        self.reference = reference
