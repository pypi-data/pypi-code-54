# -*- coding: utf-8 -*-
from ..base.Validator import Validator

"""
 * 验证list 元素的值类型
 *<B>说明：</B>
 *<pre>
 * 规则格式:
 * ['attr', [['vlist', {"validators": [["int"]]}]], {'message': 'id 必填,类型正确'}],
 *</pre>
"""
class ListValidator(Validator):

    def __init__(self,attrs):
        self.validators = [];# 验证器
        super().__init__(attrs)

    def validateValue(self,value,name = None):

        result = True;
        for val in value:
            for validatorRule in self.validators:
                validator = self.validation.makeValidator(validatorRule);
                result = validator.validateValue(val,name)
                if result is False:
                    result = False;
                    break;
            if result is False:
                break


        return result;

