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

    dotenv_filename = '.crm'
    dotenv_path = find_dotenv(
        filename=dotenv_filename,
        raise_error_if_not_found=True,
        usecwd=False
    )
    print('Load dotenv configuration from %s' % dotenv_path)
    load_dotenv(dotenv_path=dotenv_path, override=True)

    os.environ.setdefault("DJANGO_CONFIGURATION", os.getenv('KRYNEGGER_CONFIGURATION').capitalize())
except BaseException as e:
    logging.error('Dotenv file could not loaded')
    # logging.exception(e)
    # traceback.print_exc()

application = get_wsgi_application()
