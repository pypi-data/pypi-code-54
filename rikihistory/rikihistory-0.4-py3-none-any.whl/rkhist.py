import argparse
from history import histurl, record_history

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--entry', help='add a history entry with path action and user arguments',
                        action='store_true')
    parser.add_argument('path', help='page markdown file name in content', type=str)
    parser.add_argument('action', help='action description', type=str)
    parser.add_argument('user', help='user ID', type=str)
    args = parser.parse_args()
    if args.entry:
        record_history(args.path, args.action, args.user)
