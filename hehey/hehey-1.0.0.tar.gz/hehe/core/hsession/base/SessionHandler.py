from .SafeSerializer import SafeSerializer

from ..utils import CommonUtil

"""
 * session 会话类
 *<B>说明：</B>
 *<pre>
 * 略
 *</pre>
"""

class SessionHandler:

    def __init__(self,session_id = ''):

        # session 有效期
        # <B> 说明： </B>
        # <pre>
        # 单位秒
        # </pre>
        self.timeout = 60 * 30;

        # session 名称
        # <B> 说明： </B>
        # <pre>
        # 单位秒
        # </pre>
        self.name = None

        # session 名称
        # <B> 说明： </B>
        # <pre>
        # 单位秒
        # </pre>
        self.secretKey = '';

        # session id
        # <B> 说明： </B>
        # <pre>
        # cookie session id
        # </pre>
        self.session_id = session_id

        # session 存储的id
        # <B> 说明： </B>
        # <pre>
        # 用于读取,存储session 数据的key
        # </pre>
        self.sid = '';

        # 序列化类行
        # <B> 说明： </B>
        # <pre>
        # 可自定义
        # </pre>
        self.serializer = SafeSerializer;

        # 安全签名对象
        # <B> 说明： </B>
        # <pre>
        # 用于读取,存储session 数据的key
        # </pre>
        self.safeSerializer = None;

        # cookie 参数
        # <B> 说明： </B>
        # <pre>
        # 单位秒
        # </pre>
        self.cookie_params = {}

        # session 事件
        # <B> 说明： </B>
        # <pre>
        # 单位秒
        # </pre>
        self.handlers = {}

        # session 数据
        # <B> 说明： </B>
        # <pre>
        # 单位秒
        # </pre>
        self.sessionData = {}

        # session 启动状态
        # <B> 说明： </B>
        # <pre>
        # 单位秒
        # </pre>
        self.sessionOpenStatus = False;

        # 是否更新过session 值
        # <B> 说明： </B>
        # <pre>
        # 用于判断关闭session后,是否需要存储session
        # </pre>
        self.updateSession = False

        pass


    def set(self,name,value):

        self.sessionData[name] = value

        self.updateSession = True;

    def delete(self,name):

        try :
            self.sessionData.pop(name)
        except KeyError as keyerror:
            pass

        self.updateSession = True;

    def get(self,name = '',defaultValue = None):

        if name:
            return self.sessionData.get(name,defaultValue)
        else:
            return self.sessionData

    def registerHandler(self,open, close, read, write, destroy, gc,exist):

        self.handlers = {
            'open': open,
            'close': close,
            'read': read,
            'write': write,
            'destroy': destroy,
            'gc': gc,
            'existSession':exist,
        }

        pass


    def _init(self):

        if not self.session_id:
            self.sid = self.buildSessionId()
            self.session_id = self.getSafeSerializer().dumpsSessid(self.sid);

        if not self.sid:
            self.sid = self.getSafeSerializer().loadsSessid(self.session_id)

        return ;


    def openStatus(self):

        return self.sessionOpenStatus

    def setName(self,name):

        self.name = name

        return;

    def setSecretKey(self,secretKey):

        self.secretKey = secretKey

    def getName(self):

        return self.name

    def setTimeout(self,expire):

        self.timeout = expire

        return;

    def getTimeout(self):

        return self.timeout


    def getSessionId(self):

        return self.session_id

    def setSessionId(self,session_id):

        self.session_id = session_id

        return ;

    def setSerializer(self,serializer):

        self.serializer = serializer

        return;

    def getSid(self):

        return self.sid


    def getSafeSerializer(self)->'SafeSerializer':

        if self.safeSerializer is None:
            if isinstance(self.serializer,str):
                serializer = CommonUtil.getClassMeta(self.serializer)
            else:
                serializer = self.serializer

            if not serializer:
                serializer = SafeSerializer

            self.safeSerializer = serializer(self.secretKey)

        return  self.safeSerializer;

    def setCookieParams(self,cookies):

        self.cookie_params = cookies

    def buildHttpCookie(self):

        cookie = self.cookie_params.copy();
        cookie['name'] = self.name
        cookie['expire'] = self.timeout
        cookie['value'] = self.getSessionId()
        path = cookie.get('path','/');
        cookie['path'] = path

        return cookie

    def open(self):

        self.sessionOpenStatus = True

        self._init()
        # 开启
        openFunc = self.handlers.get('open')
        if openFunc():
            self.read();

        return ;

    def close(self):

        closeFunc = self.handlers.get('close')
        if closeFunc():
            self.write()

        return ;

    def read(self):

        readFunc = self.handlers.get('read')
        sessionData = readFunc(self.getSid())
        self.sessionData = self.getSafeSerializer().unSerializeSession(sessionData);

        return;

    def write(self):

        if self.updateSession:
            writeFunc = self.handlers.get('write')
            writeFunc(self.getSid(),self.getSafeSerializer().serializeSession(self.sessionData))

        return;

    def destroy(self):

        destroyFunc = self.handlers.get('destroy')
        destroyFunc(self.getSid())

        return ;

    def gc(self):

        return ;

    # 生成session id
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildSessionId(self):

        sid = ''
        while(True):
            sid = CommonUtil.buildRandomString();
            if not self.existSession(sid):
                return sid
        return;

    # 验证session id 是否有效
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def existSession(self,sid):

        existSessionFunc = self.handlers.get('existSession')
        if existSessionFunc:
            return existSessionFunc(sid)
        else:
            return True
