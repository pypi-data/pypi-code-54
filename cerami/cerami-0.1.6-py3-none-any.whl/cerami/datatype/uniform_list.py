from .dynamic import List
from .mapper import UniformListMapper

class UniformList(List):
    def __init__(self, datatype, **kwargs):
        super(UniformList, self).__init__(**kwargs)
        self.datatype = datatype
        self.mapper = UniformListMapper(self.datatype.mapper)

    def index(self, idx):
        """return an expression attribute of the inner datatype
        sets the index value on the expression attribute 
        """
        datatype_cls = type(self.datatype)
        dt = datatype_cls(column_name=self.column_name)
        dt._index = idx
        return dt
