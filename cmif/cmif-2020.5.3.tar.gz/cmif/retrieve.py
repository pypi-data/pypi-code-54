#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
retrieve remote XML data in CMI-format
"""

import requests

from .schema import etree, parser


def remote_file(url):
    """
    send http get request to given url with (optional) headers
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return etree.fromstring(response.content, parser=parser)
        print("requesting remote file failed!")
        print("url of request:")
        print(response.url)
        print("http status code: ",
              str(response.status_code))
    except requests.exceptions.ConnectionError:
        print("librair.protocols.http.get_request:")
        print("request failed! connection error...")
    except requests.exceptions.Timeout:
        print("librair.protocols.http.get_request:")
        print("request failed! timeout... try later?")
    except requests.exceptions.TooManyRedirects:
        print("librair.protocols.http.get_request:")
        print("request failed! bad url, try another one!")
    except requests.exceptions.RequestException:
        print("librair.protocols.http.get_request:")
        print("request failed! don't know why...")
    return None
