#!python
import logging
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
    # os.environ['DJANGO_SETTINGS_MODULE'] = "crm.settings"
    os.environ.setdefault("DJANGO_CONFIGURATION", 'Development')

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

    try:
        from configurations.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            pass

        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
