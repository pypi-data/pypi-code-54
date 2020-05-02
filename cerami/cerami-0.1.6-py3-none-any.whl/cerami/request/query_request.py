from .mixins import BaseRequest, Filterable, Keyable, Projectable, Limitable
from ..response import SearchResponse
from .search_attribute import (
    SearchAttribute,
    DictAttribute,
    QueryExpressionAttribute)

class QueryRequest(
        BaseRequest,
        Filterable,
        Keyable,
        Projectable,
        Limitable):
    def execute(self):
        response = self.client.query(**self.build())
        return SearchResponse(response, self.reconstructor)

    def index(self, index_name):
        """add IndexName to the request"""
        self.add_attribute(SearchAttribute, 'IndexName', index_name)
        return self

    def key(self, *expressions):
        """return a new SearchInterface setup with query attributes
        KeyConditionExpression, ExpressionAttributeNames,
        ExpressionAttributeValues are all required to query properly

        This completely overrides the implementation of Keyable
        but is defined as such for a simpler interface to remember.
        """
        for expression in expressions:
            names = {}
            names[expression.expression_attribute_name] = expression.datatype.column_name
            self.add_attribute(
                QueryExpressionAttribute,
                'KeyConditionExpression',
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
