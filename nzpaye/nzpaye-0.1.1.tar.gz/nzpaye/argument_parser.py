import argparse

def setup_parser_arguments(parser):
    parser.add_argument(
           '--hourly-rate',
            type=float,
            dest='hourly_rate',
            required=True,
            help="Enter the hourly rate"
    )
    parser.add_argument(
            '--hours-worked',
            type=float,
            dest='hours_worked',
            required=True,
            help='Enter the number of hours worked'
    )
    parser.add_argument(
            '--wht',
            type=float,
            dest='witholding_tax',
            default=10.0,
            help='Enter your witholding tax i.e. 10 or 20. Default value is 10.'
    )
    return parser

def get_parser():
    parser = argparse.ArgumentParser(description="Income Summary calculator")
    setup_parser_arguments(parser)
    return parser