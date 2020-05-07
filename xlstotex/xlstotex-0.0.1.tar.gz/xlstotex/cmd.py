from argparse import ArgumentParser
from sys import argv

from xlstotex import convert


def parse_args():

    ap = ArgumentParser()
    ap.add_argument('input_file', type=str, help='Input Excel/CSV file')
    ap.add_argument('out_file', type=str, help='Text file output')
    return vars(ap.parse_args(argv[1:]))


def main():

    args = parse_args()
    convert(args['input_file'], args['out_file'])
