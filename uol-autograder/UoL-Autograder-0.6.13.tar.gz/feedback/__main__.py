import argparse
import os
from . import run_test
from .general.util import save_feedback_file
from .general.result_watchdog import ResultWatchdog
import time


parser = argparse.ArgumentParser(description="General puprose test evaluator")
parser.add_argument('tested_file', type=str, help="file to be tested")
parser.add_argument('config_file', type=str, help="config for the test")
parser.add_argument('--result_file', '-f', type=str, default="result.json", help="output file name")
parser.add_argument('--clear_cache', '-x', action="store_true", help="Remove all cached contents")
parser.add_argument('--verbose', '-v', action="store_true", help="Enable extra console logging")
parser.add_argument('--copy_tmp', '-c', type=str, default=None, help="Copy tmp dir to specified location, before it's removed")
parser.add_argument('--enable_watchdog', '-w', action="store_true", help="Enable watchdog subprocess to ensure result file integrity [ONLY ENABLE ON EXAM ASSESSMENTS]")

# Primary entry point, with argument processing
def main():
    args = parser.parse_args()

    write_callback = None
    if args.enable_watchdog:
        watchdog = ResultWatchdog(args.result_file)
        write_callback = watchdog.submit_hash
        watchdog.launch()

    result = run_test(args.tested_file, args.config_file, {"clear_cache": args.clear_cache, "verbose": args.verbose}, args.copy_tmp)
    if not os.path.exists(args.result_file) or not args.enable_watchdog:
        save_feedback_file(result, args.result_file, verbose=args.verbose, callback=write_callback)
    time.sleep(1)


if __name__ == "__main__":      # Run main if ran directly
    main()