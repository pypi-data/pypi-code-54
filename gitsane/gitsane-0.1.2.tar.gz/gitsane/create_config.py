#!/usr/bin/env python3
"""
Summary:
    Create json file object from text file
"""
import os
import sys
import json
import argparse
import datetime
import inspect
from pygments import highlight, lexers, formatters
from core import loggers

logger = loggers.getLogger()
container = []
now = datetime.datetime.now().strftime("%Y-%m-%d")
input_file = 'repository.list'
output_file = 'repository-audit.json'
infile_path = os.environ['HOME'] + '/Backup/usr/' + input_file
outfile_path = os.environ['HOME'] + '/Backup/usr/' + output_file


def export_json_object(dict_obj, filename=None):
    """
    Summary:
        exports object to block filesystem object

    Args:
        :dict_obj (dict): dictionary object
        :filename (str):  name of file to be exported (optional)

    Returns:
        True | False Boolean export status

    """
    try:
        if filename:
            try:
                with open(filename, 'w') as handle:
                    handle.write(json.dumps(dict_obj, indent=4, sort_keys=True))
                    logger.info(
                        '%s: Wrote %s to local filesystem location' %
                        (inspect.stack()[0][3], filename))
                handle.close()
            except TypeError as e:
                logger.warning(
                    '%s: object in dict not serializable: %s' %
                    (inspect.stack()[0][3], str(e)))
        else:
            json_str = json.dumps(dict_obj, indent=4, sort_keys=True)
            print(highlight(json_str, lexers.JsonLexer(), formatters.TerminalFormatter()))
            logger.info('%s: successful export to stdout' % inspect.stack()[0][3])
            return True
    except OSError as e:
        logger.critical(
            '%s: export_file_object: error writing to %s to filesystem. Error: %s' %
            (inspect.stack()[0][3], filename, str(e)))
        return False
    else:
        logger.info('export_file_object: successful export to %s' % filename)
        return True


def pretty_print(list):
    """ prints json tags with syntax  highlighting """
    json_str = json.dumps(list, indent=4, sort_keys=True)
    print(highlight(
        json_str, lexers.JsonLexer(), formatters.TerminalFormatter()
        ))
    print('\n')
    return True


def main():
    """ Creates json file from text file input """
    try:
        with open(infile_path) as f1:
            f2 = f1.readlines()
    except OSError as e:
        logger.exception(f'{inspect.stack()[0][3]}: problem parsing file {input_file}')
        return False
    try:
        for line in f2:
            location = line.split(',')[0]
            path = '/'.join(line.split(',')[0].split('/')[:-1])
            repo = line.split(',')[1]
            if repo.endswith('\n'):
                repo = repo[:-1]
            container.append(
                {
                    "location": location,
                    "path": path,
                    "repo": repo
                }
            )
        # output
        if export_json_object(dict_obj=container, filename=outfile_path):
            pretty_print(container)
            return True
        else:
            logger.info(f'Problem writing output file object {outfile_file}')
            return False
    except Exception as u:
        logger.exception(f'{inspect.stack()[0][3]}: problem parsing file {input_file}')
        return False


def options(parser, help_menu=False):
    """
    Summary:
        parse cli parameter options
    Returns:
        TYPE: argparse object, parser argument set
    """
    parser.add_argument("-p", "--profile", nargs='?', default="default",
                              required=False, help="type (default: %(default)s)")
    parser.add_argument("-u", "--user-name", dest='username', type=str, required=False)
    parser.add_argument("-a", "--auto", dest='auto', action='store_true', required=False)
    return parser.parse_args()


def init_cli():
    # parser = argparse.ArgumentParser(add_help=False, usage=help_menu())
    parser = argparse.ArgumentParser(add_help=False)

    try:
        args = options(parser)
    except Exception as e:
        stdout_message(str(e), 'ERROR')
        sys.exit(exit_codes['EX_OK']['Code'])

    if len(sys.argv) == 1:
        help_menu()
        sys.exit(exit_codes['EX_OK']['Code'])


if __name__ == '__main__':
    sys.exit(main())
