import ast
import tokenize

from sys import stdin

__version__ = '1.0'

ERROR_CODE = 'T008'
ERROR_MESSAGE = 'Constant value with leading or trailing spaces found'


class ConstantSpacesChecker(object):
    name = 'flake8-spaces-around-constants'
    version = __version__

    def __init__(self, tree, filename='(none)', builtins=None):
        self.tree = tree
        self.filename = (filename == 'stdin' and stdin) or filename

    def check_constant_with_spaces(self, node, name, value):
        if name.isupper() and value != value.strip():
            return {
                'message': '{0} {1}: {2} = "{3}"'.format(ERROR_CODE, ERROR_MESSAGE, name, value),
                'line': node.lineno,
                'col': node.col_offset
            }

    def run(self):
        # Get lines to ignore
        if self.filename == stdin:
            noqa = _get_noqa_lines(self.filename)
        else:
            with open(self.filename, 'r') as file_to_check:
                noqa = _get_noqa_lines(file_to_check.readlines())

        # Run the actual check
        errors = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                target = node.targets[0]
                if hasattr(target, 'id') and isinstance(node.value, ast.Str):
                    if node.lineno not in noqa:
                        error = self.check_constant_with_spaces(node, target.id, node.value.s)
                        if error is not None:
                            errors.append(error)
                elif hasattr(target, 'elts'):
                    # Multiple assign: a, b = x, y
                    if not isinstance(node.value, ast.Tuple):
                        # This is not a simple assignment (e.g. a function call). Skip.
                        continue
                    for index, element in enumerate(target.elts):
                        if not isinstance(node.value.elts[index], ast.Str):
                            continue
                        if node.lineno not in noqa:
                            error = self.check_constant_with_spaces(node, element.id, node.value.elts[index].s)
                            if error is not None:
                                errors.append(error)
                else:
                    # Some other edge cases, such as assigning to an instance variable. Not a constant.
                    pass

        # Yield the found errors
        for error in errors:
            yield (error.get('line'), error.get('col'), error.get('message'), type(self))


def _get_noqa_lines(code):
    tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
    return [token[2][0] for token in tokens if token[0] == tokenize.COMMENT and
            (token[1].endswith('noqa') or (isinstance(token[0], str) and token[0].endswith('noqa')))]
