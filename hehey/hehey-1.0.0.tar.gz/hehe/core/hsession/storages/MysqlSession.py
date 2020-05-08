from ..base.WebSession import WebSession
import pymysql
import time;

"""
 * mysql session 会话
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""

class MysqlSession(WebSession):

    def __init__(self,**attrs):

        # 表名
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.tableName = '';

        self.dbconn = None;

        super().__init__(**attrs)

    def _init(self):

        super()._init()
        self.connect()

    # 连接redis 服务
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def connect(self):

        if isinstance(self.dbconn, dict):
            dbconn = self.dbconn.copy();
            # 设置游标返回的数据为字典
            self.dbconn = pymysql.connect(host=dbconn['host'], user=dbconn['user'],
                                          password=dbconn['password'], db=dbconn['dbName'],
                                          port=dbconn['port'], cursorclass=pymysql.cursors.DictCursor)

            # 自动提交
            self.dbconn.autocommit(True)

        return self.dbconn

    # 获取连接
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getConnection(self) -> 'Connection':

        return self.connect()

    def execute(self, sql,sqlParams = []):

        dbconn = self.getConnection();
        cur = None;

        try:
            cur = dbconn.cursor();
            effectRow = cur.execute(sql,sqlParams)  # 执行sql语句
            return effectRow
        except Exception as e:
            if e[0] == '2006':
                # ping mysql ,并自动重连
                self.ping_check()
                cur = self.dbconn.cursor()
                effectRow = cur.execute(sql,sqlParams)  # 执行sql语句
            else:
                # 继续抛出异常
                raise e
        finally:
            if cur is not None:
                cur.close()

        return effectRow;

    def query(self,sql,sqlParams = []):

        dbconn = self.getConnection();
        try:
            cur = dbconn.cursor();
            cur.execute(sql,sqlParams)  # 执行sql语句
            return cur.fetchall()  # 获取查询的所有记录
        except Exception as e:
            if e[0] == '2006':
                # ping mysql ,并自动重连
                self.ping_check()
                cur = dbconn.cursor();
                cur.execute(sql, sqlParams)  # 执行sql语句
            else:
                # 继续抛出异常
                raise e
        finally:
            if cur is not None:
                cur.close()

        return []

    def ping_check(self):

        self.dbconn.ping()

        return;


    def buildExpireDate(self):

        self.getTimeout()
        nowTime = int(time.time())
        expireTime = nowTime + self.getTimeout();

        timeArray = time.localtime(expireTime)
        expireDate = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)

        return expireDate;

    def findSessionBySid(self,sid):

        selectSql = "select * from {0} where id=%s".format(self.tableName);
        sessionRows = self.query(selectSql,[sid])

        if sessionRows:
            return sessionRows[0];
        else:
            return [];

    def _readSession(self,sid):

        sessionRow = self.findSessionBySid(sid)
        if not sessionRow:
            return '';

        sessionData = sessionRow['sessionData']
        if not sessionData:
            sessionData = ''

        return sessionData

    def _writeSession(self,sid,sessionData):

        updateSql = "replace into  {0} (id,sessionData,expire) values(%s,%s,%s)".format(self.tableName)
        self.execute(updateSql,[sid,sessionData,self.buildExpireDate()])

        return True

    def _destroySession(self,sid):

        updateSql = "delete from {0}  where id=%s".format(self.tableName)
        self.execute(updateSql, [sid])

        return True

    def _existSession(self,sid):

        selectSql = "select id,expire from {0} where id=%s".format(self.tableName);
        sessionRows = self.query(selectSql, [sid])
        if not sessionRows:
            return False;

        sessionRow = sessionRows[0];

        if self._checkexpire(sessionRow):
            return True;
        else:
            return False;

    def _checkexpire(self,sessionRow):

        nowTime = int(time.time())
        expire = sessionRow['expire']
        expirestr = expire.strftime("%Y-%m-%D %H:%s:%i")
        expireTime = time.strptime(expirestr, "%Y-%m-%D %H:%s:%i")

        if expireTime > nowTime:
            return True;
        else:
            return False;

