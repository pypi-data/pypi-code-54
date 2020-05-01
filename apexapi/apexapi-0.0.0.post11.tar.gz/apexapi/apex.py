""" This is the core Apex class """
import importlib
import json
from .config import Config
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from munch import munchify
import os
import sys
import logging

APEX_PATH = os.path.dirname((__file__))

# IDEA: write a Redis caching plugin (for prod use)

# IDEA: look into defining middleware hooks. Ordering is critical for this to work.
# IDEA: provide --reload flag to serve to enable hot reloading for any config changes in yaml file / python file in app.

# TODO: build standard response handlers for 40x 50x
# TODO: bring in jwt/acl system

# TODO: build this dynamically, vs statically.
core_handlers = [
    'apex.send.ok', 
    'apex.send.json',
    'apex.cors.add'
    'apex.response.asjson'
]

class ApexService:

    def __init__(self, config):
        sys.path.append(APEX_PATH)
        sys.path.append(os.getcwd())
        
        self.config = Config(config).set_props()
        logging.basicConfig(**self.config.log.config)
        self.log = logging.getLogger(self.config.log.name)
        
        self.aem = ApexEndpointManager(self.config)
        for endpoint in self.aem.endpoints:
            self.log.debug("%s endpoint loaded" % (endpoint))

        # get our url matching rules from the defined endpoints.
        self.rules = Map(self.aem.get_rules())

    def dispatch_request(self, req):
        adapter = self.rules.bind_to_environ(req.environ)
        res = Response()
        try:
            #1. try to match the req to a given rule within the defined endpoints
            endpoint, values = adapter.match()
            req.params = munchify(values)
            req.apex = self.config
            res.json = munchify({})
            #2. upon matching, iterate through the function list in the stack
            for func in self.aem.endpoints[endpoint].functions:
                if func(req, res) is not None:
                    break
            return res
            # return Response(self.callbacks[endpoint](**values))
        except HTTPException as e:
            err = {
                'code': e.code,
                'message': e.description
            }
            res.content_type = 'application/json'
            return Response(json.dumps({"error": err}), e.code)

    def wsgi_app(self, environ, start_response):
        req = Request(environ)
        res = self.dispatch_request(req)
        return res(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


class ApexEndpointManager:
    """ Class to manage endpoints within Apex """

    def __init__(self, config):
        self.config = config
        self.endpoints = {}
        self._bootstrap()

    def _bootstrap(self):
        for endpoint in self.config.endpoints:
            self.endpoints[endpoint] = (ApexEndpoint(**self.config.endpoints[endpoint]))
    
    def get_rules(self):
        rules = []
        for e in self.endpoints:
            rules.append(
                Rule(self.endpoints[e].route, 
                     methods=self.endpoints[e].methods,
                     endpoint=e
                )
            )
        return rules
    
class ApexEndpoint:

    def __init__(self, route, methods, stack):
        self.route = route
        self.methods = methods
        self.stack = stack
        self.functions = [] # ordered list of functions that will run for this endpoint.
        self._bootstrap()
    
    def _bootstrap(self):
        for handler in self.stack:
            self.functions.append(self._get_handler_function(handler))
    
    def _get_handler_function(self, handler):
        # TODO: re-write this garbage.
        # TODO: make this function my dynamic and
        # capable of loading functions from multiple
        # sources.

        # NOTE: apex.* is a reserved namespace 

        segments = handler.split('.')
        apex_module_path = 'apexapi.core.handlers'
        
        module = '.'.join(segments[:-1])
        method = segments[-1]
        handler = module

        if handler.startswith('apex.'):
            handler = "%s.%s" % (apex_module_path, module)
        
        # load path dynamically
        # log.debug(handler, method)
        return getattr(importlib.import_module(handler), str(method))
