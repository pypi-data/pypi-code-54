from .string_mapper import StringMapper
from .base_datatype_mapper import BaseDatatypeMapper

class NumberMapper(BaseDatatypeMapper):
    def resolve(self, value):
        """convert the number into a string"""
        return str(value)

    def parse(self, value):
        """convert the value into an int"""
        return int(value)

