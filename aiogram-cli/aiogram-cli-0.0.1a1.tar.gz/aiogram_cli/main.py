import typer
from aiogram_cli.loader import setup_plugins


def main():
    app = typer.Typer()
    setup_plugins(app)
    app()
