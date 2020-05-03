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

from ixian.task import Task
from ixian.config import CONFIG
from ixian_docker.modules.docker.tasks import run, Compose


class Manage(Task):
    """
    Shortcut to Django's manage.py script.

    This shortcut gives access to manage.py within the context of the app
    container. Volumes and environment variables for loaded modules are loaded
    automatically via docker-compose.

    The script is run by calling `{PYTHON.BIN} manage.py`. Arguments are passed
    through to the script.

    Type `ix manage --help` for it's built-in help.
    """

    name = "manage"
    category = "django"
    short_description = "Django manage.py script."
    depends = ["compose_runtime"]

    def execute(self, *args):
        manage(*args)


MANAGE_CMD = "{PYTHON.BIN} manage.py"


def manage(*args):
    """Shim around `manage.py`"""
    return run(MANAGE_CMD, *args)


class Shell(Task):
    """
    Shortcut to Django python shell.

    This shortcut runs within the context of the app container. Volumes and
    environment variables for loaded modules are loaded automatically via
    docker-compose.
    """

    name = "shell"
    category = "django"
    short_description = "open django python shell"
    depends = ["compose_runtime"]

    def execute(self, *args):
        return manage("shell_plus", *args)


class ShellPlus(Task):
    """
    Shortcut to Django extensions shell_plus.

    This shortcut runs within the context of the app container. Volumes and
    environment variables for loaded modules are loaded automatically via
    docker-compose.
    """

    name = "shell_plus"
    category = "django"
    short_description = "open django shell_plus"
    depends = ["compose_runtime"]

    def execute(self, *args):
        return manage("shell_plus", *args)


class DjangoTest(Task):
    """
    Shortcut to Django test runner

    This shortcut runs within the context of the app container. Volumes and
    environment variables for loaded modules are loaded automatically via
    docker-compose.

    The command automatically sets these settings:
       --settings={DJANGO.SETTINGS_TEST}
       --exclude-dir={DJANGO.SETTINGS_MODULE}

    Arguments are passed through to the command.
    """

    name = "django_test"
    category = "testing"
    parent = ["test", "test_py"]
    depends = ["compose_runtime"]
    short_description = "django test runner"

    def execute(self, *args):
        required_args = [
            "--settings={DJANGO.SETTINGS_TEST}",
            "--exclude-dir={DJANGO.SETTINGS_MODULE}",
        ]
        args = args or [CONFIG.PYTHON.ROOT_MODULE]
        return manage("test", *required_args, *args)


class Migrate(Task):
    """
    Run django migrations.
    """

    name = "migrate"
    category = "django"
    short_description = "run database migrations"
    depends = ["compose_runtime"]

    def execute(self, *args):
        return manage("migrate", *args)


class MakeMigrations(Task):
    """
    Generate missing django migrations. This is a shortcut to
    `manage.py makemigrations`.

    By default this will generate migrations only for {CONFIG.PROJECT_NAME}.
    This is overridden whenever args are passed to this task.
    """

    name = "makemigrations"
    category = "django"
    short_description = "generate missing database migrations"
    depends = ["compose_runtime"]

    def execute(self, *args):
        return manage("makemigrations", *args)


class DBShell(Task):
    """
    Shortcut to `manage.py dbshell`
    """

    name = "dbshell"
    category = "django"
    short_description = "open a database shell"
    depends = ["compose_runtime"]

    def execute(self, *args):
        return manage("dbshell", *args)


class Runserver(Task):
    """
    Shortcut to `manage.py runserver 0.0.0.0:8000`

    This command maps port 8000:8000 so the server is accessible outside the
    container. Additional args are passed through to the command but the IP and
    port can not be changed.
    """

    name = "runserver"
    category = "django"
    short_description = "start django test server"
    depends = ["compose_runtime"]

    def execute(self, *args):
        return run(
            MANAGE_CMD, "--service-ports", "runserver", *(args or ["0.0.0.0:8000"]),
        )
