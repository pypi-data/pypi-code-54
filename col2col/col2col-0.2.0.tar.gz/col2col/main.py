#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import logging

from col2col.col2col import col2col_fromfile

logger = logging.getLogger('col2col')


def main():

    parser = argparse.ArgumentParser(prog='col2col',
                                     description='Column to column XLSX units converter',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        help='input XLSX',
                        required=True)
    parser.add_argument('-o', '--output',
                        type=str,
                        help='output XLSX',
                        required=True)
    parser.add_argument('-m', '--map',
                        type=str,
                        help='JSON map',
                        required=True)
    parser.add_argument('-r', '--reverse',
                        action='store_true',
                        default=False,
                        help='Reverse JSON map',
                        required=False)
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='Activate verbosity',
                        required=False)

    args = parser.parse_args()

    # Setup logger handler

    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Checking inputs
    if os.path.isfile(args.input):
        in_xlsx = args.input
    else:
        raise FileNotFoundError("Input XLSX not found: {f}".format(f=args.input))

    output_directory = os.path.dirname(os.path.abspath(args.output))
    if os.path.isdir(output_directory):
        out_xlsx = args.output
    else:
        raise NotADirectoryError("Directory for output XLSX not found: {d}".format(d=output_directory))

    if os.path.isfile(args.map):
        map_json = args.map
    else:
        raise FileNotFoundError("Map JSON file not found: {jf}".format(jf=args.map))

    # Core
    col2col_fromfile(in_xlsx, out_xlsx, map_json, reverse=args.reverse)


if __name__ == "__main__":
    main()
