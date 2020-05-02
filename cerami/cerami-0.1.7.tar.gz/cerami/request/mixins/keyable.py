from ..search_attribute import DictAttribute

class Keyable(object):
    def key(self, *expressions):
        """return a new Request setup with the Key attribute"""
        for expression in expressions:
            key_dict = {}
            key_dict[expression.datatype.column_name] = expression.attribute_map()
            self.add_attribute(DictAttribute, 'Key', key_dict)
        return self
