import typehint as th
import inspect
import ast
import _ast

class ClowLang:
    def __init__(self, llc='llc', cc='cc'):
        self.types = th.TypeHints()

    def compile_function(self, f):
        source = inspect.getsource(f.__code__)
        module = ast.parse(source)
        
        return self.generate_code(module)

    def compiled(f):
        assembly = self.compile_function(f)

    def generate_code(module):
        return ''
