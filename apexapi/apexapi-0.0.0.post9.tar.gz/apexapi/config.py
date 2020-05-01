'''
This component is responsible for configuration management.
CURRENT SOURCES:

    1) Environment Variables
        Environment variables can be referenced in the config file.
        Example:

        foo: !env 'FOO'

        The value of "foo" would be set to whatever the value of the 
        environment variable 'FOO' was. If there is no value, an exception
        is raised.
    
    2) Config File
        Config files must be valid yaml files with *.yaml extension. 
        They must be located in the /config directory in order to be evaluated properly.
        To read values from a config file, simply pass the name of the config file, without
        the yaml extension, into the config class constructor. Then access the values of the
        variables as props.

        Assuming there is a file called "api.dev.yaml" located in the config directory, this
        would be a valid example:
        
        Example:
            c = Config("api.dev")
            print(c.host_address)  
TODO:
    Nice to haves would be additional config sources such as:
    
    1) service - Get config from a service endpoint (JSON)
        handy for more complex setups where a config service
        could be used
    
    2) db - Get config from a database
        for this one, you'd simply pass connection details
        to the database, and config opts would be loaded
        automatically.
'''

import yaml
import os
import json
from munch import munchify
from typing import Any, IO

APP_DIR = os.getcwd() # TODO: make this configurable

class Loader(yaml.SafeLoader):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream: IO) -> None:
        """Initialise Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)


def _include(loader: Loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""

    filename = os.path.abspath(os.path.join(loader._root, loader.construct_scalar(node)))
    extension = os.path.splitext(filename)[1].lstrip('.')

    with open(filename, 'r') as f:
        if extension in ('yaml', 'yml'):
            return yaml.load(f, Loader)
        elif extension in ('json', ):
            return json.load(f)
        else:
            return ''.join(f.readlines())

def _env(loader: Loader, node: yaml.Node) -> Any:
    """set value of key at node from environment variable"""
    if node.value in os.environ:
        return os.environ[node.value]
    raise Exception('undefined environment variable referenced %s' % (node.value))

yaml.add_constructor('!include', _include, Loader)
yaml.add_constructor('!env', _env, Loader)

class Config:
 
    def __init__(self, config_file):
        config_file_path = "%s/%s" % (APP_DIR, config_file)
        """ 
        The constructor for Config class. 
        Parameters: 
           env (string): load config vals based on env.
        """ 
        # check to see if the config file exist
        if not os.path.isfile(config_file_path):
            raise FileNotFoundError("%s was not found in %s" % (config_file, APP_DIR))
    
        with open(config_file_path, 'r') as f:
            self.props = yaml.load(f, Loader=Loader)
    
    def set_props(self):
        return munchify(self.props)