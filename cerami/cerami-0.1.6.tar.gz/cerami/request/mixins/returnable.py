from ..search_attribute import SearchAttribute

class Returnable(object):
    def returns(self, value):
        self.add_attribute(
            SearchAttribute,
            'ReturnValues',
            value)
        return self
