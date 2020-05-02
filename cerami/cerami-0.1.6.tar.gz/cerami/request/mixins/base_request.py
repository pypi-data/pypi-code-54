from copy import copy
from ...reconstructor import RawReconstructor
from ..search_attribute import SearchAttribute

class BaseRequest(object):
    """The Base Class for all requests

    It provides the default constructor and methods for building
    requests.
    """

    def __init__(self, client, tablename="", request_attributes=None, reconstructor=None):
        """constructor for base request"""
        self.request_attributes = copy(request_attributes or {})
        self.client = client
        self.reconstructor = reconstructor or RawReconstructor()
        if tablename:
            self.add_attribute(SearchAttribute, 'TableName', tablename)

    def __str__(self):
        return self.build().__str__()

    def add_attribute(self, attr_class, name, value):
        """add a search attribute to a duplicated instance
        @param attr_class - a SearchAttribute class
        @param name - the name of the attribute
        @param value - the value that will be added to the SearchAttribute
        """
        request_attribute = self.request_attributes.get(name, attr_class(name))
        request_attribute.add(value)
        self.request_attributes[name] = request_attribute

    def build(self):
        """build the dict used by dynamodb"""
        return dict((k, v.build()) for k, v in self.request_attributes.items())

