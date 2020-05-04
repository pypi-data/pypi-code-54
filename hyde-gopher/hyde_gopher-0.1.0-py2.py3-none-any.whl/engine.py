# This file is based on Hyde's engine.py
from pathlib import Path
from commando import (
    Application,
    command,
    store,
    subcommand,
    true,
    version
)
from commando.util import getLoggerWithConsoleHandler
from hyde.model import Config
from hyde.site import Site
from . import generator, server
from . import _version


class Engine(Application):
    def __init__(self, raise_exceptions=False):
        logger = getLoggerWithConsoleHandler('hyde-gopher')
        super(Engine, self).__init__(
            raise_exceptions=raise_exceptions,
            logger=logger
        )
    
    @command(
        description="hyde-gopher - build hyde sites for gopher",
        epilog='Use %(prog)s {command} -h to get help on individual commands'
    )
    @true('-x', '--raise-exceptions', default=None,
          help="Don't handle exceptions.")
    @version('--version', version='%(prog)s ' + _version)
    @store('-s', '--sitepath', default='.', help="Location of the hyde site")
    def main(self, args):
        """
        Will not be executed. A sub command is required. This function exists
        to provide common parameters for the subcommands and some generic stuff
        like version and metadata
        """
        if args.raise_exceptions in (True, False):
            self.raise_exceptions = args.raise_exceptions
        return Path(args.sitepath).absolute()
    
    @subcommand('gen', help='Generate the site')
    @store('-c', '--config-path', default='site.yaml', dest='config',
           help='The configuration used to generate the site')
    @store('-d', '--deploy-path', dest='deploy', default=None,
           help='Where should the site be generated?')
    # always regen
    def gen(self, args):
        """
        The generate command. Generates the site at the given
        deployment directory.
        """
        sitepath = self.main(args)
        site = self.make_site(sitepath, args.config, args.deploy)
        self.logger.info("Regenerating the site...")
        generator.generate_all(site)
        self.logger.info("Generation complete.")
    
    @subcommand('serve', help='Serve the website')
    @store('-a', '--address', default='localhost', dest='address',
           help='The address where the website must be served from.')
    @store('-p', '--port', type=int, default=7070, dest='port',
           help='The port where the website must be served from.')
    @store('-c', '--config-path', default='site.yaml', dest='config',
           help='The configuration used to generate the site')
    @store('-d', '--deploy-path', dest='deploy', default=None,
           help='Where should the site be generated?')
    def serve(self, args):
        """
        The serve command. Serves the site at the given
        deployment directory, address and port. Regenerates
        the entire site or specific files based on the request.
        """
        sitepath = self.main(args)
        site = self.make_site(sitepath, args.config, args.deploy)
        server.serve(site, args.address, args.port)

    def make_site(self, sitepath, config, deploy=None):
        """
        Creates a site object from the given sitepath and the config file.
        """
        config = Config(sitepath, config_file=config)
        config.deploy_root = deploy or Path(sitepath) / "deploy_gopher"
        return Site(sitepath, config)
