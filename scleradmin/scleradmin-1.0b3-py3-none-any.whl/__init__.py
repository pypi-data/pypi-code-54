import sys
import os
import argparse

from . import install

def main():
    """Parse arguments and call the installer"""

    parser = argparse.ArgumentParser(
        description = "Sclera Platform Administration",
        epilog = "In --add and --remove above, 'plugin' has the format 'org:name:version', where 'org:' and ':version' are optional. When not specified, 'org' defaults to 'com.scleradb' and 'version' defaults to the latest installable version. Sclera requires Java 13 or higher."
    )

    parser.add_argument(
        "--install", action = "store_true",
        help = "install Sclera in the root directory"
    )

    parser.add_argument(
        "--add", metavar = "plugin", type = str, nargs = "+",
        help = "add plugins"
    )

    parser.add_argument(
        "--remove", metavar = "plugin", type = str, nargs = "+",
        help = "remove plugins"
    )

    parser.add_argument(
        "--update", action = "store_true",
        help = "update Sclera and installed plugins to the latest version"
    )

    parser.add_argument(
        "--root", metavar = "rootdir", type = str, nargs = 1,
        default = [os.getenv("SCLERA_ROOT", os.path.expanduser("~/sclera"))],
        help = "root directory location (if not specified, will use $SCLERA_ROOT if present, otherwise ~/sclera)"
    )

    parser.add_argument(
        "--overwrite", action = "store_true",
        help = "overwrite root directory if present"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    try:
        install.run(args)
    except ConnectionError:
        sys.exit("Could not connect to the internet. Exiting.")
    except Exception as e:
        sys.exit(e)
