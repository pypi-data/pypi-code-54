import typer
from aiogram_cli.loader import load_plugins_list


def plugins():
    """
    Get plugins list
    """
    for entry_point in load_plugins_list():
        typer.echo(f" - {entry_point}")
