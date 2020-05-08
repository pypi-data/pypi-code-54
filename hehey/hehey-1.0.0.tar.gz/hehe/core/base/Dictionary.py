from hehe.helper.ArrayHelper import ArrayHelper
from hehe.helper.ClassHelper import ClassHelper
"""
 * 字典基类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
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
class BaseDictionary():

    def __getattr__(self, dictname):

        def _func(*arg, **kwargs):

            funName = _func.func_name;
            dictfuncname = '';
            if funName[0:3] == 'map':
                dictfuncname = ClassHelper.lcfirst(funName[3:]);
                funcMeta = getattr(self, dictfuncname)
                return ArrayHelper.map(funcMeta(), "id", "name")
            elif funName[0:6] == 'column':
                dictfuncname = ClassHelper.lcfirst(funName[6:]);
                funcMeta = getattr(self, dictfuncname)
                return ArrayHelper.getColumn(funcMeta(), "id")
            elif funName[0:5] == 'index':
                dictfuncname = ClassHelper.lcfirst(funName[5:]);
                funcMeta = getattr(self, dictfuncname)
                return ArrayHelper.index(funcMeta(), "id")
            else:
                dictfuncname = funName
                funcMeta = getattr(self, dictfuncname)
                return funcMeta();

            return ;

        _func.func_name = dictname

        return _func




