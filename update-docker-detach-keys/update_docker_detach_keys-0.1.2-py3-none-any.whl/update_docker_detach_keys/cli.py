import click
from pathlib import Path
from json_file import JSONFile


@click.command()
def cli():
    config_path = Path.home().joinpath(".docker/config.json")
    json_file = JSONFile(config_path, keep_formatting=True)
    json_file.update_key_value(key="detachKeys", value="ctrl-e,e")
    print(json_file.pretty)
    return True
