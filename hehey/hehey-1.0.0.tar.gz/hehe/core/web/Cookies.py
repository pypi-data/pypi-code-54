
"""
 * http cookie信息对象
 *<B>说明：</B>
 *<pre>
 *  使用
 *</pre>
 *<B>示例：</B>
 *<pre>
 * 略
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
class Cookies:

    def __init__(self):

        self._cookies = {}

        return ;

    def __iter__(self):
        return self._cookies

    def __getitem__(self, key):

        return self._cookies.get(key, None)

    # 获取全部cookie 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getCookies(self):

        return self._cookies

    # 设置cookies
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setCookies(self,cookies):

        self._cookies = cookies

    # 设置cookie 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def set(self, name, value = None,**params):

        if isinstance(value,dict):
            cookie = {'name': name};
            cookie.update(value)
        else:
            cookie = {'name': name, 'value': value};

        cookie.update(params)
        self._cookies[name] = cookie

        return ;

    # 获取header 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def get(self, name, defaultValue=None):

        return self._cookies.get(name, defaultValue)

    # 是否存在cookie
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def has(self, name):

        valueList = self._cookies.get(name, None)
        if valueList is None:
            return False
        else:
            return False

    # 删除cookie
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def remove(self, name):

        self._cookies.pop(name)

        return ;

    # 删除全部cookies
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def removeAll(self):

        self._cookies = {};

        return ;

    # 计算cookie长度
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getCount(self):

        return len(self._cookies)

    # 格式化cookie
    # <B> 说明： </B>
    # <pre>
    # 用于http header
    # </pre>
    def formatCookies(self):

        if not self._cookies:
            return []

        httpCookies = []

        for name, cookie in self._cookies.items():
            name = cookie.get('name',None)
            value = cookie.get('value',None)
            domain = cookie.get('domain', '')
            expire = cookie.get('expire', '')
            path = cookie.get('path', '')
            secure = cookie.get('secure', '')
            httponly = cookie.get('httponly', '')
            cookiehttp = [];
            cookiehttp.append('{0}={1}'.format(name,value))

            if domain:
                cookiehttp.append('Domain={0}'.format(domain))
            if expire:
                cookiehttp.append('Max-Age={0}'.format(expire))
            if path:
                cookiehttp.append('Path={0}'.format(path))

            if secure:
                cookiehttp.append('Secure')

            if httponly:
                cookiehttp.append('HttpOnly')

            cookiehttp = ';'.join(cookiehttp);

            httpCookies.append(('Set-Cookie',cookiehttp))

        return httpCookies;

    # 格式化cookie
    # <B> 说明： </B>
    # <pre>
    # 用于http header
    # </pre>
    def parseCookies(self,httpCookieStr):

        http_cookie = str(httpCookieStr)
        if http_cookie:
            http_cookieList = http_cookie.split(';')
            for cookie in http_cookieList:
                cookieItem = cookie.split('=')
                self._cookies[cookieItem[0].strip()] = cookieItem[1]

        return ;

