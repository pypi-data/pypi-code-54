from tabulate import tabulate
from nzpaye.paye import income_summary
import sys
from nzpaye import argument_parser
import logging
from nzpaye.log import setup_logging

setup_logging("ERROR")
logger = logging.getLogger("paye")

def validate_argument_values(options):
    try:
        if not (options.witholding_tax == 10.0 or options.witholding_tax == 20.0):
            logger.error("Witholding tax can be 10 or 20 ")
            sys.exit(1)
        if options.hours_worked <= 0:
            logger.error("Hours worked should be greater than 0")
            sys.exit(1)
        if options.hourly_rate <= 0:
            logger.error("Hourly rate should be greater than 0")
            sys.exit(1)
    except ValueError as e:
        logger.error(e)
        sys.exit(1)
    return True

def paye_summary(options):
    try:
        validate_argument_values(options)
        summary = income_summary(options.hourly_rate, options.hours_worked, options.witholding_tax)
        print(tabulate([list(summary.values())],
                       headers=["Hours Worked", "Total Income", "Less Witholding Tax (10%)", "Plus GST", "Paid to Account",
                                "Remaining PAYE", "Remaining GST + PAYE", "Disposable Income"], tablefmt='pretty'))
    except Exception as e:
        logger.error("Oops something went wrong. ")
        logger.error(str(e))
        sys.exit(1)

