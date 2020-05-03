import click
import operator
import time
from os import getcwd
from zoek.generator_from_path import generator_from_path
from zoek._filter_attr import filter_attr
from zoek.print_iterable import print_iterator
from zoek._custom_operators import string_contains, string_begins_with


@click.command()
@click.argument('path', default=getcwd())
@click.option('--depth', '-d', type=int, default=1, help="how many subdirectories should zoek look in?"
                                                         "defaults to 1, meaning only files in current directory.")
@click.option('--startswith', '-s', type=str, help="require file name to start with a string")
@click.option('--contains', '-c', type=str, help="require file name to contain a certain string")
@click.option('--minsize', '-m', type=int,
              help="filter on size (-size) given in Kb: the file has size n, where n could be:"
                   "+integer, integer -> file size bigger than integer"
                   "-integer -> file size smaller than integer")
@click.option('--datecreated', '-dc', type=int, help="files that were created n minutes ago, where n could be:"
                                                     "+integer -> files created more than n minutes ago"
                                                     "-integer -> files created less than n minutes ago"
                                                     "integer -> files created exactly n minutes ago)")
@click.option('--datemodified', '-dm', type=int, help="files that were modified n minutes ago, where n could be:"
                                                      "+integer -> files created more than n minutes age"
                                                      "-integer -> files created less than n minutes age"
                                                      "integer -> files created exactly n minutes ago")
def main(depth, path, startswith, minsize, contains, datecreated, datemodified):
    files = generator_from_path(path, max_depth=depth)
    time_now = time.time()

    if startswith is not None:
        files = filter_attr(generator=files, attr="name", op=string_begins_with, value=startswith)

    if contains is not None:
        files = filter_attr(generator=files, attr="name", op=string_contains, value=contains)

    if minsize is not None:
        files = filter_attr(generator=files, attr="st_size", op=operator.ge, value=minsize)

    if datecreated is not None:
        diff = time_now - (abs(datecreated) * 60)
        if datecreated <= 0:
            ops = operator.ge
        else:
            ops = operator.lt

        files = filter_attr(generator=files, attr="st_ctime", op=ops, value=diff)

    if datemodified is not None:
        diff = time_now - (abs(datemodified) * 60)
        if datemodified <= 0:
            ops = operator.ge
        else:
            ops = operator.lt
        files = filter_attr(generator=files, attr="st_mtime", op=ops, value=diff)

    print_iterator(files)


if __name__ == '__main__':
    main()
