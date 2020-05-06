from django.contrib.postgres.fields import JSONField
from django.db.models import F, CharField, Expression
from django.db.models.constants import LOOKUP_SEP
from django.utils.deconstruct import deconstructible


class ForceColumn(Expression):
    """
    Represents the SQL of a column name without the table name.

    This variant of Col doesn't include the table name (or an alias) to
    avoid a syntax error in check constraints.
    """
    contains_column_references = True

    def __init__(self, target, output_field=None):
        if output_field is None:
            output_field = target
        super().__init__(output_field=output_field)
        self.target = target

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.target)

    def as_sql(self, compiler, connection):
        return self.target.db_column, []

    def get_group_by_cols(self):
        return [self]

    def get_db_converters(self, connection):
        if self.target == self.output_field:
            return self.output_field.get_db_converters(connection)
        return (
                self.output_field.get_db_converters(connection) +
                self.target.get_db_converters(connection)
        )


@deconstructible
class ForceF(F):
    model = None
    json_field = None

    def __init__(self, model, name, json_field):
        super(ForceF, self).__init__(name)
        self.model = model
        self.json_field = json_field

    def resolve_expression(self, query=None, allow_joins=True, reuse=None,
                           summarize=False, for_save=False, simple_col=False):
        _field_ref = self.json_field + 's.' + self.name.replace(LOOKUP_SEP, '.')
        path, final_field, targets, rest = query.names_to_path(
            [self.json_field], query.get_meta(), query.get_initial_alias())
        if not isinstance(final_field, JSONField):
            raise Exception('`ForeF` only available for JSON Fields')
        _dummy_field = CharField(db_column=_field_ref, name=_field_ref)
        _dummy_field.model = self.model
        return ForceColumn(_dummy_field, _dummy_field)
