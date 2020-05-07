import argparse
import pathlib
import re
import typing
import tarfile
import fnmatch


class FilePattern:
    def __init__(self, name: str):
        self.__from_top = name.startswith('/')
        name = name.lstrip('/')
        self.__only = name
        self.__last = '**/' + name
        self.__middle = '**/' + name + '/**'
        self.__first = name + '/**'

    def match(self, file_name_from_top: pathlib.Path):
        file = str(file_name_from_top)
        if fnmatch.fnmatch(file, self.__only) or fnmatch.fnmatch(file, self.__first):
            return True

        if self.__from_top:
            return False

        return fnmatch.fnmatch(file, self.__last) or fnmatch.fnmatch(file, self.__middle)


class IgnoreManager:
    def __init__(self, ignore_file: typing.Optional[pathlib.Path] = None):
        self.__exclude_pattern = []
        self.__include_pattern = []

        space_only_regex = re.compile(r'(\s*|^#)')

        if ignore_file is None:
            return

        with ignore_file.open() as fp:
            for line in fp:
                line = line.rstrip()
                if space_only_regex.fullmatch(line) is not None:
                    continue

                if line.startswith('!'):
                    line = line[1:]
                    self.__include_pattern.append(FilePattern(line))
                else:
                    self.__exclude_pattern.append(FilePattern(line))

    def has(self, file_name_from_top: pathlib.Path):
        for inc in self.__include_pattern:
            if inc.match(file_name_from_top):
                return False

        for exc in self.__exclude_pattern:
            if exc.match(file_name_from_top):
                return True
        return False


def __enumerate_files(directory: pathlib.Path):
    ignore = directory / '.packignore'
    if ignore.exists():
        ignore = IgnoreManager(ignore)
    else:
        ignore = IgnoreManager()

    return (
        f
        for f in directory.rglob('*')
        if not ignore.has(f)
    )


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--version', '-V', action='store_true', help='show program version')
    parser.add_argument('--verbose', '-v', action='store_true', help='print verbose log')
    parser.add_argument(
        '--format', '-f',
        choices=('auto', 'gz', 'xz', 'bz2', 'none'),
        help='compress format\n'
             ' * auto:  auto detect from file name\n'
             '   gz:  tar.gz format\n'
             '   xz:    tar.xz format\n'
             '   bz2: tar.bz2 format\n'
             '   none:  no compress raw tar format',
        default='auto'
    )
    parser.add_argument('directory', nargs='?', default=str(pathlib.Path.cwd()), help='input directory')
    parser.add_argument('--output', '-o', help='output file name', required=True)

    args = parser.parse_args()

    open_mode = {
        'auto': None,
        'gzip': 'gz',
        'xz': 'xz',
        'bzip2': 'bz2',
        'none': '',
    }[args.format]

    output = args.output
    if open_mode is None:
        if output.endswith('.gz'):
            open_mode = 'gz'
        elif output.endswith('xz'):
            open_mode = 'xz'
        elif output.endswith('bz2'):
            open_mode = 'bz2'
        else:
            open_mode = ''

    with tarfile.open(output, 'w:{}'.format(open_mode)) as tfp:
        cwd = pathlib.Path(args.directory)
        for file in __enumerate_files(cwd):
            try:
                file = file.relative_to(cwd)
            except ValueError:
                pass
            if args.verbose:
                print(file)
            tfp.add(str(file), recursive=False)


if __name__ == '__main__':
    main()
