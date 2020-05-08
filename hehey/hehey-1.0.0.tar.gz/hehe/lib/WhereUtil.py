
from hehe import he

"""
 * sql where 工具
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
 *</pre>
"""
class WhereUtil():

    # 获取当前route pathinfo
    # <B> 说明： </B>
    # <pre>
    # 不带参数
    # </pre
    @classmethod
    def toWhere(cls,datas = {},rules = []):

        where = {};

        for rule in rules:

            name = rule.get("name",None);
            if name is None:
                continue

            field = rule.get("field",name)

            emtpy = rule.get("emtpy", 'emtpy')
            value = datas.get(name,None)
            emtpyFunc = getattr(cls,'_{0}'.format(emtpy))
            if not emtpyFunc:
                continue;

            if emtpyFunc(value):
                continue;

            operator = rule.get("op", '=')
            if operator == '=':
                where[field] = value
            else:
                where[field] = [operator,value]

        return where;

    # 判断值为空
    # <B> 说明： </B>
    # <pre>
    # '',[],{},0 等至为空
    # </pre
    @classmethod
    def _emtpy(cls,value):

        if not value:
            return True
        else:
            return False

    @classmethod
    def _str(cls,value):

        if value is None or str(value) == '':
            return True
        else:
            return False;

    @classmethod
    def _int(cls,value):

        if value is None or value == '' or int(value) == 0:
            return True
        else:
            return False;







