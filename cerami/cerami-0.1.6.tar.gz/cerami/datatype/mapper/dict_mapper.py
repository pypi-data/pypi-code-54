from .base_datatype_mapper import BaseDatatypeMapper

class DictMapper(BaseDatatypeMapper):
    def __init__(self, datatype, map_guesser, parse_guesser):
        """initialize the DictMapper
        takes in an additional datatype_guesser
        so it has a way to assigning mapped values
        """
        super(DictMapper, self).__init__(datatype)
        self.map_guesser = map_guesser
        self.parse_guesser = parse_guesser

    def resolve(self, value):
        """map each k,v in the value dict

        Use the MapGuesser to find the datatype
        Use the datatype's mapper to resolve the value
        """
        res = {}
        for key, val in value.items():
            guessed_dt = self.map_guesser.guess(key, val)
            res[key] = guessed_dt.mapper.map(val)
        return res

    def parse(self, value):
        """map each k,v in the value dict

        Use the ParseGuesser to find the datatype
        User the datatype's reconstructor to parse the value
        """
        res = {}
        data = value[self.datatype.condition_type]
        for key, nested_dict in data.items():
            guessed_dt = self.parse_guesser.guess(key, nested_dict)
            res[key] = guessed_dt.mapper.reconstruct(nested_dict)
        return res
