
import click

from click import Context

from pobject import I
from file_util import File
from json_cli.json_file import JSONFile

FILE_PATH_CONTEXT = "file_path"


@click.group(invoke_without_command=True)
@click.option("--file", "file_path")
@click.pass_context
def cli(context: Context, file_path):
    if context.invoked_subcommand is None:
        if file_path:
            json_file = JSONFile(file_path)

            if not json_file.exists():
                json_file.create()
                print(f'Created JSON file: {json_file.path}')

            print(json_file.pretty)
        else:
            _help = context.get_help()
            print(_help)
    else:
        context.ensure_object(dict)
        context.obj[FILE_PATH_CONTEXT] = file_path


@cli.command()
@click.argument("key")
@click.pass_context
def remove(context, key):
    file_path = context.obj[FILE_PATH_CONTEXT]
    json_file = JSONFile(file_path)
    result = json_file.remove(key)

    if result is False:
        print(f'Key: "{key}" not found.')

    print(json_file.pretty)


@cli.command()
@click.argument("arg", nargs=-1)
@click.pass_context
def update(context, arg):

    file_path = context.obj[FILE_PATH_CONTEXT]
    json_file = JSONFile(file_path)

    if isinstance(arg, tuple):
        # Multi args
        json_file.update_key_value(key=arg[0], value=arg[1])
    else:
        json_file.add_key_value_string(arg)

    print(json_file.pretty)


@cli.command()
@click.argument("file-path", type=click.Path())
def create(file_path):

    empty_json_dict = {}

    json_string = I(empty_json_dict).to_json_string()

    File(file_path).write(json_string)

    print(f"JSON file created at: {file_path}")
