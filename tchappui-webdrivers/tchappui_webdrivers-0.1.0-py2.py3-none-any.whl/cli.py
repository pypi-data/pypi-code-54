"""Console script for install_webdrivers."""
import sys
import click

from . import webdrivers as wd


@click.command()
def main(args=None):
    """Console script for install_webdrivers."""
    wd.install_latest_chromedriver()
    wd.install_latest_geckdriver()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
