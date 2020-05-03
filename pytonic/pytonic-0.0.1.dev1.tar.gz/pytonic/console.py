import argparse
import pkg_resources
import sys

version = pkg_resources.get_distribution('pytonic').version

def verbsVisitor(verb):
    for _verb in pkg_resources.iter_entry_points(group='pytonic.verbs'):
        if verb == _verb.name:
            return _verb.load()
    

def generateOptionalArguments(parser):
    add = parser.add_argument
    add('--version', action='store_true', help='prints the pytonic current version')

def generatePytonicVerbs(parser):
    verb_parser = parser.add_subparsers(
        dest='verb',
        metavar='[verbs]'
    )
    add = verb_parser.add_parser
    add('make', help='Makes a catkin package', description='Makes a catkin package')
    add('configure', description="Makes a catkin package")

def main():
    parser = argparse.ArgumentParser()
    generateOptionalArguments(parser)
    generatePytonicVerbs(parser)

    args = parser.parse_args()
    if args.version:
        print('pytonic {}'.format(version))
    if args.verb:
        verbsVisitor(args.verb)