import argparse
import os


class CliArgs:
    directory: str
    file: str

    def __init__(self,
                 directory: str,
                 file: str,
                 ):
        self.directory = directory
        self.file = file

    @staticmethod
    def get_cli_args():
        parser = argparse.ArgumentParser(prog='ftests')
        parser.add_argument('directory',
                            nargs='?',
                            default=os.getcwd(),
                            help='the directory in which to run the tests (default to current directory)',
                            )
        parser.add_argument('-f', '--file',
                            default='.ftests.yml',
                            help='name of the tests definition file (default to .ftests.yml)',
                            )
        args = parser.parse_args()
        cli_args = CliArgs(
            directory=args.directory,
            file=args.file,
        )
        return cli_args

    def get_file_full_path(self) -> str:
        return f'{self.directory}{"" if self.directory.endswith("/") else "/"}{self.file}'
