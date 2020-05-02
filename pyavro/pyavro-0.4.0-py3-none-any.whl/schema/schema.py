import pydantic as pyd
from typing import List
import fastavro
import funcy as fn
from pyavro.util import match_regex_expr_or_error
from pyavro.field.field import Field


class Schema(pyd.BaseModel):
    """
    Avro uses a schema to define values in a record. This schema describes the fields allowed in the value,
    along with their data types.

    The schema is stored inside an avro file as JSON, whereas the records themselves are stored as binary. This means
    that every record inside an Avro file is guaranteed to conform to that schema.

    Args:
        type: Identifies the JSON field type. For Avro schemas, this must always be record when it is specified at
        the schema's top level. The type record means that there will be multiple fields defined.

        namespace: This identifies the namespace in which the object lives. Essentially, this is meant to be a URI
        that has meaning to you and your organization. It is used to differentiate one schema type from
        another should they share the same name.

        name: This is the schema name which, when combined with the namespace, uniquely identifies the schema within
        the store.

        fields_: This is the actual schema definition. It defines what fields are contained in the value, and the
        data type for each field. A field can be a simple data type, such as an integer or a string, or it can
        be complex data. Note: The field is suffixed with an underscore here because it clashes with Pydantic reserved
        keywords. An alias is used here to ensure we deserialize with the right value when we parse the schema.
    """
    type: str = "record"
    namespace: str
    name: str
    fields_: List[Field] = pyd.Field(..., alias="fields")

    @pyd.validator('name')
    def name_must_begin_with_letters(cls, value):
        expr = "^[A-Za-z_]"
        return match_regex_expr_or_error(value, 'name', expr)

    @pyd.validator('name')
    def name_must_only_contain(cls, value):
        expr = "[A-Za-z0-9_]"
        return match_regex_expr_or_error(value, 'name', expr)

    def parse(self):
        self.fields_ = fn.lmap(lambda x: x._to_avro_type(), self.fields_)
        dict_schema = self.dict(by_alias=True)
        parsed_schema = fastavro.parse_schema(dict_schema, _write_hint=False)
        return parsed_schema
