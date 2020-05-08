from ..base.WebSession import WebSession
import os

"""
 * web session 会话基础
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""

class FileSession(WebSession):

    def __init__(self,**attrs):

        self.savepath = '/tmp';

        super().__init__(**attrs)

    # 构建保存路径
    def buildSavepath(self,sid = ''):

        if sid:
            savepath = self.savepath + '/' + "{0}{1}".format(self.keyPrefix,sid)
        else:
            savepath = self.savepath + '/' +  "{0}{1}".format(self.keyPrefix,self.sessionHandler.getSid())

        return savepath


    def _readSession(self,sid):

        sesspath = self.buildSavepath(sid);
        if not os.path.exists(sesspath):
            return '';

        # 判断有效期
        sesspathStat = os.stat(sesspath)
        lastUptime = int(sesspathStat.st_mtime)
        if self.expire(lastUptime):
            return ''

        sessionData = ''
        with open(sesspath, 'r') as f:
            sessionData = f.read()

        return sessionData

    def _writeSession(self,sid,sessionData):

        sesspath = self.buildSavepath(sid);
        with open(sesspath, 'w') as f:
            f.write(sessionData)

        return True

    def _destroySession(self,sid):

        sesspath = self.buildSavepath(sid);
        os.remove(sesspath)

        return True


    def _existSession(self,sid):

        sesspath = self.buildSavepath(sid);
        if os.path.exists(sesspath):
            return True
        else:
            return False

