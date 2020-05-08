# -*- coding: utf-8 -*-
from ..base.Validator import Validator
from ..utils import CommonUtil

"""
 * in 集合验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['inlist',{'numbers':[1,2,3]}]],{'message'=>'输入的值必须为1,2,3,4'}]
 *</pre>
"""
class InValidator(Validator):

    def __init__(self,attrs):
        self.numbers = []

        super().__init__(attrs)
        self.numbers = CommonUtil.listToStr(self.numbers)

    def validateValue(self,value,name = None):

        self.addParam('numbers', ','.join(self.numbers));
        if str(value) in self.numbers:
            return True
        else:
            return False

