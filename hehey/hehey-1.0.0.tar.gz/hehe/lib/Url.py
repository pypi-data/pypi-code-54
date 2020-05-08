
from hehe import he

"""
 * url 工具类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
 *</pre>
"""
class Url():

    # 获取当前route pathinfo
    # <B> 说明： </B>
    # <pre>
    # 不带参数
    # </pre
    @classmethod
    def getRoute(self):

        return he.app.route;

    # 生成地址
    # <B> 说明： </B>
    # <pre>
    # 不带参数
    # </pre
    def toUrl(self,url,vars = {},scheme = False,**options):

        fullUrl = he.app.toUrl(url, vars,**options)

        if scheme:
            fullUrl = he.app.hrequest.getHostUrl() + fullUrl

        return fullUrl;