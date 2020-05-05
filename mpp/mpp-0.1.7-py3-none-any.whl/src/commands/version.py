import sys

from mpp.src.utils import config_file


def version(args=None):
    """
    Fast increment the version number

    Args:
        args (argparse args): parameters from parser.parse_args()
    """

    # Get project config file
    mpp_config = config_file.read()

    # Show current project version
    if args.add is None:
        print(mpp_config["name"], mpp_config["version"])
        sys.exit()

    # Verify arguments
    if set(args.add) != {"+"}:
        print(f"Wrong argument: got '{args.add}' but expected N '+'")
        sys.exit()

    ver = [int(v) for v in mpp_config["version"].split(".")]
    index = args.add.count("+")
    if index > len(ver):
        print(f"Too many '+': got {index} but maximum expected is {len(ver)}")
        sys.exit()

    # Increase version number
    ver[-index] += 1
    # Set lower version numbers to 0
    for i in range(-index + 1, 0):
        ver[i] = 0

    # Write config
    ver = ".".join([str(v) for v in ver])
    mpp_config["version"] = ver
    config_file.write(mpp_config)
    print(mpp_config["name"], ver)
