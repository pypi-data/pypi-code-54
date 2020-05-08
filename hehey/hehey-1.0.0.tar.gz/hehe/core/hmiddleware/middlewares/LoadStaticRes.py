
from hehe import he
import os;

"""
 * 加载静态资源
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class LoadStaticRes:


    def handle(self):

        # 判断是否静态文件
        routerRequest = he.app.routerRequest;
        routeUrl = routerRequest.getRouteUrl();
        if routeUrl:
            ext = os.path.splitext(routeUrl)[1][1:]
            if ext and ext != '.py':
                self.read_static_res(ext);
                he.raiseAppstopException()
                return False;

    def read_static_res(self, ext):

        routerRequest = he.app.routerRequest;
        routeUrl = routerRequest.getRouteUrl();
        # 读取文件
        staticfilepath = he.app.conf.staticPath + '/' + routeUrl;

        if os.path.isfile(staticfilepath):
            reponse = he.app.getRespone();
            if ext in ['html']:
                reponse.sendRawFile(staticfilepath)
            else:
                reponse.sendFile(staticfilepath)
        else:
            response = he.app.getRespone()
            response.setStatusCode(404)

        return;