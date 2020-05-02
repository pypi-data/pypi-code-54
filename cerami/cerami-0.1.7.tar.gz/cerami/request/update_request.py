from .mixins import BaseRequest, Keyable, Returnable
from ..response import SaveResponse
from ..datatype.expression import (
    UpdateRemoveExpression,
    EqualityExpression)
from .search_attribute import (
    DictAttribute,
    UpdateAction,
    UpdateExpressionAttribute)


class UpdateRequest(BaseRequest, Keyable, Returnable):
    def execute(self):
        response = self.client.update_item(**self.build())
        return SaveResponse(response, self.reconstructor)

    def set(self, *expressions):
        for expression in expressions:
            self.update_expression('SET', expression)
        return self

    def remove(self, *datatypes):
        for datatype in datatypes:
            expression = UpdateRemoveExpression(datatype)
            self.update_expression('REMOVE', expression)
        return self

    def add(self, datatype, value):
        expression = EqualityExpression('', datatype, value)
        return self.update_expression('ADD', expression)

    def delete(self, datatype, value):
        expression = EqualityExpression('', datatype, value)
        return self.update_expression('DELETE', expression)

    def update_expression(self, action, expression):
        """perform the steps for UpdateExpression"""
        name = {}
        name[expression.expression_attribute_name] = expression.datatype.column_name
        self.add_attribute(UpdateExpressionAttribute,
                           'UpdateExpression',
                           UpdateAction(action, expression))
        self.add_attribute(DictAttribute,
                           'ExpressionAttributeNames',
                           name)
        self.add_attribute(DictAttribute,
                           'ExpressionAttributeValues',
                           expression.value_dict())
        return self
