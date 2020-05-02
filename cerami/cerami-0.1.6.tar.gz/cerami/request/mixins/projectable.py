from ..search_attribute import (
    DictAttribute,
    ProjectionExpressionAttribute)
from ...datatype.expression import BaseExpression

class Projectable(object):
    """A mixin to add the project method"""

    def project(self, *datatypes_or_expressions):
        """return a new Request setup with project attributes

        ProjectionExpression, ExpressionAttributeNames

        The args can be an array of datatypes or expressions because projecting 
        allows for list index expressions
        """
        for val in datatypes_or_expressions:
            names = {}
            if hasattr(val, 'expression_attribute_name'):
                expr = val
                names[expr.expression_attribute_name] = expr.datatype.column_name
            else:
                expr = BaseExpression('', val, None)
                names[expr.expression_attribute_name] = val.column_name
            self.add_attribute(
                ProjectionExpressionAttribute,
                'ProjectionExpression',
                expr)
            self.add_attribute(
                DictAttribute,
                'ExpressionAttributeNames',
                names)
