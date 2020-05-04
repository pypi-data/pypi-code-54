from flask import Flask
from flask_gopher import GopherExtension, GopherRequestHandler
from hyde.template import Template
from . import generator


def serve(site, address, port):
    app = Flask(__name__)
    gopher = GopherExtension(app)
    generator.gopher = gopher
    generator.gopher_menu = lambda: gopher.menu
    site.config.base_path = "/"
    templates = Template.find_template(site)
    templates.configure(site)
    macros = templates.loader.load(templates.env, "macros.j2")
    templates.env.globals.update(macros.module.__dict__)
    stack = list()
    site.content.load()
    stack.append(site.content)
    while stack:
        current = stack.pop()
        app.add_url_rule(
            current.url, current.relative_path,
            lambda c=current: generator.generate_node(site, c)
        )
        for child in current.resources:
            app.add_url_rule(
                child.url, child.relative_path,
                lambda c=child: generator.generate_resource(site, templates, c)
            )
        for child in current.child_nodes:
            stack.append(child)
    app.run(address, port, request_handler=GopherRequestHandler)
