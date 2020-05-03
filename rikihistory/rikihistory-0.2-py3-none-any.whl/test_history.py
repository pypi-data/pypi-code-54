from random import Random
from unittest import TestCase
from unittest import mock
from history import histurl, record_history

fakepage = mock.Mock()
fakepage.path = r'content\fakepageurl.md'
fakepage.url = 'fakepageurl'

random = Random()


class Test(TestCase):
    """
    This code generates content/history directory
    and content/history\fakepageurl_hist.md file in its parent directory.

    """
    def test_givenWikiPageURL_thenReturnHistWikiPageURL(self):
        test_url = histurl('wiki-page')
        answer = 'history/wiki-page_hist'
        self.assertEqual(test_url, answer)

    def test_givenRandUserName_whenHistoryRecordMade_thenUserNameInNewEntry(self):
        randuser = 'user' + str(random.randint(0, 1000))
        record_history(fakepage.path, 'action', randuser)
        with open('content/' + histurl(fakepage.url) + ".md", 'r', encoding='utf-8') as f:
            contents = f.read()
        f.close()
        self.assertIn(randuser, contents)

    def test_givenRandAction_whenAddingRecordToExistingHistoryFile_thenActionInNewEntry(self):
        randaction = 'action' + str(random.randint(0, 1000))
        record_history(fakepage.path, randaction, 'user')
        record_history(fakepage.path, randaction, 'user')
        with open('content/' + histurl(fakepage.url) + ".md", 'r', encoding='utf-8') as f:
            contents = f.read()
        f.close()
        self.assertIn(randaction, contents)

    def test_givenMockPage_whenHistoryRecordMade_thenHistFilePathReturned(self):
        testpath = record_history(fakepage.path, 'action', 'Claude')
        answer = r'content/history\fakepageurl_hist.md'
        self.assertEqual(testpath, answer)
