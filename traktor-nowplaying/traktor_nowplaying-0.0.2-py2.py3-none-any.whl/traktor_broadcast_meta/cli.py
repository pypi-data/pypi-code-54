"""
Contains a command-line interface implemented with argparse.
"""

from .core import Listener
from .options import PORT, QUIET
import argparse

DESCRIPTION = 'Use Traktor\'s broadcast functionality to extract metadata about the currently playing song'
EPILOG = 'Note that you must configur '

parser = argparse.ArgumentParser(
    description=DESCRIPTION
)

parser.add_argument('-p', '--port', default=PORT,
    type=int,
    help='Port to listen on for broadcasts from Traktor'    
)

parser.add_argument('-q', '--quiet', default=QUIET,
    action='store_true',
    help='Suppress console output of currently playing song'
)

parser.add_argument('-o', '--outfile', default=None,
    help='Provide a file path to which the currently playing song should be written',
)

args = parser.parse_args()

def main():
    listener = Listener(port=args.port, quiet=args.quiet, outfile=args.outfile)
    listener.start()

if __name__ == '__main__':
    main()
