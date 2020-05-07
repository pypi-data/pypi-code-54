"""
Usage:
    something --help
    something --version
    something name [--first | --last | --full]

Options:
  -h --help        Show this info.
  -v --version     Show version.
  name <type>      Name type [default:  --full].
"""

from docopt import docopt
from geta import name
from geta.version import __version__


def main(args=docopt(__doc__)):
    if args["--version"]:
        print("version", __version__)
        return

    if args["name"]:
        if args["--first"]:
            print(name.first_name())
        elif args["--last"]:
            print(name.last_name())
        else:
            print(name.full_name())


if __name__ == "__main__":
    main()
