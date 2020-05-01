"""Console script for install_webdrivers."""
import os
import sys
import click

from . import webdrivers as wd


@click.command()
def main(args=None):
    """Console script for install_webdrivers."""
    if not os.environ.get("TRAVIS"):
        click.echo(
            "install-webdrivers actually only supports install on Travis-CI."
        )
    click.echo("Installing the latest version of chromedriver.")
    wd.install_latest_chromedriver()
    click.echo("Installing the latest version of geckodriver.")
    wd.install_latest_geckdriver()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
