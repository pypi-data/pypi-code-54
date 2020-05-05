from unittest import main, TestCase
from unittest.mock import patch, PropertyMock

from pansurg.papers.papers import Papers


class TestPapers(TestCase):

    @patch("pansurg.papers.papers.Papers._load")
    @patch("pansurg.papers.papers.Papers._save")
    @patch('pansurg.papers.papers.Papers.cache_exists', new_callable=PropertyMock)
    @patch("pansurg.papers.papers.Papers._get_data")
    def test___init__(self, mock_get_data, mock_cache_exists, mock__save, mock__load):
        mock_cache_exists.return_value = True
        test = Papers()

        self.assertEqual([], test)
        mock__load.assert_called_once_with()

        mock_cache_exists.return_value = False
        test = Papers()

        self.assertEqual([], test)
        mock__load.assert_called_once_with()
        mock_get_data.assert_called_once_with()
        mock__save.assert_called_once_with()

        mock_get_data.reset_mock()
        mock__save.reset_mock()

        test = Papers(force_refresh=True)
        self.assertEqual([], test)
        mock__load.assert_called_once_with()
        mock_get_data.assert_called_once_with()
        mock__save.assert_called_once_with()

    @patch("pansurg.papers.papers.DataUpdate")
    @patch("pansurg.papers.papers.Papers.__init__")
    def test__get_data(self, mock_init, mock_update):
        mock_init.return_value = None
        test = Papers()
        test._get_data()

        mock_update.assert_called_once_with()
        mock_update.return_value.get_data.assert_called_once_with()

    @patch("pansurg.papers.papers.pickle")
    @patch("pansurg.papers.papers.open")
    @patch("pansurg.papers.papers.Papers.__init__")
    def test__save(self, mock_init, mock_open, mock_pickle):
        mock_init.return_value = None
        test = Papers()

        test._save()
        mock_pickle.dump.assert_called_once_with(test, mock_open.return_value.__enter__.return_value)

    @patch("pansurg.papers.papers.pickle")
    @patch("pansurg.papers.papers.open")
    @patch("pansurg.papers.papers.Papers.__init__")
    def test__load(self, mock_init, mock_open, mock_pickle):
        mock_init.return_value = None
        test = Papers()
        mock_pickle.load.return_value = ["one", "two", "three"]

        test._load()
        mock_pickle.load.assert_called_once_with(mock_open.return_value.__enter__.return_value)

        self.assertEqual(["one", "two", "three"], test)


if __name__ == "__main__":
    main()
