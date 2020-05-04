from imperium_legacy.helpers import exists, matches, date, date_modify
from imperium_legacy.exceptions import UnsupportedFunctionException
import parser
import re

AUTHORIZED_FUNCTIONS = { 
    'exists': True,
    'matches': True,
    'date': True,
    'date_modify': True
}


class Expression:

    def evaluate(self, expression, subject, source=None):
        matched = re.findall(r"([a-zA-Z_{1}][a-zA-Z0-9_]+)\s?\(", expression)
        for match in matched:
            if match not in AUTHORIZED_FUNCTIONS:
                raise UnsupportedFunctionException('[error] Unsupported function "{}"'.format(match))

        subject_reg = r"""(?<![A-Za-z1-9'\"$#\[.])(\$subject|subject|\$out|out)\b"""
        source_reg = r"""(?<![A-Za-z1-9'\"$#\[.])(\$source|source|\$in)\b"""

        expression = re.sub(subject_reg, 'subject', expression)
        expression = re.sub(source_reg, 'source', expression)

        expr = parser.expr(expression)

        return eval(expr.compile(''))
