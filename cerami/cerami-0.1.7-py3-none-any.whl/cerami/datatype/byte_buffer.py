from .base_datatype import DynamoDataType
from .mapper import ByteMapper

class ByteBuffer(DynamoDataType):
    def __init__(self, mapper_cls=ByteMapper, **kwargs):
        super(ByteBuffer, self).__init__(mapper_cls=mapper_cls, condition_type="B", **kwargs)
