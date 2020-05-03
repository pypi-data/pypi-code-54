import click

from pobject import I
from file_util import File


@click.group()
def cli():
    pass


@cli.command()
@click.argument("file-path", type=click.Path())
def create(file_path):

    empty_json_dict = {}

    json_string = I(empty_json_dict).to_json_string()

    File(file_path).write(json_string)

    print(f"JSON file created at: {file_path}")
