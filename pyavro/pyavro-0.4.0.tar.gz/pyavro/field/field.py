from pydantic import BaseModel, root_validator
from typing import Optional, List, Union, Any
import funcy as fn
from decimal import Decimal


class Field(BaseModel):
    name: str
    type: Any
    default: Optional[Any]

    def _to_avro_type(self):
        type_match = {
            str: 'string',
            None: "null",
            int: 'int',
            float: 'float',
            bytes: 'bytes',
            Decimal: 'decimal'
        }
        new_type = type_match[self.type]
        self.type = new_type
        return self

    @staticmethod
    def check_for_null_in_list(vals):
        if (vals[0] != 'null') or (any(vals[1:]) == "null"):
            raise ValueError("The first index of AvroField(type) must be 'null' if field is nullable")

    @root_validator()
    def type_must_start_with_null_if_nullable(cls, values):
        default = fn.get_in(values, ["default"])
        _type = fn.get_in(values, ["type"])
        if default is None:
            if isinstance(_type, list):
                cls.check_for_null_in_list(_type)
        return values
