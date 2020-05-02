from .base_datatype import DynamoDataType
from .mapper import SetMapperDecorator

class Set(DynamoDataType):
    def __init__(self, datatype, **kwargs):
        super(Set, self).__init__(**kwargs)
        self.datatype = datatype
        self.mapper = SetMapperDecorator(self.datatype.mapper)
        self.condition_type = self.datatype.condition_type + "S"
