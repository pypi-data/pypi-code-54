from __future__ import print_function

import os
import os.path
import pickle
import sys

import click
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from . import click_helpers


def __get_credentials(scopes, credentials_file="credentials.json", pickle_file="token.pickle"):
    """Get credentials for access"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            #creds = flow.run_local_server(port=0)
            creds = flow.run_local_server(port=3000)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def __overwrite_sheet(creds, values=[], **kwargs):
    """
    WIP: script to overwrite sheet range into.
    """
    #  pylint: disable=no-member

    service = build('sheets', 'v4', credentials=creds)
    body = {
        'values': values,
    }
    service.spreadsheets().values().update(
        body=body,
        **kwargs,
    ).execute()


def __append_sheet(creds, spreadsheet_id, range_name, appending_values):
    """
    WIP: script to overwrite sheet range into.
    """
    #  pylint: disable=no-member

    #################### read current values

    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name,
    ).execute()

    if not result:
        print('No data found.')
    else:
        for row in result['values']:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)

    #################### write new values

    values = result['values']
    values.append(*appending_values)
    body = {
        'values': values,
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()


@click.group()
@click.option('-c', '--credentials', 'credentials_file', type=str, default="credentials.json", help="The filename of the Google API credential json. Default: credentials.json")
@click.option('-p', '--pickle', 'pickle_file', type=str, default="token.pickle", help="The filename of the cookie pickle to store access token. Default: token.pickle")
@click.argument('googlesheet_id')
@click.pass_context
def googlesheet(ctx, credentials_file, pickle_file, googlesheet_id):
    """Manipulate of Google Sheet data"""

    # TODO: check if credentials_file exists
    # TODO: prompt user how to generate the credentials JSON file form API console

    ctx.obj["googlesheet_id"] = googlesheet_id
    ctx.obj["credentials"] = __get_credentials(
        [
            'https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/spreadsheets',
        ],
        credentials_file=credentials_file,
        pickle_file=pickle_file,
    )


@googlesheet.command()
@click.option('-h', '--include-headers', is_flag=True, default=False, help="Include the header label as first row of the data.")
@click.option('-r', '--range', 'range_name', type=str, required=True, help="Specify the range to update.")
@click_helpers.do_each('files', 'filename')
@click_helpers.print_output('--print-filename', 'print_filename', help="Print the name of the input file to STDOUT")
@click_helpers.csv_to_dataframe('filename', keep_outer_keyword=True)
@click.pass_context
def update(ctx, filename,  df, include_headers, range_name):
    """Update google sheet"""

    # convert dataframe into 2-dimensional slice
    values = list(map(lambda a: a.tolist(), df.values))

    if include_headers:
        new_values = [list(df.keys())]
        new_values.extend(values)
        values = new_values

    __overwrite_sheet(
        ctx.obj["credentials"],
        values=values,
        spreadsheetId=ctx.obj["googlesheet_id"],
        range=range_name,
        valueInputOption='RAW',
    )

    return filename
