import unittest
from vetmanager.functions import url
from vetmanager.domain import UrlInterface
from interface import implements


class TestFunctions(unittest.TestCase):

    def test_url(self):
        urlObject = url('test')
        self.assertTrue(isinstance(urlObject, implements(UrlInterface)))


if __name__ == '__main__':
    unittest.main()
