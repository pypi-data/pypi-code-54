"""
Nigiri auto-generated file
"""
from sdkboil.object import SdkObject
from .out import Out


class Transaction(SdkObject):
    schema = {
        "rules": [],
        "schema": {
            "blockchain_status": {
                "rules": [
                    "required",
                    "in:mempool,unconfirmed,confirmed,reverted"
                ],
                "type": "string"
            },
            "created_at": {
                "rules": [
                    "required"
                ],
                "type": "ISO_8601_date"
            },
            "normalized_txid": {
                "rules": [
                    "len:64",
                    "required"
                ],
                "type": "string"
            },
            "outs": {
                "elements": {
                    "rules": [],
                    "schema": {
                        "amount": {
                            "rules": [
                                "required"
                            ],
                            "type": "integer"
                        },
                        "n": {
                            "rules": [
                                "required"
                            ],
                            "type": "integer"
                        }
                    },
                    "type": "object"
                },
                "rules": [
                    "required"
                ],
                "type": "array"
            },
            "outs_sum": {
                "rules": [
                    "required"
                ],
                "type": "integer"
            },
            "status": {
                "rules": [
                    "required",
                    "in:unconfirmed,confirmed,reverted"
                ],
                "type": "string"
            },
            "txid": {
                "rules": [
                    "len:64",
                    "required"
                ],
                "type": "string"
            }
        },
        "type": "object"
    }
    sub_objects = {
        'outs': [Out],

    }

    def __init__(self, outs_sum, status, txid, created_at, outs, blockchain_status, normalized_txid):
        super().__init__()
        self.outs_sum = outs_sum
        self.status = status
        self.txid = txid
        self.created_at = created_at
        self.outs = outs
        self.blockchain_status = blockchain_status
        self.normalized_txid = normalized_txid
