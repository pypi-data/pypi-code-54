from django.db.models.constants import LOOKUP_SEP
from django.db.models.sql.datastructures import BaseTable


class JsonbFunction:
    JSONB_TO_RECORDSET = ("jsonb_to_recordset", '#>')


class JsonbFunctionTable(BaseTable):
    jsonb_join_type = ("JOIN LATERAL", "ON TRUE")
    function_name = None
    function_alias = None

    def __init__(self, table_name, function_name, field_name, columns):
        field_name_seq = field_name.split(LOOKUP_SEP)
        self.model_field = field_name_seq[0]
        self.json_path = field_name_seq[1:]
        alias = self.model_field + 's'
        super(JsonbFunctionTable, self).__init__(table_name=table_name, alias=alias)
        self.function_name = function_name
        column_definitions = list()
        for _c in columns:
            column_definitions.append('{c_name} {c_type}'.format(c_name=_c[0], c_type=_c[1]))
        self.function_alias = '{alias}({column_definitions})'.format(
            alias=alias, column_definitions=','.join(column_definitions))

    def as_sql(self, compiler, connection):
        return "{join} {function}({table}.{field} {sign} '{json_path}') {f_alias} {condition}".format(
            join=self.jsonb_join_type[0],
            condition=self.jsonb_join_type[1],
            f_alias=self.function_alias,
            function=self.function_name[0],
            sign=self.function_name[1],
            table=compiler.quote_name_unless_alias(self.table_name),
            field=compiler.quote_name_unless_alias(self.model_field),
            json_path='{' + ",".join(self.json_path) + '}'
        ), []

    def relabeled_clone(self, change_map):
        return self.__class__(self.table_name, change_map.get(self.table_alias, self.table_alias))

    def equals(self, other, with_filtered_relation):
        return (
                isinstance(self, other.__class__) and
                self.table_name == other.table_name and
                self.table_alias == other.table_alias and
                self.function_name == other.function_name and
                self.join_type == other.join_type
        )
