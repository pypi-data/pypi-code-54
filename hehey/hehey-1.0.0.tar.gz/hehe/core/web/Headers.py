
"""
 * http 头部信息对象
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
class Headers:

    def __init__(self):

        self._headers = {}

    # 获取全部headers 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getHeaders(self):

        return self._headers

    # 设置headers 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setHeaders(self,headers):

        self._headers = headers

        return ;

    # 设置header 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def set(self,name,value):

        name = self.formatName(name);
        self._headers[name] = [value]

        return ;

    def __iter__(self):
        return self._headers


    def __getitem__(self,name):

        name = self.formatName(name);

        return self._headers.get(name,None)

    # 获取header 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def get(self,name,defaultValue = None):

        name = self.formatName(name);

        return self._headers.get(name,defaultValue)

    # 追加header 值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def append(self,name,value):

        name = self.formatName(name);
        valueList = self._headers.get(name,None)

        if valueList is None:
            valueList = [value]
        else:
            valueList.append(value)

        self._headers[name] = valueList

        return ;

    # 是否存在header
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def has(self,name):
        name = self.formatName(name);
        valueList = self._headers.get(name, None)
        if valueList is None:
            return False
        else:
            return True

    # 删除header
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def remove(self,name):
        name = self.formatName(name);
        self._headers.pop(name)

        return ;

    # 删除全部header
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def removeAll(self):

        self._headers = {};

        return ;

    # 计算headers长度
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getCount(self):

        return len(self._headers)

    def formatName(self,name):

        return name.lower()

    # 格式化header
    # <B> 说明： </B>
    # <pre>
    # 用于http header
    # </pre>
    def formatHeaders(self):

        headerList = []

        if self._headers:
            for name,value in self._headers.items():
                if isinstance(value,list):
                    headerList.append((name,','.join('%s' % val for val in value)))
                else:
                    headerList.append((name,value))

        return headerList;