# -*- coding: utf-8 -*-
from ..base.Validator import Validator
"""
 * 为空验证器
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attrs',[['empty']],{'message'=>'输入的值必须为空'}]
 × 一般配合!empty 使用,不为空
 *</pre>
"""
class EmptyValidator(Validator):

    def __init__(self,attrs):
        super().__init__(attrs)
        self.skipOnEmpty = False


    def validateValue(self,value,name = None):

        if self.isEmpty(value):
            return True
        else:
            return False