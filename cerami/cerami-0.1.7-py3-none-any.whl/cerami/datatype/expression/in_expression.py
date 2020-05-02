from .base_expression import BaseExpression

class InExpression(BaseExpression):
    """
    Generate an IN expression

    Email.scan.filter(Email.generated_email.in_("test@test.com"))
    ---
    dynamodb scan \
        --table-name "Emails" \
        --filter-expression "generated_email IN (:email1)" \
        --expression-attribute-values '{":email1": {"S": "test@test.com"}}'


    so i need to keep the expression-attribute-values the exact same:
        value_dict() needs to just call super for each one?

    """
    def __init__(self, datatype, value):
        super(InExpression, self).__init__('IN', datatype, value)
        self.expression_attribute_values = self._build_expression_attribute_values()

    def __str__(self):
        value_names = ', '.join([k for k,v in self.value_dict().items()])
        attr_name = self.expression_attribute_name
        if hasattr(self.datatype, '_index'):
            attr_name = "{}[{}]".format(attr_name, self.datatype._index)
        return "{attr_name} {expression} ({value_names})".format(
            attr_name=attr_name,
            expression=self.expression,
            value_names=value_names)

    def value_dict(self):
        return self.expression_attribute_values

    def _build_expression_attribute_values(self):
        column_name_safe = self.datatype.column_name.replace('.', '_')
        res = {}
        for v in self.value:
            value_name = self._generate_variable_name(column_name_safe)
            value_mapped = self.datatype.mapper.map(v)
            res[value_name] = value_mapped
        return res
