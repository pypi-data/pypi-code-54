from functools import reduce

from reader.feed import my_add
from reader.feed import my_product


def my_add_all(*args):
    return reduce(my_add, args, 0)


def my_product_all(*args):
    return reduce(my_product, args, 1)
