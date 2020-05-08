# -*- coding: utf-8 -*-
from ..base.Validator import Validator
import re

"""
 * 整型数验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:decimalPoint 整数的位数
 * ['attrs',[['int',{'decimalPoint':2}]],{'message'=>'你输入的值必须为整数'}]
 *</pre>
"""
class IntValidator(Validator):

    def __init__(self,attrs):
        self.decimalPoint = None
        self.pattern = r'^(\d{point})$'
        super().__init__(attrs)

    def validateValue(self,value,name = None):

        if not self.decimalPoint:
            point = '+'
        else:
            point = '{1,' + str(self.decimalPoint) + '}'

        pattern = self.pattern.replace('{point}',point)
        if re.match(pattern,str(value)) is None:
            return False
        else:
            return True