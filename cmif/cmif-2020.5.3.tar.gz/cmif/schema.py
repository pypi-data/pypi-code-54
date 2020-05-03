#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
handle XML data in CMI-format
"""

from lxml import etree

parser = etree.XMLParser(remove_blank_text=True)


def pretty(elements):
    """
    pretty print elements
    """
    print(etree.tostring(elements, pretty_print=True).decode())
