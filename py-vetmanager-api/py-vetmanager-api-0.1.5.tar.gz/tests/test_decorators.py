import unittest
from vetmanager.decorators import only_once


class FakeForTest:
    i = 0

    @only_once
    def incremented_text(self):
        self.i = self.i + 1
        return 'test' + str(self.i)


class TestFunctions(unittest.TestCase):

    def test_only_once(self):
        fake = FakeForTest()
        self.assertEqual(fake.incremented_text(), 'test1')
        self.assertEqual(fake.incremented_text(), 'test1')


if __name__ == '__main__':
    unittest.main()
