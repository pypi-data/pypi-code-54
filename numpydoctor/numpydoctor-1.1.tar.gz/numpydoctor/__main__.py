""" CLI entrypoint for numpydoctor """

import argparse
import sys
from numpydoctor import application, __version__
from numpydoctor.docstring_tools import TODO_REQUIRED

_DESCRIPTION = "Completion, correction, and checking of numpydoc-style docstrings in Python."
_DEFAULT_LINE_WRAP_COL = None
_DEFAULT_TAB_LEN = 4
_DEFAULT_TODO_LEVEL = TODO_REQUIRED


def check_entrypoint(args: argparse.Namespace) -> None:
    if args.missing:
        code = application.check_missing(args.path, offset=args.offset,
                                         nested=args.nested, private=args.private,
                                         magic=args.magic)
    else:
        code = application.check(args.path, offset=args.offset,
                                 nested=args.nested, private=args.private,
                                 magic=args.magic)
        sys.exit(code)


def fix_entrypoint(args: argparse.Namespace) -> None:
    args.todo = _DEFAULT_TODO_LEVEL if args.todo is None else args.todo
    if args.missing:
        application.fill_missing(
            args.path, offset=args.offset, nested=args.nested,
            private=args.private, magic=args.magic,
            inplace=args.inplace, line_wrap_col=args.line_wrap_col,
            tab_len=args.indent_size, todo_level=args.todo
        )
    else:
        application.fix(
            args.path, offset=args.offset, nested=args.nested,
            private=args.private, magic=args.magic,
            inplace=args.inplace, line_wrap_col=args.line_wrap_col,
            tab_len=args.indent_size, todo_level=args.todo
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=_DESCRIPTION)
    subparse = parser.add_subparsers(help='action subcommands', required=False)
    parser.add_argument("-V", "--version", action='store_true', help="show package version")
    parser.add_argument("-N", "--nested", action='store_true',
                        help="include functions & classes nested in other functions")
    parser.add_argument("-p", "--private", action='store_true', help="include private names")
    parser.add_argument("-m", "--magic", action='store_true', help="include magic names")
    parser.add_argument("-a", "--all", action='store_true', help="include all names (equivalent to -pm)")
    parser.set_defaults(entrypoint=None)

    files = argparse.ArgumentParser(add_help=False)
    files.add_argument("path", nargs='?', help="path to python module source file")
    files.add_argument("-o", "--offset", type=int, help="""
cursor byte offset in `file` of scope to check, optional.
If omitted, will check all docstrings.
    """.strip())

    check_parser = subparse.add_parser('check', help="check docstring information.", description="""
Check docstring information. Find module, class, function, and
coroutine definitions in source code whose docstrings contain
incorrect or outdated information, or are missing docstrings entirely.
    """.strip(), parents=[files])
    check_parser.set_defaults(entrypoint=check_entrypoint)
    check_parser.add_argument("-M", "--missing", action='store_true',
                              help="only check for missing docstrings")

    fix_parser = subparse.add_parser('fix', help="fix docstring information.", description="""
Fix docstring information. Gather information about modules,
functions, classes, and coroutines through static analysis and modify
docstrings, inserting missing information and correcting out-of-date
documentation.
    """.strip(), parents=[files])
    fix_parser.set_defaults(entrypoint=fix_entrypoint)
    fix_parser.add_argument("-M", "--missing", action='store_true',
                            help="only add missing docstrings, do not fix existing docstrings")
    fix_parser.add_argument("-i", "--inplace", action='store_true',
                            help="modify the file in-place (default: write to stdout)")
    fix_parser.add_argument("-L", "--line-wrap-col", type=int, default=_DEFAULT_LINE_WRAP_COL,
                            help=f"line wrap column for docstrings (default: {_DEFAULT_LINE_WRAP_COL})")
    fix_parser.add_argument("-I", "--indent-size", type=int, default=_DEFAULT_TAB_LEN,
                            help=f"size of indentation in spaces (default: {_DEFAULT_TAB_LEN})")
    fix_parser.add_argument("-T", "--todo", action='count',
                            help="""
control where TODO messages are inserted for missing docstring data.
Repeating this argument will make it more pedantic.  By default, TODO
messages will be inserted where required data is missing -- parameter
names, return types. Each additional level will insert TODOs for
missing types, descriptions, return names, and extended summaries.
    """.strip())

    args = parser.parse_args()
    if args.version:
        print(f"{__package__} {__version__}")
    elif args.entrypoint is None:
        parser.print_usage()
    else:
        args.entrypoint(args)


if __name__ == '__main__':
    main()
