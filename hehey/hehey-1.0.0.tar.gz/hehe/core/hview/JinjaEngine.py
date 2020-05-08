
from .view import Engine
from jinja2 import Environment, FileSystemLoader

"""
 * Jinja2引擎类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class JinjaEngine(Engine):


    def __init__(self,**config):

        super().__init__(**config)
        opts = self.config.copy();
        searchpath = opts.get('searchpath',None)
        if searchpath:
            opts.pop("searchpath")

        opts['loader'] = FileSystemLoader(searchpath)
        self.env = Environment(**opts)


    def fetchInternal(self, tpl, data = []):

        template = self.env.get_template(tpl)

        return template.render(**data)

