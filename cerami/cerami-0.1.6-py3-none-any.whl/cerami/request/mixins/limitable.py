from ..search_attribute import SearchAttribute

class Limitable(object):
    """A mixin to add the limit method"""

    def limit(self, limit_number):
        """return a new Request setup with the limit attribute"""
        self.add_attribute(
            SearchAttribute,
            'Limit',
            limit_number)
