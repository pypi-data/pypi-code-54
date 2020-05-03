#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read and write local XML data in CMI-format
"""

import os

from .schema import etree, parser


def writer(tree, file="cmif.xml", path="."):
    """
    write given element tree to file at path
    """
    xml = etree.ElementTree(tree, parser=parser)
    if path and not os.path.exists(path):
        os.makedirs(path)
    out = os.path.join(path, file)
    xml.write(out, pretty_print=True, encoding="UTF-8", xml_declaration=True)


def reader(filepath):
    """
    read xml data from given file path
    """
    return etree.parse(filepath, parser=parser)
