import argparse
from truckman.save import save_volume
from truckman.load import load_volume


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Save and load Docker named volumes.")
    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument(
       "--save",
       type=str,
       action="store",
       help="Save a volume as a tar archive.")
    command_group.add_argument(
       "--load",
       type=str,
       action="store",
       help="Path of tar archive to load volume from."
    )
    parser.add_argument(
      "--name",
      type=str,
      action="store",
      help="Name of the volume to load the tar archive to."
    )
    args = parser.parse_args()

    if args.save:
        save_volume(args.save)
    if args.load and not args.name:
        parser.error("You must specify the name of the volume to be created!")
    elif not args.load and args.name:
        parser.error(
           "You must specify the path to the tar file to load the volume from!"
        )
    elif args.load and args.name:
        load_volume(volume_path=args.load, volume_name=args.name)
    else:
        parser.print_help()
