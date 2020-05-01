import unittest

from unittest.mock import Mock

from d64.dos_path import DOSPath
from d64.exceptions import DiskFullError

from test.mock_block import MockBlock


class TestDOSPath(unittest.TestCase):

    def test_open_read_exists(self):
        mock_entry = Mock()
        mock_entry.start_ts = (None, None)
        path = DOSPath(None, entry=mock_entry)
        with path.open('r') as file_:
            self.assertIsNotNone(file_)

    def test_open_read_not_exists(self):
        path = DOSPath(None, name='x')
        with self.assertRaises(FileNotFoundError):
            with path.open('r') as _:
                pass

    def test_open_write_exists(self):
        mock_image = Mock()
        mock_image.writeable = True
        first_block = MockBlock()
        mock_entry = Mock()
        mock_entry.first_block.return_value = first_block
        path = DOSPath(mock_image, entry=mock_entry)
        with path.open('w') as file_:
            self.assertIsNotNone(file_)
            self.assertEqual(file_.entry.size, 1)
        self.assertEqual(first_block.data_size, 0)
        mock_image.bam.set_free.assert_not_called()

    def test_open_write_exists_2block(self):
        mock_image = Mock()
        mock_image.writeable = True
        second_block = MockBlock()
        first_block = MockBlock()
        first_block.set_next_block(second_block)
        mock_entry = Mock()
        mock_entry.first_block.return_value = first_block
        path = DOSPath(mock_image, entry=mock_entry)
        with path.open('w') as file_:
            self.assertIsNotNone(file_)
            self.assertEqual(file_.entry.size, 1)
        self.assertEqual(first_block.data_size, 0)
        self.assertIsNone(first_block.next_block())
        mock_image.bam.set_free.assert_called_once()

    def test_open_write_not_exists(self):
        mock_image = Mock()
        mock_image.writeable = True
        mock_image.get_free_entry.return_value = Mock()
        path = DOSPath(mock_image, name='x')
        with path.open('w', 'seq') as file_:
            self.assertIsNotNone(file_)
            self.assertEqual(file_.entry.file_type, 'seq')
            self.assertEqual(file_.entry.name, 'x')
            self.assertEqual(file_.entry.size, 1)

    def test_open_write_not_exists_full(self):
        mock_image = Mock()
        mock_image.writeable = True
        mock_image.get_free_entry.return_value = None
        path = DOSPath(mock_image, name='x')
        with self.assertRaises(DiskFullError):
            with path.open('w', 'seq') as _:
                pass

    def test_open_read_only(self):
        mock_image = Mock()
        mock_image.writeable = False
        path = DOSPath(mock_image, name='x')
        with self.assertRaises(PermissionError):
            with path.open('w') as _:
                pass

    def test_open_invalid_mode(self):
        path = DOSPath(None, name='x')
        with self.assertRaises(ValueError):
            with path.open('q') as _:
                pass

    def test_open_missing_type(self):
        mock_image = Mock
        mock_image.writeable = True
        path = DOSPath(mock_image, name='x')
        with self.assertRaises(ValueError):
            with path.open('w') as _:
                pass


if __name__ == '__main__':
    unittest.main()
