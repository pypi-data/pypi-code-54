
from .server import BaseServer
import sys
from urllib import parse;
from hehe import he

"""
 * 命令脚本接口类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
 *</pre>
"""
class ConsoleServer(BaseServer):


    def run(self):

        # 开始监听HTTP请求:
        self.consoleApp()

        return ;

    def consoleApp(self):

        # 创建对应的应用类对象
        app = he.config.appClass(he.config);
        # 创建请求对象
        app.initReqeust(self.getEnviron())
        # 运行应用
        app.runApp();
        # 返回响应body
        response = app.getRespone()
        # 设置响应头部

        return response.getContent()

    # 解析命令参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getEnviron(self):

        url = sys.argv[1]
        result = parse.urlparse(url)
        environ = {};

        environ['PATH_INFO'] = result.path
        environ['QUERY_STRING'] = result.query

        return environ;