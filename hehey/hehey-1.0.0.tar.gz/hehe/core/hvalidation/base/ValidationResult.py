# -*- coding: utf-8 -*-

"""
 * 验证结果类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""

class ValidationResult(object):

    def __init__(self):

        # 验证器验证结果列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.validatorResults  = []

        # 错误列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.errors = [];

        return ;

    # 解析最终验证结果
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    # param validateResultList 验证结果对象列表
    def getResult(self):

        if hasattr(self,'_validResult'):

            return getattr(self,'_validResult')

        validResult = True
        for validateResult in self.validatorResults:
            if validateResult.getResult() == False:
                validResult = False
                self.addError(validateResult.getMessage())

        setattr(self,'_validResult',validResult)

        return validResult;


    def addValidatorResult(self,validatorResult):

        self.validatorResults.append(validatorResult)

        return ;

        # 获取第一个错误消息
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>

    def getFirstError(self):

        if self.errors:
            return self.errors[0];
        else:
            return '';

        # 添加错误消息
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>

    def addError(self, message=''):

        self.errors.append(message)

        return;

        # 获取所有错误消息
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>

    def getErrors(self):

        return self.errors

