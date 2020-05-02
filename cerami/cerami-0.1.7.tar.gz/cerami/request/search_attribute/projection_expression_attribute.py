from .search_attribute import SearchAttribute

class ProjectionExpressionAttribute(SearchAttribute):
    def __init__(self, name, value=None):
        value = value or []
        super(ProjectionExpressionAttribute, self).__init__(name, value)
    def add(self, expression):
        self.value.append(expression)

    def build(self):
        return ', '.join(str(expr) for expr in self.value)
