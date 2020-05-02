from .expression import (
    EqualityExpression,
    InExpression)

class DynamoDataType(object):
    """Abstract class for all DataTypes
    class variable defined. It is used for querying to
    determine what type of attribute is being searched upon
    """
    def __init__(
            self,
            default=None,
            column_name="",
            condition_type="",
            mapper_cls=None):
        self.default = default
        self.set_column_name(column_name)
        self.condition_type = condition_type
        self.mapper = mapper_cls(self) if mapper_cls else None

    def eq(self, value):
        return EqualityExpression("=", self, value)

    def neq(self, value):
        return EqualityExpression("<>", self, value)

    def gt(self, value):
        return EqualityExpression(">", self, value)

    def gte(self, value):
        return EqualityExpression(">=", self, value)

    def lt(self, value):
        return EqualityExpression("<", self, value)

    def lte(self, value):
        return EqualityExpression("<=", self, value)

    def in_(self, *values):
        return InExpression(self, values)

    def set_column_name(self, val):
        self.column_name = val

    def build(self, val):
        """set the value to val or default if present

        building is called automatically by the DynamoDataAttribute
        when the model is initialized.
        """
        if val is None:
            return self._get_default(val)
        return val

    def _get_default(self, val=None):
        if self.default:
            if callable(self.default):
                return self.default()
            else:
                return self.default
        return None
