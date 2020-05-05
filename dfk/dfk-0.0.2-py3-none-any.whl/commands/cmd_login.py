import click

from dfk.config import write_config


@click.command("login")
@click.argument("ip", required=True)
@click.argument("port", required=True)
@click.option("--debug", default=False, is_flag=True)
def cli(ip, port, debug):
    """🔑 defektor login."""

    write_config(str(ip), int(port), bool(debug))
