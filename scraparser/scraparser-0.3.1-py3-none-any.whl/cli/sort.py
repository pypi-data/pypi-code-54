import sys

import click
import pandas as pd

from . import click_helpers


@click.command()
@click.option('--sort-as-number', default=True, is_flag=True, help="To treat the column like number for sorting. Default True")
@click.option('--column', default=0, type=int, help="The column number to sort with. Count starting with 0. Default 0")
@click_helpers.do_each(outer_keyword='files', inner_keyword='filename')
@click_helpers.print_output('--print_filename', default=True, help="Print the result CSV filename to STDOUT.")
@click_helpers.csv_to_dataframe(outer_keyword="filename", inner_keyword="df", keep_outer_keyword=True)
@click_helpers.dataframe_to_csv(input_keyword="filename")
@click.pass_context
def sort(ctx, column, sort_as_number, df):
    """Sort the data by the specified column. By default sort by the first column."""
    column_index = df.keys()[0]
    if sort_as_number:
        df[column_index] = pd.to_numeric(df[column_index])
    df.sort_values(by=column_index, inplace=True)
    return df
