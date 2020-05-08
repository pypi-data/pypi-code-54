
from itsdangerous import BadSignature, URLSafeTimedSerializer
import hashlib
import json
import datetime

"""
 * session 序列化
 *<B>说明：</B>
 *<pre>
 *  用于加密session id
 * 序列化session 数据
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
class SafeSerializer:

    salt = 'cookie-session'
    digestMethod = staticmethod(hashlib.sha1)
    keyDerivation = 'hmac'

    def __init__(self,secretKey):

        self.secretKey = secretKey;

    def dumpsSessid(self,sid):

        serializer = self.getSerializer()
        return serializer.dumps(sid)

    def loadsSessid(self,sessid):

        serializer = self.getSerializer()
        return serializer.loads(sessid)

    def serializeSession(self,sessionData):

        if sessionData:
            return json.dumps(sessionData,cls=JsonEncoder)
        else:
            return ''

    def unSerializeSession(self,sessionData):

        if not sessionData:
            return {}

        return json.loads(sessionData)

    # 获取签名对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # return bool True:已过期,False:未过期
    def getSerializer(self)->'URLSafeTimedSerializer':

        if not self.secretKey:
            return None

        signer_kwargs = dict(
            key_derivation=self.keyDerivation,
            digest_method=self.digestMethod
        )

        return URLSafeTimedSerializer(self.secretKey, salt=self.salt,
                                      signer_kwargs=signer_kwargs)


class JsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)