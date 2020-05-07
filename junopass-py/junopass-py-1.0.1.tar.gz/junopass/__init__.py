from junopass import signatures
from junopass.client import *


class JunoPass(object):
    def __init__(self, access_token, junopass_public_key):
        self.access_token = access_token
        self.junopass_public_key = junopass_public_key

    def setup_device(self):
        """
        Generates device signing key
        Use this only on new devices e.g during setup/registration.
        Consider keeping the keys in a safe place for future use.
        Note the private_key must never be shared.

        Returns a tupple of key pair (private_key, public_key).

        Example:
        from junopass import JunoPass
        jp = JunoPass(<Access-Token>, <JunoPass-Public-Key>)
        private_key, public_key = jp.setup_device()
        """
        return signatures._generate_device_keys()

    def authenticate(self, payload):
        pass
