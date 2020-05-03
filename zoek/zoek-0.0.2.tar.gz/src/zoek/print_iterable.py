from typing import Iterator


def print_iterator(it: Iterator) -> None:
    """Prints the elements of the provided iterator"""
    try:
        while True:
            file = next(it)
            print(file.name)
    except StopIteration:
        pass
