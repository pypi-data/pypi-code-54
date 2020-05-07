import logging
import os
import sys

from configurations.wsgi import get_wsgi_application

PROJECT_DIR = os.path.abspath(__file__)
sys.path.append(PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

try:
    from dotenv import load_dotenv, find_dotenv
    from pathlib import Path

    dotenv_path = find_dotenv(raise_error_if_not_found=True)
    dotenv_result = load_dotenv(dotenv_path=dotenv_path)
    print('dotenv[wsgi] configuration %s from "%s"' % ('loaded' if dotenv_result else 'not loaded', dotenv_path))
except BaseException as e:
    logging.error('dotenv[wsgi] configuration could not loaded')
    logging.exception(e)
    os.environ.setdefault("KRYNEGGER_CONFIGURATION", "development")
finally:
    os.environ.setdefault("DJANGO_CONFIGURATION", os.getenv('KRYNEGGER_CONFIGURATION').capitalize())

application = get_wsgi_application()
