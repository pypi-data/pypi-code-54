from ..search_attribute import (
    DictAttribute,
    QueryExpressionAttribute)

class Filterable(object):
    """A mixin to add the filter method"""

    def filter(self, *expressions):
        """return a new Request setup with filter attributes

        FilterExpression, ExpressionAttributeNames, ExpressionAttributeValues
        are all required to filter properly
        """
        for expression in expressions:
            names = {}
            names[expression.expression_attribute_name] = expression.datatype.column_name
            self.add_attribute(
                QueryExpressionAttribute,
                'FilterExpression',
                expression)
            self.add_attribute(
                DictAttribute,
                'ExpressionAttributeNames',
                names)
            self.add_attribute(
                DictAttribute,
                'ExpressionAttributeValues',
                expression.value_dict())
        return self
