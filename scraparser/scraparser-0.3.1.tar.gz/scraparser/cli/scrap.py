import os
import sys
import urllib.request
from datetime import datetime
from urllib.parse import urlparse

import click
import validators

from . import click_helpers


def __scrap_url(url, filename, mkdir=True, headers={}):
    if os.path.exists(filename):
        raise Exception("File already exists: {0}".format(filename))

    req = urllib.request.Request(
        url,
        data=None,
        headers=headers,
    )
    response = urllib.request.urlopen(req)
    with open(filename, "wb") as file:
        file.write(response.read())


@click.command()
@click_helpers.do_each('urls', 'url_input')
@click_helpers.print_output('--print-filename', default=True, help="Print the result filename to STDOUT.")
@click.pass_context
def scrap(ctx, url_input):
    """Scrap any URL, add some timestamp string, then save to the "./data" folder of the install location."""

    if not validators.url(url_input):
        raise Exception("Not a valid URL: {0}".format(url_input))

    url = urlparse(url_input)
    # Note: might support other scheme such as "file://" in the future,
    # but focus on HTTP and FTP for now.
    if url.scheme not in ["http", "https", "ftp"]:
        raise Exception("Not a supported URL scheme: {0}".format(url_input))

    # Rewrite the filename (from path) to add timestamp
    filename_basename = os.path.basename(url.path)
    timestring = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    dirname = os.path.join(
        os.getcwd(),
        "data",
    )
    filename_scraped = os.path.join(
        dirname,
        "{0}.{1}{2}".format(
            os.path.splitext(filename_basename)[0],
            timestring,
            os.path.splitext(filename_basename)[1],
        ),
    )

    # Do the scrapping
    __scrap_url(
        url.geturl(),
        filename_scraped,
        mkdir=True,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        },
    )
    return filename_scraped
