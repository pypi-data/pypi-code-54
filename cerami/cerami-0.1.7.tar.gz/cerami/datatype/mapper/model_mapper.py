from .base_datatype_mapper import BaseDatatypeMapper

class ModelMapper(BaseDatatypeMapper):
    def map(self, value):
        mapped = {}
        mapped[self.datatype.condition_type] = value.as_item()
        return mapped

    def resolve(self, value):
        res = {}
        for key, val in value.items():
            column = getattr(self.datatype.model_cls, key)
            res[key] = column.mapper.resolve(val)
        return res

    def parse(self, value):
        """map each k,v in value dict to columns on the Model

        Iterate over all columns on the Model
        Use the columns mapper to reconstruct the value
        Return a new instance of the Model
        """
        data = {}
        model_cls = self.datatype.model_cls
        for column in model_cls._columns:
            try:
                val = value[column.column_name]
            except KeyError:
                continue
            data[column.column_name] = column.mapper.reconstruct(val)
        return model_cls(**data)
