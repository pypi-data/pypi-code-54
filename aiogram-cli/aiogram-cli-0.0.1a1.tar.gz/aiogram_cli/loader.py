from typing import Generator

from pkg_resources import EntryPoint, iter_entry_points

import typer
from typer import Typer


def load_plugins_list() -> Generator[EntryPoint, None, None]:
    yield from iter_entry_points(group="aiogram_cli.plugins", name=None)


def setup_plugins(app: Typer):
    for entry_point in load_plugins_list():
        try:
            plugin_loader = entry_point.resolve()
            plugin_loader(app)
        except Exception:
            typer.echo("Failed to load plugin {plugin}", color="red")
            raise
