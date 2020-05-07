# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: display.py
# Project: path
# Author: Brian Cherinka
# Created: Monday, 27th April 2020 12:37:39 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2020 Brian Cherinka
# Last Modified: Monday, 27th April 2020 12:37:39 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
try:
    import rich.table
    import rich.console
except ImportError:
    rich = None


def create_rich_table(data, name='Table', columns=None, pprint=None):
    ''' '''

    if not rich:
        print('rich package not found. Cannot create rich table')

    table = rich.table.Table(title=name)

    # add columns
    if columns:
        for column in columns:
            table.add_column(column)

    # add rows (list of tuples)
    for row in data:
        table.add_row(*row)

    if pprint:
        print_rich(table)

    return table


def print_rich(data, console=None):
    ''' '''
    if not rich:
        print('rich package not found. Cannot print with rich console')

    if not console:
        from rich.console import Console
        console = Console()
    console.print(data)
