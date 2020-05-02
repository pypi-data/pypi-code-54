from .base_datatype import DynamoDataType
from .mapper import StringMapper

class BaseString(DynamoDataType):
    def __init__(self, mapper_cls=StringMapper, **kwargs):
        super(BaseString, self).__init__(mapper_cls=mapper_cls, condition_type="S", **kwargs)
