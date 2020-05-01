import os
import re
import sys

import camelot
import click
import pandas as pd

from . import click_helpers


def __pdf_tables_to_dataframe(filepath, headers=False, pages='all', is_valid_table=False, sanitize=False, offset=0, limit=-1):
    """Read all tables in a given PDF then concat all into one dataframe"""

    # Read all tables in a PDF to frames
    tables = camelot.read_pdf(filepath=filepath, pages=pages)
    frames = []

    # define a header sanitier
    sanitize_header = lambda a: a
    if sanitize != False:
        sanitize_header = lambda d: dict(map(lambda kv: (kv[0], sanitize(kv[1])), d.items()))

    firstHeaders = sanitize_header(tables[offset].df.iloc[0].to_dict())

    if is_valid_table == False:
        # If no validator function, set it to check if the first headers are identical
        is_valid_table = lambda a: sanitize_header(a.iloc[0].to_dict()) == firstHeaders

    # determine the end of loop
    n = offset + limit
    if n < offset or n > tables.n:
        n = tables.n

    # loop through all tables, determine if they are valid for concat,
    # then put it into the "frames" slice for concating
    for i in range(offset, n):
        if is_valid_table(tables[i].df):
            frames.append(tables[i].df[1:])

    # assign the first table header to be the overall header
    # if none is provided
    if headers == False:
        headers = firstHeaders

    # concat all data frames into a single one
    return pd.concat(frames, ignore_index=True, sort=False).rename(columns=headers)


def __sanitize_items_in(df, sanitize):
    """Sanitize the dataframe values if it has EOL or space in it"""
    # Sanitize the dataframe values
    for i, row in df.iterrows():
        for key, value in row.iteritems():
            if type(value) != str:
                continue
            if "\n" in value or " " in value:
                df.at[i, key] = sanitize(value)


@click.command()
@click.option('--leave-space', default=False, is_flag=True, help="Leave the space in scraped table cells in sanitation process.")
@click.option('--headers', default=False, help="Specify the header names, separated by commas, for replacing the overall table. Use delimited \"\\,\" if you need to use actual comma.")
@click.option('--pages', default='all', type=str, help="Specifies the page range to scan. Can be comma separated page number, range like \"2-4\" or \"10-end\". Read \"3.5.2  Specify page numbers\" in camelot documentation.")
@click.option('--offset', default=0, type=int, help="The number of table(s) to skip before the start of scanning.")
@click.option('--limit', default=-1, type=int, help="The total number of table(s) to scan.")
@click_helpers.do_each(outer_keyword='files', inner_keyword='filename')
@click_helpers.print_output('--print-filename', 'print_filename', default=True, help="Print the result CSV filename to STDOUT.")
@click_helpers.dataframe_to_csv(keep_input_keyword=True, force_in_place=True)
@click.pass_context
def parse_pdf_to_csv(
    ctx,
    leave_space,
    headers,
    pages,
    offset,
    limit,
    filename,
):
    """Parse the PDF file and join all the tables"""

    # Define string sanitize
    sanitize = lambda a: a.replace("\r", "").replace("\n", "").replace(" ", "")
    if leave_space:
        sanitize = lambda a: a.replace("\r", "").replace("\n", "")

    if headers != False:
        # Treat the headers input as comma separated values
        headers_list = list(map(lambda a: a.replace("\\,", ","), re.split(r'(?<!\\),', headers)))
        headers_dict = dict(enumerate(headers_list))
    else:
        headers_dict = False

    # concat all tables, which passes the "is_valid_table" test
    # into a single dataframe.
    df = __pdf_tables_to_dataframe(
        filename,
        headers=headers_dict,
        pages=pages,
        #is_valid_table=lambda df: df[0][0] in ["個案\n編號", "Case \nno."],
        sanitize=sanitize,
        limit=limit,
        offset=offset,
    )

    # Sanitize the dataframe values
    __sanitize_items_in(df, sanitize)

    # Write to CSV file
    return df
