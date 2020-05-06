from __future__ import absolute_import, unicode_literals

import logging
import traceback

from django.core import checks
from django.core.checks import register, Tags

# from .exceptions import DatabaseConnectionError



# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ['celery_app']

# @register()
# def database_check(app_configs, **kwargs):
#     errors = []
#     from django.db import connections
#     from django.db.utils import OperationalError
#     db_conn = connections['default']
#     try:
#         c = db_conn.cursor()
#     except OperationalError as operational_exception:
#         errors.append(DatabaseConnectionError(operational_exception, db_conn))
#     finally:
#         return errors


def manage():
    import os
    import sys

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", 'production')

    import os
    from dotenv import load_dotenv
    # explicitly providing path to '.env'
    from pathlib import Path  # python3 only
    env_path = Path('.') / '.crm'
    load_dotenv(dotenv_path=env_path)

    os.environ.setdefault("DJANGO_CONFIGURATION", os.getenv('KRYNEGGER_CONFIGURATION'))

    from configurations.management import execute_from_command_line
    execute_from_command_line(sys.argv)