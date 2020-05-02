from .base_datatype_mapper import BaseDatatypeMapper

class UniformListMapper(BaseDatatypeMapper):
    def __init__(self, mapper):
        self.mapper = mapper
        self.condition_type = "L"

    def resolve(self, value):
        return [self.mapper.map(i) for i in value]

    def parse(self, value):
        return [self.mapper.reconstruct(i) for i in value]
