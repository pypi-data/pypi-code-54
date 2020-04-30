import os

from marshmallow import fields
from marshmallow_encrypted.crypto import decrypt, encrypt

SECRET_KEY_ENV_NAME = "MARSHMALLOW_ENCRYPTED_SECRET_KEY"


__all__ = ["EncryptedField"]


class EncryptedField(fields.Field):
    default_error_messages = {"invalid": "Invalid slug"}
    SLUG_REGEX = r"^[a-z0-9]+[a-z0-9\-]*$"

    def __init__(self, secret_key=None, *args, **kwargs):
        try:
            self._secret_key = secret_key or os.environ[SECRET_KEY_ENV_NAME]
        except KeyError:
            raise TypeError(
                f"No secret key found. Either provide `secret_key` when "
                f"instantiating {self.__class__.__name__} or set the "
                f"{SECRET_KEY_ENV_NAME} environment variable."
            )
        super().__init__(*args, **kwargs)

    def _validated(self, value):
        if not isinstance(value, str):
            self.fail("invalid")
        return value

    def _serialize(self, value, attr, obj):
        encrypted_value = encrypt(value.encode(), secret_key=self._secret_key)
        encrypted_dict = dict(
            zip(("ciphertext", "tag", "nonce"), encrypted_value)
        )
        return super()._serialize(encrypted_dict, attr, obj)

    def _deserialize(self, value, attr, data, partial):
        return decrypt(**value, secret_key=self._secret_key).decode()
