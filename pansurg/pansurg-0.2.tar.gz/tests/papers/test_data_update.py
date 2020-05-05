from unittest import main, TestCase
from unittest.mock import patch, MagicMock

from pansurg.papers.data_update import DataUpdate


class TestDataUpdate(TestCase):

    def test___init__(self):
        test = DataUpdate()

        self.assertEqual(str, type(test._url))
        self.assertEqual([], test.data)

    @patch("pansurg.papers.data_update.tarfile")
    @patch("pansurg.papers.data_update.urllib")
    def test_get_data(self, mock_urllib, mock_tarfile):
        mock_open = MagicMock()
        mock_extract_file_function = MagicMock()
        mock_open.__enter__ = mock_extract_file_function
        mock_tarfile.open.return_value = mock_open

        test = DataUpdate()
        test.get_data()


if __name__ == "__main__":
    main()
