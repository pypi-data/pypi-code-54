import unittest
from vetmanager.url.protocol import HTTPS
from vetmanager.url.host import FakeHost
from vetmanager.domain import Url


class TestDomain(unittest.TestCase):

    def test_url(self):
        self.assertEqual(str(Url(HTTPS(), FakeHost())), 'https://host')


if __name__ == '__main__':
    unittest.main()
