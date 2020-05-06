import unittest

from ftests.cli_args import CliArgs


class CliArgsTest(unittest.TestCase):

    def test_get_file_full_path_with_trailing_slash(self):
        args = CliArgs(directory='directory/with/trailing/slash/', file='.ftests.yml')
        self.assertEqual('directory/with/trailing/slash/.ftests.yml',
                         args.get_file_full_path(),
                         'Directory and file should be concatenated without adding another slash in-between')

    def test_get_file_full_path_without_trailing_slash(self):
        args = CliArgs(directory='directory/without/trailing/slash', file='.ftests.yml')
        self.assertEqual('directory/without/trailing/slash/.ftests.yml',
                         args.get_file_full_path(),
                         'Directory and file should be concatenated with a slash in-between')


if __name__ == '__main__':
    unittest.main()
