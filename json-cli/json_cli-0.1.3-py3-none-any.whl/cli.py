import click

from pobject import I
from file_util import File
from json_cli.json_file import JSONFile

FILE_PATH_CONTEXT = "file_path"


@click.group(invoke_without_command=True)
@click.option("--file", "file_path")
@click.pass_context
def cli(context, file_path):
    if context.invoked_subcommand is None:
        print(JSONFile(file_path).pretty)
    else:
        context.ensure_object(dict)
        context.obj[FILE_PATH_CONTEXT] = file_path


@cli.command()
@click.argument("key-value")
@click.pass_context
def add(context, key_value):
    file_path = context.obj[FILE_PATH_CONTEXT]
    json_file = JSONFile(file_path)
    json_file.add_key_value_string(key_value)
    print(json_file.pretty)


@cli.command(help="Alias for add")
@click.argument("key-value")
@click.pass_context
def update(context, key_value):
    file_path = context.obj[FILE_PATH_CONTEXT]
    json_file = JSONFile(file_path)
    json_file.add_key_value_string(key_value)
    print(json_file.pretty)


@cli.command()
@click.argument("file-path", type=click.Path())
def create(file_path):

    empty_json_dict = {}

    json_string = I(empty_json_dict).to_json_string()

    File(file_path).write(json_string)

    print(f"JSON file created at: {file_path}")
