import ast
import os
from collections import namedtuple

statement = namedtuple('Statement', ['code', 'line'])


class PyParser(ast.NodeVisitor):
    def __init__(self, path):
        self.path = path
        self.parsed_stmts = []

    def parse_source(self):
        self.parsed_stmts = []
        with open(self.path, 'r') as src_code:
            ast_tree = ast.parse(src_code.read())
        self.visit(ast_tree)
        return self.parsed_stmts


class FileMatcher:
    """
    Class helps to maintain custom list of files
    Based on pytest-isort implementation:
        https://github.com/moccu/pytest-isort/blob/master/pytest_isort.py
    """

    def __init__(self, require_lines):
        self.requires = []

        for line in require_lines:
            comment_position = line.find("#")
            # Strip comments.
            if comment_position != -1:
                line = line[:comment_position]

            glob = line.strip()

            # Skip blank lines.
            if not glob:
                continue

            # Normalize path if needed.
            if glob and os.sep != '/' and '/' in glob:
                glob = glob.replace('/', os.sep)

            self.requires.append(glob)

    def __call__(self, path):
        for glob in self.requires:
            if path.fnmatch(glob):
                return glob
