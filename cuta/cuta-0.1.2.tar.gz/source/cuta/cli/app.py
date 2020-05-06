
import emoji
import re
import sys
import typer
from typing import List

import cuta

from . import utils


app = typer.Typer()


@app.command("init")
def init():
    """
    Initialize application.
    """
    utils.version()

    api = cuta.from_env()
    app = api.get_app()

    create_env(app)
    create_package(app)

    utils.complete()


def create_env(app):
    """
    Create base environment
    """
    tag = f"ylathouris/cuta:{app.platform}-{app.runtime}"
    if cuta.core.env.exists(tag):
        return

    color = utils.get_color()
    utils.set_color(typer.colors.BRIGHT_CYAN)
    utils.title("Creating Base Environment", emoji="whale")

    report = {}
    for item in cuta.core.env.pull(app.base):
        uid = item.get("id", "")
        status = item.get("status", "")
        progress = item.get("progress")
        lines = []
        if progress:
            report[uid] = f"{uid}: {status} {progress}"
            lines = report.values()
            count = len(lines)
            for line in lines:
                utils.echo(line)

            utils.clear_lines(count)

    utils.set_color(color)


def create_package(app):
    """
    Initialize package config/files.
    """
    color = utils.get_color()
    utils.set_color(typer.colors.BRIGHT_YELLOW)
    utils.title("Creating Package", emoji="package")

    for output in app.init():
        utils.echo(output)

    utils.set_color(color)


@app.command("add")
def add_deps(deps: List[str], dev: bool = typer.Option(False, "--dev")):
    echo_version()
    api = cuta.from_env()
    app = api.get_app()

    typer.echo(yellow(emoji.emojize(":package: Adding dependencies...")))
    for output in app.add(deps, dev=dev):
        typer.echo(yellow("Packaging: ") + output)

    done()


@app.command("remove")
def remove_deps(deps: List[str], dev: bool = typer.Option(False, "--dev")):
    echo_version()
    api = cuta.from_env()
    app = api.get_app()

    typer.echo(yellow(emoji.emojize(":package: Removing dependencies...")))
    for output in app.remove(deps, dev=dev):
        typer.echo(yellow("Packaging: ") + output)

    done()


@app.command("build")
def build():
    echo_version()
    api = cuta.from_env()
    app = api.get_app()

    typer.echo(green(emoji.emojize(f":package: Building app: {app.tag}")))
    for output in app.build():
        typer.echo(cyan("Docker: ") + output)

    done()


@app.command("shell")
def shell():
    echo_version()
    typer.echo(green(emoji.emojize(f":whale: Initializing cuta shell")))
    api = cuta.from_env()
    app = api.get_app()
    app.shell()


@app.command("delete")
def delete():
    echo_version()
    api = cuta.from_env()
    app = api.get_app()
    typer.echo(yellow(emoji.emojize(f":package: Deleting app: {app.name}")))
    app.delete()
    done()


def echo_version():
    """
    """
    msg = green(f"Cuta Version: {cuta.version}")
    typer.echo(msg)


def cyan(msg: str) -> str:
    return typer.style(msg, fg=typer.colors.BRIGHT_CYAN)


def blue(msg: str) -> str:
    return typer.style(msg, fg=typer.colors.BRIGHT_BLUE)


def green(msg: str) -> str:
    return typer.style(msg, fg=typer.colors.BRIGHT_GREEN)


def yellow(msg: str) -> str:
    return typer.style(msg, fg=typer.colors.BRIGHT_YELLOW)


def done(msg="Complete!"):
    text = typer.style(msg, fg=typer.colors.BRIGHT_WHITE, bold=True)
    typer.echo(text)
