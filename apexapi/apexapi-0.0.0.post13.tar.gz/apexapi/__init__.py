import sys
import click
from werkzeug.serving import run_simple
from .apex import ApexService
import requests
import os

APEX_DIR = (os.path.dirname(__file__))

class ApexConfigException(Exception):
  pass

# TODO: write command to 'lint' or 'check' the app.yaml file w/out starting the server.

# This uses the 'application factory' pattern to produce the ApexService WSGI app.
# Gunicorn is used to serve up this app via Docker --> CMD ["gunicorn"  , "-b", "0.0.0.0:8499", "core:create_service('app.yaml')"]
def create_service():
  service = ApexService('app.yaml')
  return service

# Create a click 'group' to contain our cli commands.
@click.group()
def cli():
  pass

@cli.command()
def serve():
  """ starts a local development server. Do not use this for production. """
  service = ApexService('app.yaml')
  run_simple('127.0.0.1', 8499, service, use_debugger=False, use_reloader=True)

# @cli.command()
# def init():
#   """ initialize a new ApexAPI service project. """
#   # TODO: check if app.yaml already exist, and if so, do not overwrite.
#   # Prompt user to confirm overwrite or add flag --overwrite
#   with open('app.yaml', 'w+') as app:
#     tpl = open('%s/core/templates/app.yaml.tpl' % (APEX_DIR))
#     app.write(tpl.read())
#   print("ApexAPI is ready!")

# @cli.command()
# @click.option('--from-url', default=False, help="replace the app.yaml file with contents at a given url.")
# @click.option('--backup', default=True, help="create a local backup of the current app file before fetching the new one.")
# def fetch(from_url, backup):
#   """ fetch the app config """
#   r = requests.get(from_url).text
#   src = "%s/app.yaml" % APP_DIR
#   dst = "%s/app.back" % APP_DIR
#   os.rename(src, dst)
#   f = open(src, 'w+')
#   f.write(r)
#   f.close()

def main():
    """ Apex CLI """
    try:
      cli()
    # TODO: add additional core exceptions here
    except ApexConfigException as config_error:
      print("CONFIG ERROR: " + str(config_error))
      sys.exit(1)
    except FileNotFoundError as FNF:
      print("CONFIG ERROR: " + str(FNF))
      sys.exit(1)
    # except Exception as err:
    #   print("UNKNOWN ERROR: %s" % (str(err)))
    #   sys.exit(1)