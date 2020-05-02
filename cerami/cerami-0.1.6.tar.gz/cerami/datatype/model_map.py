from copy import copy
from .base_datatype import DynamoDataType
from .mapper import ModelMapper

class ModelMap(DynamoDataType):
    def __init__(self, model_cls, mapper_cls=ModelMapper, **kwargs):
        super(ModelMap, self).__init__(condition_type="M", mapper_cls=mapper_cls, **kwargs)
        self.model_cls = model_cls
        for column in self.model_cls._columns:
            setattr(self, column.column_name, copy(column))

    def set_column_name(self, val):
        super(ModelMap, self).set_column_name(val)
        for name, attr in self.__dict__.items():
            if isinstance(attr, DynamoDataType):
                new_name = val + "." + name
                attr.set_column_name(new_name)
