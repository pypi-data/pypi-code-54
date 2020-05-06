from aiohttp.web_app import Application

from yades_api import routes
from yades_api.middlewares import token_middleware


def create_app(loop, config, db):
    app = Application(loop=loop, middlewares=[token_middleware])
    app['config'] = config
    app['db'] = db

    routes.setup(app)

    return app
