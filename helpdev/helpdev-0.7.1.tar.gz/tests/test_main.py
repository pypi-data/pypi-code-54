#!python
# -*- coding: utf-8 -*-
"""Test the qtsass is compiling the SCSS files to QSS."""

import helpdev


def test_check_float():
    output = helpdev.check_float()
    assert isinstance(output, dict)
