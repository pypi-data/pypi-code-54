import re
from typing import Union, Any


def match_regex_expr_or_error(value, field, expr) -> Union[Any, ValueError]:
    if re.match(expr, value):
        return value
    else:
        raise ValueError(f"Avro schema field '{field}' must match regex expression: {expr}")