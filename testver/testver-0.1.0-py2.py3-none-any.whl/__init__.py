"Programmatically edit python package versions for testing."
import ast
import sys
import astunparse
from pathlib import Path

__version__ = "0.1.0"


def modver(filepath: Path, suffix: str = "test"):
    filepath = Path(filepath)
    tree = ast.parse(filepath.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and (
            node.targets[0].id == "__version__"
        ):
            if isinstance(node.value, ast.Constant):
                # python >=3.8 doesn't have ast.Str
                # new_value = node.value.value + f"-{suffix}"
                node.value.value += f"-{suffix}"
                new_value = node.value.value
            elif isinstance(node.value, ast.Str):
                node.value.s += f"-{suffix}"
                new_value = node.value.s
            break
    else:
        raise ValueError(
            "The specified file doesn't have a variable called __version__."
        )
    return (astunparse.unparse(tree), new_value)
