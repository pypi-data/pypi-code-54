from __future__ import absolute_import, unicode_literals

def manage():
    import os
    import sys

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

    try:
        from dotenv import load_dotenv, find_dotenv
        from pathlib import Path

        dotenv_filename = '.crm'
        dotenv_path = find_dotenv(
            filename=dotenv_filename,
            raise_error_if_not_found=True,
            usecwd=True
        )
        print('Load dotenv configuration from %s' % dotenv_path)
        load_dotenv(dotenv_path=dotenv_path, override=True)

        os.environ.setdefault("DJANGO_CONFIGURATION", os.getenv('KRYNEGGER_CONFIGURATION').capitalize())
    except BaseException as e:
        logging.error('Dotenv file could not loaded')

    from configurations.management import execute_from_command_line
    execute_from_command_line(sys.argv)

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
