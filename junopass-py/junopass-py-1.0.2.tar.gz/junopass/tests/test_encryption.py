import unittest

from junopass import JunoPass


class TestEncryption(unittest.TestCase):

    def setUp(self):
        access_token = "xx"
        junopass_public_key = "yy"
        self.jp = JunoPass(access_token, junopass_public_key)

    def test_device_setup(self):
        prvtkey, pubkey = self.jp.setup_device()
        self.assertIsNotNone(prvtkey)
        self.assertIsNotNone(pubkey)
        self.assertNotEqual(prvtkey, pubkey)
