import logging
from subuid import SubUidList

log = logging.getLogger(__name__)

# support Python2 file not found
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def parse_subuid_file(filename):
    '''Parse the given filename and return a list of subuids'''
    subuids = SubUidList()
    try:
        with open(filename) as f:
            content = f.readlines()
        for line in content:
            line_list = line.rstrip().split(':')
            if len(line_list) != 3:
                logging.error('Line did not parse: %s' % line.rstrip())
                continue
            subuids.allocate(*line.rstrip().split(':'))
    except FileNotFoundError:
        log.info('File not found.')
    finally:
        log.info('Found %d subuids' % len(subuids))

    return subuids


def write_subuid_file(filename, subuids, mode='w'):
    '''Writes out the given list of subuids to the filename'''
    with open(filename, mode) as f:
        for subuid in subuids:
            f.write('%s\n' % subuid)
