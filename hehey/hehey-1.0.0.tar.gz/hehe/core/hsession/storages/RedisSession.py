from ..base.WebSession import WebSession
from redis import Redis


"""
 * redis session 会话
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""

class RedisSession(WebSession):

    def __init__(self,**attrs):

        self.red = Redis;

        super().__init__(**attrs)

    def _init(self):

        super()._init()
        self.connect()

    def connect(self):

        if isinstance(self.red,dict):
            self.red = Redis(**self.red)

        return ;

    # 构建保存路径
    def buildRedisKey(self,sid = ''):

        if sid:
            sessionRedisKey = "{0}{1}".format(self.keyPrefix,sid)
        else:
            sessionRedisKey = "{0}{1}".format(self.keyPrefix,self.sessionHandler.getSid())

        return sessionRedisKey

    def _readSession(self,sid):

        sessionRedisKey = self.buildRedisKey(sid);
        sessionData = self.red.get(sessionRedisKey)
        if sessionData:
            sessionData = sessionData.decode()
        else :
            sessionData = ''

        return sessionData

    def _writeSession(self,sid,sessionData):

        sessionRedisKey = self.buildRedisKey(sid);
        self.red.setex(sessionRedisKey,self.getTimeout(),sessionData)

        return True

    def _destroySession(self,sid):

        sessionRedisKey = self.buildRedisKey(sid);
        self.red.delete(sessionRedisKey)

        return True

    def _existSession(self,sid):

        essionRedisKey = self.buildRedisKey(sid);
        if self.red.exists(essionRedisKey):
            return True
        else:
            return False

