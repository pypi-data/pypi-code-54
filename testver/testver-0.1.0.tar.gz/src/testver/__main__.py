import os
import argparse
import pathlib
from . import modver


parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument(
    "file", type=str, help="The file to read in and modify.",
)
parser.add_argument(
    "--suffix",
    "-s",
    metavar="suffix",
    type=str,
    help="The suffix to append. The default is to find this from git.",
)
parser.add_argument("--dryrun", action="store_true")


def _get_sha():
    return os.getenv("GITHUB_SHA") or os.getenv("TRAVIS_COMMIT") or "test"


if __name__ == "__main__":

    sha = _get_sha()

    args = parser.parse_args()
    filepath = pathlib.Path(args.file)

    suffix = args.suffix or sha

    files_to_try = sorted(
        [file_ for file_ in sorted(filepath.glob("**/__init__.py"))]
        + [file_ for file_ in sorted(filepath.glob("**/__version__.py"))]
    )

    if filepath.is_dir():
        for file_ in files_to_try:
            if "__version__" in file_.read_text():
                mod_text, new_ver = modver(file_, suffix=suffix)
                if not args.dryrun:
                    file_.write_text(mod_text)
                print(f"Changed __version__ in file {file_} to {new_ver}")
