# -*- coding: utf-8 -*-
from ..base.Validator import Validator

"""
 * 相等验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['eq',{number':6}]],{'message'=>'请输入一个等于6的值'}]
 * operator:大于(gt),大于等于(egt),小于(lt),小于等于(elt)
 *</pre>
"""
class EqualValidator(Validator):

    def __init__(self,attrs):
        self.number = 0
        self.operator = '=='
        self.operatorList = ['==','==']

        super().__init__(attrs)

    def validateValue(self,value,name = None):
        self.addParam('number',self.number);

        if self.operator not in self.operatorList:
            return False

        result = False

        if self.operator == '==':
            # 大于
            result = (str(value) == str(self.number))
        elif self.operator == '===':
            # 大于等于
            result = (value is self.number)
        else:
            pass

        return result