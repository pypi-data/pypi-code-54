import argparse

import pendulum

from date_range.generate_dates import generate_date_range_and_output


def parse_args(args=None):
    date_parser = lambda dt: pendulum.parse(dt).date()
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start-date', required=True, type=date_parser)
    parser.add_argument('-e', '--end-date', required=True, type=date_parser)
    parser.add_argument('-o', '--sort-order', choices=['asc', 'desc'], default='asc')
    return parser.parse_args(args=args)


def main():
    args = parse_args()
    generate_date_range_and_output(args)
