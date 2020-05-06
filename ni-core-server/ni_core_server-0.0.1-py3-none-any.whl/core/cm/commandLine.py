import click
import coloredlogs
import tornado

from ..app import UploadHandler


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/upload', UploadHandler)  # Point d'accès des uploads
        ]
        tornado.web.Application.__init__(self, handlers)


@click.command(name='core_server')
@click.option('--port', '-p', default=8888, help='Port listening server')
@click.option('--log-level', '-l', default='INFO', help='Log level')
def cm(port, log_level):
    """
    Utilitaire de ligne de commande permettant de récupérer tous les scénarii d'un test.
    :return:
    """
    coloredlogs.install(level=log_level)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
