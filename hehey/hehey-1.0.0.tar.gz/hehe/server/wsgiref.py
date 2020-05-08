
from wsgiref.simple_server import make_server
from .server import BaseServer
from hehe import he

"""
 * 服务接口类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
 *</pre>
 *<B>日志：</B>
 *<pre>
 *  略
 *</pre>
 *<B>注意事项：</B>
 *<pre>
 *  略
 *</pre>
"""
class WsgirefServer(BaseServer):


    def run(self):

        localport = he.config.localport

        httpd = make_server('', localport, self.wsgiApp)
        print('Serving HTTP on port http://localhost:{0}/signup/login'.format(localport))
        # 开始监听HTTP请求:
        httpd.serve_forever()

        return ;

    def wsgiApp(self,environ, start_response):

        # 创建对应的应用类对象
        app = he.config.appClass(he.config);
        # 创建请求对象
        app.initReqeust(environ)
        # 运行应用
        app.runApp();
        # 返回响应body
        response = app.getRespone()
        # 设置响应头部
        start_response(response.buildHttpStatus(), response.buildHttpHeaders())

        return response.getContent()