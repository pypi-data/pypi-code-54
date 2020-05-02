from .base_datatype_mapper import BaseDatatypeMapper

class ListMapper(BaseDatatypeMapper):
    def __init__(self, datatype, map_guesser, parse_guesser):
        super(ListMapper, self).__init__(datatype)
        self.map_guesser = map_guesser
        self.parse_guesser = parse_guesser

    def map(self, value):
        """map each v in the value list

        Use the MapGuesser to find the datatype
        Use the datatype's mapper to resolve the value
        """
        mapped = {}
        res = []
        for idx, val in enumerate(value):
            guessed_dt = self.map_guesser.guess(idx, val)
            res.append(guessed_dt.mapper.map(val))
        mapped[self.datatype.condition_type] = res
        return mapped

    def resolve(self, value):
        res = []
        for idx, val in enumerate(value):
            guessed_dt = self.map_guesser.guess(idx, val)
            res.append(guessed_dt.mapper.resolve(val))
        return res

    def parse(self, value):
        res = []
        for idx, val in enumerate(value):
            guessed_dt = self.parse_guesser.guess(idx, val)
            res.append(guessed_dt.mapper.reconstruct(val))
        return res
