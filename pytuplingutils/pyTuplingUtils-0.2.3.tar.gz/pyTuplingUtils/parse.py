#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Oct 19, 2019 at 03:04 AM -0400

from argparse import ArgumentParser


def single_ntuple_parser_no_output(descr, parser=None):
    parser = ArgumentParser(description=descr) if parser is None else parser

    parser.add_argument('-n', '--ref',
                        nargs='?',
                        required=True,
                        help='''
path to reference n-tuple.''')

    parser.add_argument('-t', '--ref-tree',
                        nargs='?',
                        required=True,
                        help='''
tree name for the reference n-tuple.''')

    return parser


def single_ntuple_parser(descr, parser=None):
    parser = single_ntuple_parser_no_output(descr) if parser is None else parser

    parser.add_argument('-o', '--output',
                        nargs='?',
                        required=True,
                        help='''
path to output file.''')

    parser.add_argument('-b', '--ref-branch',
                        nargs='?',
                        required=True,
                        help='''
branch name(s) in reference n-tuple. may be separated by ",".''')

    return parser


def double_ntuple_parser_no_output(descr, parser=None):
    parser = single_ntuple_parser_no_output(descr) if parser is None else parser

    parser.add_argument('-N', '--comp',
                        nargs='?',
                        required=True,
                        help='''
path to comparison n-tuple.''')

    parser.add_argument('-T', '--comp-tree',
                        nargs='?',
                        required=True,
                        help='''
tree name for the comparison n-tuple.''')

    return parser


def double_ntuple_parser(descr, parser=None):
    if parser is None:
        parser = double_ntuple_parser_no_output(descr)
        parser = single_ntuple_parser(descr, parser)

    parser.add_argument('-B', '--comp-branch',
                        nargs='?',
                        required=True,
                        help='''
branch name(s) in comparison n-tuple. may be separated by ",".''')

    return parser
