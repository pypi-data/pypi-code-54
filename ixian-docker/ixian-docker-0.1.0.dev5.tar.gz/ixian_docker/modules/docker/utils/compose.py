# Copyright [2018-2020] Peter Krenesky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging

from ixian.config import CONFIG
from ixian.utils.argparse import argunparse, merge_parser_args
from ixian.utils.process import execute

logger = logging.getLogger(__name__)


def get_run_parser(include_compose_parser=True) -> argparse.ArgumentParser:
    """
    get argparse.ArgumentParser for docker-compose run.
    :param include_compose_parser:
    :return: parser capable of parsing command line args for docker-compose run
    """
    if include_compose_parser:
        parser = get_compose_parser()
    else:
        parser = argparse.ArgumentParser(add_help=False)
        parser.arguments = []

    new_args = [
        dict(args=["-d", "--detach"], action="store_true"),
        dict(args=["--name"], action="store"),
        dict(args=["--entrypoint"], action="store"),
        dict(args=["-e"], action="append"),
        dict(args=["-l", "--label"], action="append", nargs=1),
        dict(args=["-u", "--user"], action="store"),
        dict(args=["--no-deps"], action="store_true"),
        dict(args=["--rm"], action="store_true"),
        dict(args=["--publish"], action="store"),
        dict(args=["--service-ports"], action="store_true"),
        dict(args=["--use-aliases"], action="store_true"),
        dict(args=["-v", "--volume"], action="append", nargs=1),
        dict(args=["-T"], action="store_true"),
        dict(args=["-w", "--workdir"], action="store"),
    ]
    parser.arguments.extend(new_args)
    for datum in new_args:
        copy = datum.copy()
        args = copy.pop("args")
        parser.add_argument(*args, **copy)

    return parser


def get_compose_parser() -> argparse.ArgumentParser:
    """
    get argparse.ArgumentParser for docker-compose.
    :return: parser capable of parsing command line args for docker-compose
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.arguments = [
        dict(args=["-f", "--file"], action="store"),
        dict(args=["-p", "--project-name"], action="store"),
        dict(args=["--verbose"], action="store_true"),
        dict(args=["--log-level"], action="store"),
        dict(args=["--no-ansi"], action="store_true"),
        dict(args=["--version"], action="store_true"),
        dict(args=["--tls"], action="store_true"),
        dict(args=["--tlscacert"], action="store"),
        dict(args=["--tlscert"], action="store"),
        dict(args=["--tlskey"], action="store"),
        dict(args=["--tlsverify"], action="store_true"),
        dict(args=["--skip-hostname-check"], action="store_true"),
        dict(args=["--project-directory"], action="store"),
        dict(args=["--compatibility"], action="store_true"),
        dict(args=["--env-file"], action="store"),
    ]

    for datum in parser.arguments:
        copy = datum.copy()
        args = copy.pop("args")
        parser.add_argument(*args, **copy)
    return parser


# TODO: typehint
def parse_compose_args(command, *args: str, **defaults):
    """
    Parse docker compose args and merge with `COMPOSE_BASE_ARGS`.
    """

    # normalize args
    args = " ".join(args).split(" ")
    default_args = " ".join(defaults).split(" ")
    base_args = getattr(CONFIG.DOCKER, "COMPOSE_BASE_ARGS", [])
    if not isinstance(base_args, str):
        base_args = " ".join(base_args).split(" ")

    # parse args as given
    run_parser = get_run_parser()
    _, unknown_args = run_parser.parse_known_args(args)

    # find the first arg that isn't a known arg, anything before it is an option for compose
    # Anything after is for the command. Reparse args just in case there were any ambiguous flags.
    index_of_first_unknown = args.index(unknown_args[0]) if unknown_args else None
    compose_args = args[:index_of_first_unknown]
    command_args = args[index_of_first_unknown:]

    # get run args
    # mix base_args and args - both should only be for compose or run
    default_options, _ = run_parser.parse_known_args(default_args)
    compose_options, _ = run_parser.parse_known_args(compose_args)
    run_options = merge_parser_args(run_parser, base_args, default_args, compose_args)

    # get compose_options and remove from run_options
    # use the copy from run_options
    compose_parser = get_compose_parser()
    compose_options = merge_parser_args(
        compose_parser, base_args, default_args, compose_args
    )
    for key in compose_options.keys():
        compose_options[key] = run_options.pop(key)

    return (
        argunparse(compose_options, compose_parser),
        argunparse(run_options, run_parser),
        command_args,
    )


def run(command, *args, **options):
    """
    Wrapper around docker-compose run
    :param command: command to run
    :param args: args to docker-compose and docker-compose command
    :param options:
    :return:
    """
    return compose("run", command, *args, **options)


def compose(compose_command, command, *args, **options):
    logger.debug(
        f'compose {compose_command} command="{command}" args={args} options={options}'
    )
    # Add default ENV and configured ENVs
    env = {
        "APP_DIR": CONFIG.DOCKER.APP_DIR,
        "ROOT_MODULE_PATH": CONFIG.PYTHON.ROOT_MODULE_PATH,
    }
    env.update(CONFIG.DOCKER.COMPOSE_ENV)
    env.update(options.pop("env", {}))

    # parse and normalize args
    app = options.pop("app", None) or CONFIG.DOCKER.DEFAULT_APP
    compose_args, run_args, command_args = parse_compose_args(
        compose_command, env=env, *args, **options
    )
    template = "docker-compose{CR} {compose_args} {compose_command}{CR} {run_args} {app} {command} {command_args}"

    print("compose_args: ", compose_args)
    print("run_args: ", run_args)
    print("command_args: ", command_args)

    def render_command():
        with_cr = "{} \\\n"
        formatted = template.format(
            CR=" \\\n",
            compose_args=" ".join((with_cr.format(line) for line in compose_args)),
            compose_command=compose_command,
            run_args=" ".join((with_cr.format(line) for line in run_args)),
            command_args=" ".join((with_cr.format(line) for line in command_args)),
            app=app,
            command=CONFIG.format(command or ""),
            image=CONFIG.DOCKER.IMAGE,
        )
        logger.info(CONFIG.format(formatted))

    render_command()
    return execute(
        template.format(
            CR="",
            compose_args=" ".join(compose_args),
            compose_command=compose_command,
            run_args=" ".join(run_args),
            app=app,
            command=command or "",
            command_args=" ".join(command_args),
        ),
        env=CONFIG.DOCKER.COMPOSE_ENV,
        silent=True,
    )
