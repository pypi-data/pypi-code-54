# -*- coding: utf-8 -*-
import importlib,inspect,random,time,hashlib
import collections
from .JsonEncoder import JsonEncoder
import json
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('安全伪随机数生成器不可用')
    using_sysrandom = False

"""
 * 类帮助类
 *<B>说明：</B>
 *<pre>
 *  提供基本类操作,获取属性值,设置属性等等
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
class ArrayHelper:

    # 获取字典值
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    @classmethod
    def getValue(cls,array:dict, key:str = '', default = None):

        if key in array.keys():
            return array.get(key,default);

        pos = key.find('.')
        if pos != -1:
            myarray = cls.getValue(array,key[0:pos],default);
            return myarray.get(key[pos - 1:], default);

        return default;

    # 返回list 字典某列表的值集合
    # <B> 说明： </B>
    # <pre>
    # datas = [
    #      {"id":"1",'cat':1,"name":"111"},
    #      {"id": "2",'cat':2, "name": "222"},
    #      {"id": "3", 'cat': 2, "name": "333"}
    # ];
    # data = ArrayHelper.getColumn(datas,"id");
    # result is:
    # ['1', '2', '3']
    # </pre>
    @classmethod
    def getColumn(cls,array:dict, key:str = ''):

        result = [];

        for element in array:
            value = cls.getValue(element, key)
            result.append(value)

        return result;

    # 返回list 字典某列表的值集合
    # <B> 说明： </B>
    # <pre>
    # datas = [
    #      {"id":"1",'cat':1,"name":"111"},
    #      {"id": "2",'cat':2, "name": "222"},
    #      {"id": "3", 'cat': 2, "name": "333"}
    # ];
    # data = ArrayHelper.index(datas,"id");
    # result is:
    # OrderedDict([('1', {'cat': 1, 'name': '111', 'id': '1'}), ('2', {'cat': 2, 'name': '222', 'id': '2'}), ('3', {'cat': 2, 'name': '333', 'id': '3'})])
    # </pre>
    @classmethod
    def index(cls, array: dict, key: str = ''):

        result = collections.OrderedDict();

        for element in array:
            itemKey = cls.getValue(element, key)
            result[str(itemKey)] = element

        return result;


    # list 字典转成固定格式
    # <B> 说明： </B>
    # <pre>
    # datas = [
    #      {"id":"1",'cat':1,"name":"111"},
    #      {"id": "2",'cat':2, "name": "222"},
    #      {"id": "3", 'cat': 2, "name": "333"}
    # ];
    # data = ArrayHelper.map(datas,"id","name");
    # result is:
    # {'3': '333', '2': '222', '1': '111'}
    #
    # data = ArrayHelper.map(datas,"id","name",'cat');
    # result is:
    # {'2': {'2': '222', '3': '333'}, '1': {'1': '111'}}
    # </pre>
    @classmethod
    def map(cls,array, fromKey,toKey , group = None):

        result = collections.OrderedDict({});
        for element in array:
            key = cls.getValue(element,fromKey)
            value = cls.getValue(element, toKey)

            if group:
                groupKey = str(cls.getValue(element, group))
                item = result.get(groupKey,{})
                item[str(key)] = value
                result[groupKey] = item;
            else:
                result[str(key)] = value;

        return result

    @classmethod
    def jsondumps(cls,data):

        return json.dumps(data,cls=JsonEncoder)

    @classmethod
    def jsonloads(cls,json):

        return json.loads(json)

    @classmethod
    def jsonload(cls, json):

        return json.load(json)
