from .base_datatype_mapper import BaseDatatypeMapper

class ByteMapper(BaseDatatypeMapper):
    def resolve(self, value):
        return self._encode(value)

    def parse(self, value):
        return self._encode(value)

    def _encode(self, value):
        """try to encode it or return the value (meaning its already encoded"""
        try:
            return value.encode('utf-8')
        except AttributeError:
            return value
