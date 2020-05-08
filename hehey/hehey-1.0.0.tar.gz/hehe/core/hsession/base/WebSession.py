from .SessionHandler import SessionHandler
from ..utils import CommonUtil

import time

"""
 * web session 会话基类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""

class WebSession:

    def __init__(self,**attrs):

        # 过期时间
        # <B> 说明： </B>
        # <pre>
        # 单位秒,默认 30 分钟
        # </pre>
        self.timeout = 30 * 60;

        # session 名称
        # <B> 说明： </B>
        # <pre>
        # 一般用于cookie 名称
        # </pre>
        self.name = '';

        # session id 签名秘钥
        # <B> 说明： </B>
        # <pre>
        # cookie session id 与存储的session id 通过加密的方式转换
        # 存在一一对应的关系
        # </pre>
        self.secretKey = '';

        # 存储 session id 前缀
        # <B> 说明： </B>
        # <pre>
        # 最后生成的存储session id 会自动加上此前缀
        # </pre>
        self.keyPrefix = '';

        # cookie session id 参数
        # <B> 说明： </B>
        # <pre>
        # 基本格式请参考cookie 相关设置参数
        # </pre>
        self.cookieParams = {}

        # session 开启的标识
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.sessionStart = False

        # session 初始化标识
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.sessionInit = False

        # session 序列化类型
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.serializer = None;

        # session 事件类型
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.sessionHandler = SessionHandler;

        if attrs:
            CommonUtil.setAttrs(self,attrs)

        self.registerSessionHandler()

    # 开启session
    # <B> 说明： </B>
    # <pre>
    # 读取,更新session 之前,必须先开启session
    # </pre>
    def open(self):

        if self.sessionStart:
            return True

        self.initSessionHandler()
        self.sessionStart = True
        if self.sessionInit is False:
            self._init()
            
        self.sessionHandler.open()

        return ;

    def _init(self):

        self.sessionInit = True

        return ;

    # 关闭session
    # <B> 说明： </B>
    # <pre>
    # 关闭后,session 数据会自动持久化(文件或redis 等等)
    # </pre>
    def close(self):

        self.sessionStart = False
        self.sessionHandler.close()

        return ;

    def getSessionHandler(self):

        return self.sessionHandler

    # 设置session 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def set(self,name,value):

        self.open()

        self.sessionHandler.set(name,value)

        return ;

    # 获取指定名称session 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def get(self,name,defaultValue = None):

        self.open()

        return self.sessionHandler.get(name,defaultValue)

    # 获取全部session 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getSession(self):

        self.open()

        return self.sessionHandler.get()

    # 删除指定名称session 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def detele(self, name):

        self.open()

        return self.sessionHandler.delete(name)

    def setName(self,name):

        self.name = name;

        return self.sessionHandler.setName(self.name)

    def getName(self):

        return self.name

    def setTimeout(self,expire):

        return self.sessionHandler.setTimeout(expire)

    def getTimeout(self):

        self.open()

        return self.sessionHandler.getTimeout()

    def getSessionId(self):

        return self.sessionHandler.getSessionId()

    def setSessionId(self,sessionId):

        return self.sessionHandler.setSessionId(sessionId)

    # 数据是否过期
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # return bool True:已过期,False:未过期
    def expire(self,lasttime):
        # 校验有效期
        nowTime = int(time.time())

        if self.timeout > 0 and nowTime > lasttime + self.timeout:
            # 已过期
            return True
        else:
            return False


    def initSessionHandler(self):

        self.sessionHandler.setName(self.name)
        self.sessionHandler.setTimeout(self.timeout)
        self.sessionHandler.setCookieParams(self.cookieParams)
        self.sessionHandler.setSecretKey(self.secretKey)
        self.sessionHandler.setSerializer(self.serializer)

        return ;

    def registerSessionHandler(self):

        self.sessionHandler = SessionHandler();
        self.sessionHandler.registerHandler(
            self._openSession,
            self._closeSession,
            self._readSession,
            self._writeSession,
            self._destroySession,
            self._gcSession,
            self._existSession
        )

        self.initSessionHandler()

        return ;

    # 存储驱动的开启session 事件
    # <B> 说明： </B>
    # <pre>
    # 存储驱动必实现此接口
    # </pre>
    def _openSession(self):

        return True

    # 存储驱动的关闭session 事件
    # <B> 说明： </B>
    # <pre>
    # 存储驱动必实现此接口
    # </pre>
    def _closeSession(self):

        return True

    # 存储驱动的读取session 事件
    # <B> 说明： </B>
    # <pre>
    # 存储驱动必实现此接口
    # </pre>
    def _readSession(self,sid):

        return ;

    # 存储驱动的写入session 事件
    # <B> 说明： </B>
    # <pre>
    # 存储驱动必实现此接口
    # </pre>
    def _writeSession(self,sid,sessionData):

        return ;

    # 存储驱动的销毁session 事件
    # <B> 说明： </B>
    # <pre>
    # 存储驱动必实现此接口
    # </pre>
    def _destroySession(self,sid):

        return ;

    # 存储驱动的gc 回收session 事件
    # <B> 说明： </B>
    # <pre>
    # 存储驱动必实现此接口
    # </pre>
    def _gcSession(self):

        return ;

    # 存储驱动的验证sid 是否存在事件
    # <B> 说明： </B>
    # <pre>
    # 存储驱动必实现此接口
    # </pre>
    def _existSession(self,sid):

        return ;

