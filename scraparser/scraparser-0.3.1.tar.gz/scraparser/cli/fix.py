import math
import re
import sys

import click

from . import click_helpers


@click.group()
@click.pass_context
def fix(ctx):
    """Fixing data issues from PDF parsing mistakes."""
    pass


@fix.command()
@click.option('--in-place', default=False, is_flag=True, help="Modify the file in-place.")
@click_helpers.do_each(outer_keyword='files', inner_keyword='filename')
@click_helpers.print_output('--print_filename', default=True, help="Print the result CSV filename to STDOUT.")
@click_helpers.csv_to_dataframe(outer_keyword="filename", inner_keyword="df", keep_outer_keyword=True)
@click_helpers.dataframe_to_csv(input_keyword="filename")
@click.pass_context
def empty_rows(ctx, df):
    """Treat rows with only 1 cell to be a parser mistake. Concat that cell content to the one above it."""
    rows_to_drop = []

    for i, row in df.iterrows():
        num_empty_field = 0
        non_empty_cell_key = -1

        for key, value in row.iteritems():
            if type(value) == float and math.isnan(value):
                num_empty_field += 1
            else:
                non_empty_cell_key = key

        # If the row has only 1 field defined
        if num_empty_field == len(row) - 1 and i > 0:
            df.at[i-1, non_empty_cell_key] += df.at[i, non_empty_cell_key]
            rows_to_drop.append(i)

    df = df.drop(rows_to_drop)
    return df


@fix.command()
@click.option('--column', type=int, help="To treat the column with empty value. Begins with 0. Required.")
@click_helpers.do_each(outer_keyword='files', inner_keyword='filename')
@click_helpers.print_output('--print_filename', default=True, help="Print the result CSV filename to STDOUT.")
@click_helpers.csv_to_dataframe(outer_keyword="filename", inner_keyword="df", keep_outer_keyword=True)
@click_helpers.dataframe_to_csv(input_keyword="filename")
@click.pass_context
def column_underflow(ctx, column, df):
    """Fix the empty values which content spilled over to the last column."""
    keys = df.keys()
    accepted_values = list(filter(lambda a: type(a) == str, df[keys[column]].unique()))

    for i, row in df.iterrows():
        if type(row.iat[column]) == float and math.isnan(row.iat[column]):
            for accepted_value in accepted_values:
                if str(row.iat[column-1]).endswith(accepted_value):
                    df.iat[i, column-1] = row.iat[column-1][:-len(accepted_value)]
                    df.iat[i, column] = accepted_value
    return df


@fix.command()
@click.option('--column', type=int, help="To treat the column with empty value. Begins with 0. Required.")
@click.option('--date-format', type=str, default="DD/MM/YYYY", help="Specify the format of the date string. Default: DD/MM/YYYY.")
@click_helpers.do_each(outer_keyword='files', inner_keyword='filename')
@click_helpers.print_output('--print_filename', default=True, help="Print the result CSV filename to STDOUT.")
@click_helpers.csv_to_dataframe(outer_keyword="filename", inner_keyword="df", keep_outer_keyword=True)
@click_helpers.dataframe_to_csv(input_keyword="filename")
@click.pass_context
def date_column_underflow(ctx, column, date_format, df):
    """Fix the empty values of date column, which content spilled over to the last column."""

    # parse date format into regex
    pattern = re.escape(date_format).upper()
    pattern = pattern.replace("YYYY", "\\d{4}")
    pattern = pattern.replace("YY", "\\d{2}")
    pattern = pattern.replace("MM", "\\d{2}")
    pattern = pattern.replace("DD", "\\d{2}")
    pattern = "^(.+?)({0})$".format(pattern)

    for i, row in df.iterrows():
        if type(row.iat[column]) == float and math.isnan(row.iat[column]):
            match = re.match(pattern, str(row.iat[column-1]))
            if match is not None:
                df.iat[i, column-1] = match.group(1)
                df.iat[i, column] = match.group(2)
    return df

@fix.command()
@click.option('--column', type=int, help="To treat the column with empty value. Begins with 0. Required.")
@click.option('--date-format', type=str, default="DD/MM/YYYY", help="Specify the format of the date string. Default: DD/MM/YYYY.")
@click_helpers.do_each(outer_keyword='files', inner_keyword='filename')
@click_helpers.print_output('--print_filename', default=True, help="Print the result CSV filename to STDOUT.")
@click_helpers.csv_to_dataframe(outer_keyword="filename", inner_keyword="df", keep_outer_keyword=True)
@click_helpers.dataframe_to_csv(input_keyword="filename")
@click.pass_context
def date_column_overflow(ctx, column, date_format, df):
    """Fix the values spilled over from other column onto a date column."""

    # parse date format into regex
    pattern = re.escape(date_format).upper()
    pattern = pattern.replace("YYYY", "\\d{4}")
    pattern = pattern.replace("YY", "\\d{2}")
    pattern = pattern.replace("MM", "\\d{2}")
    pattern = pattern.replace("DD", "\\d{2}")
    pattern = "^(.+?)({0})$".format(pattern)

    if column == 0:
        # TODO: perhaps throw some error here???
        return df

    for i, row in df.iterrows():
        if type(row.iat[column-1]) == float and math.isnan(row.iat[column-1]):
            match = re.match(pattern, str(row.iat[column]))
            if match is not None:
                df.iat[i, column-1] = match.group(1)
                df.iat[i, column] = match.group(2)
    return df
