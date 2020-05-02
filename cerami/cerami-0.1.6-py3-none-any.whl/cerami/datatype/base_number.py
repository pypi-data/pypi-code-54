from .base_datatype import DynamoDataType
from .mapper import NumberMapper
from .expression import ArithmeticExpression

class BaseNumber(DynamoDataType):
    def __init__(self, mapper_cls=NumberMapper, **kwargs):
        super(BaseNumber, self).__init__(mapper_cls=mapper_cls, condition_type="N", **kwargs)

    def add(self, value):
        return ArithmeticExpression('+', self, value)

    def subtract(self, value):
        return ArithmeticExpression('-', self, value)
