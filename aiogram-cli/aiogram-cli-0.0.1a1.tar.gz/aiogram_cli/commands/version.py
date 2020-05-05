# import aiogram
import typer

import aiogram_cli


def version():
    # typer.echo(f"aiogram: v{aiogram.__version__}")
    typer.echo(f"aiogram-cli: v{aiogram_cli.__version__}")
