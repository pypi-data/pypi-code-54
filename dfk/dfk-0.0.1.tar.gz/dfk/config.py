import ipaddress
import json
from json import JSONDecodeError
from pathlib import Path

import click
from defektor_api import Configuration
from jsonschema import validate, ValidationError

CONFIG_DATA = None
CONFIG_PATH = Path.home().joinpath(".config").joinpath("dfk").joinpath("config")

config_schema = {
    "type": "object",
    "properties": {
        "address": {"type": "string"},
        "port": {"type": "number"},
        "debug": {"type": "boolean"},
    },
    "required": ["address", "debug"]
}


def load_config():
    if not Path.exists(CONFIG_PATH):
        click.echo("ERROR: Please login!")
        exit(1)

    try:
        with open(str(CONFIG_PATH)) as config_file:
            config_data = json.loads(config_file.read().replace('\n', ''))

        validate(config_data, config_schema)

        ipaddress.ip_address(config_data["address"])

        CONFIG_DATA = config_data
    except (JSONDecodeError, ValidationError) as schema_format_exception:
        click.echo(f"ERROR: error in configuration file.\n{schema_format_exception}")
        exit(1)
    except IOError as file_read_exception:
        click.echo(f"ERROR: reading configuration file.\n{file_read_exception}")
        exit(1)
    except ValueError as address_format_exception:
        click.echo(f"ERROR: address not valid in configuration file.\n{address_format_exception}")
        exit(1)

    config: Configuration = Configuration()
    if CONFIG_DATA['debug']:
        config.host = f"https://virtserver.swaggerhub.com/jaimelive/defektorControlAPI/1.0.0"
    elif CONFIG_DATA['address'] and CONFIG_DATA['port']:
        config.host = f"https://{CONFIG_DATA['address']}:{CONFIG_DATA['port']}/defektorControlAPI/1.0.0"

    return config


def require_login(func):
    load_config()
