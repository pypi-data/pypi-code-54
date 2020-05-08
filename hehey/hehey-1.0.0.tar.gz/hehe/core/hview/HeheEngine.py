
from .view import Engine
from htemplate.view import View
from hehe import he
from htemplate.view import reg_temp_context

@reg_temp_context()
def hehecontext():

    return {"_request":he.app.hrequest};

"""
 * 视图引擎类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class HeheEngine(Engine):

    def fetchInternal(self, tpl, data = []):

        opts = self.config.copy();
        heheView = View(opts);

        return heheView.fetch(tpl,data)

