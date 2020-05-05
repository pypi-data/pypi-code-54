from aiogram_cli.commands.plugins import plugins
from aiogram_cli.commands.version import version
from typer import Typer


def setup(app: Typer):
    app.command()(plugins)
    app.command()(version)
