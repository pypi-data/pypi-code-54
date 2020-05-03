"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject


class PaymentOrder(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "amount": {
                "rules": [
                    "required",
                    "decimal"
                ],
                "type": "string"
            },
            "callback_url": {
                "rules": [
                    "regex[https_url]:^https://",
                    "nullable",
                    "maxlen:300"
                ],
                "type": "url"
            },
            "cancel_url": {
                "rules": [
                    "regex[https_url]:^https://",
                    "nullable",
                    "maxlen:300"
                ],
                "type": "url"
            },
            "continue_url": {
                "rules": [
                    "regex[https_url]:^https://",
                    "nullable",
                    "maxlen:300"
                ],
                "type": "url"
            },
            "details": {
                "rules": [
                    "maxlen:300",
                    "nullable"
                ],
                "type": "string"
            },
            "reference": {
                "rules": [
                    "maxlen:300",
                    "nullable"
                ],
                "type": "string"
            },
            "required_confirmations": {
                "rules": [
                    "min:0",
                    "nullable"
                ],
                "type": "integer"
            }
        },
        "type": "object"
    }
    sub_objects = {

    }

    def __init__(self, amount, details=None, reference=None, cancel_url=None, callback_url=None, required_confirmations=None, continue_url=None):
        super().__init__()
        self.details = details
        self.reference = reference
        self.cancel_url = cancel_url
        self.callback_url = callback_url
        self.required_confirmations = required_confirmations
        self.amount = amount
        self.continue_url = continue_url
