from unittest import main, TestCase
from unittest.mock import patch

from pansurg.papers.papers import Papers


class TestPapers(TestCase):

    @patch("pansurg.papers.papers.Papers._get_data")
    def test___init__(self, mock_get_data):
        test = Papers()
        self.assertEqual([], test)

    @patch("pansurg.papers.papers.DataUpdate")
    @patch("pansurg.papers.papers.Papers.__init__")
    def test__get_data(self, mock_init, mock_update):
        mock_init.return_value = None
        test = Papers()
        test._get_data()

        mock_update.assert_called_once_with()
        mock_update.return_value.get_data.assert_called_once_with()


if __name__ == "__main__":
    main()
