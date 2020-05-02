import numbers
from .number import Number
from .string import String
from .set import Set
from .base_datatype import DynamoDataType
from .expression import ListAppendExpression
from .mapper import (
    DictMapper,
    ListMapper)

class DefaultMapGuesser(object):
    def guess(self, key, value):
        """guess the datatype from the value
        Guessing for mapping means we are trying to figure out the datatype
        in order to convert it into a dict usable by dynamodb. So this
        guesser will makes its guess based on value directly
        """
        if isinstance(value, numbers.Number):
            return Number()
        elif isinstance(value, dict):
            return Map()
        elif isinstance(value, list):
            return List()
        else:
            return String()


class DefaultParseGuesser(object):
    def guess(self, key, value):
        """guess the datatype from the key within value
        we are guessing on something like {'M': {'test': {'S': 'hello'}}}
        where key is 'test' and value is {'S': 'hello'}
        this will fetch the inner key ('S') and guess from this value
        """
        attr_key = list(value)[0]
        if attr_key == "N":
            return Number()
        elif attr_key == "S":
            return String()
        elif attr_key == "SS":
            return Set(String())
        elif attr_key == "NS":
            return Set(Number())
        elif attr_key == "L":
            return List()
        elif attr_key == "M":
            return Map()
        else:
            return String()


class Map(DynamoDataType):
    def __init__(
            self,
            map_guesser=None,
            parse_guesser=None,
            **kwargs):
        super(Map, self).__init__(condition_type="M", **kwargs)
        self.map_guesser = map_guesser or DefaultMapGuesser()
        self.parse_guesser = parse_guesser or DefaultParseGuesser()
        self.mapper = DictMapper(self, self.map_guesser, self.parse_guesser)

    def key(self, datatype, key):
        column_name = self.column_name + "." + key
        return type(datatype)(column_name=column_name)


class List(DynamoDataType):
    def __init__(
            self,
            map_guesser=None,
            parse_guesser=None,
            **kwargs):
        super(List, self).__init__(condition_type="L", **kwargs)
        self.map_guesser = map_guesser or DefaultMapGuesser()
        self.parse_guesser = parse_guesser or DefaultParseGuesser()
        self.mapper = ListMapper(self, self.map_guesser, self.parse_guesser)

    def append(self, array):
        if not isinstance(array, list):
            array = [array]
        return ListAppendExpression(self, array)

    def index(self, idx, datatype_cls):
        """return an expression attribute of the inner datatype
        sets the index value on the expression attribute 
        """
        dt = datatype_cls(column_name=self.column_name)
        dt._index = idx
        return dt
