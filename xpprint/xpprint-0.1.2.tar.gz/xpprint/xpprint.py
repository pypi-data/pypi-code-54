import argparse
import sys

from bs4 import BeautifulSoup, PageElement, Tag


def tree(bsObj, level=-1, filter=lambda x: False):
    assert isinstance(bsObj, PageElement), type(bsObj)
    
    if not isinstance(bsObj, Tag) or filter(bsObj.name):
        return
    
    if BeautifulSoup.ROOT_TAG_NAME != bsObj.name:
        indent = '| ' * max(level, 0)
        cls = '.' + ' '.join(bsObj.attrs['class']) if 'class' in bsObj.attrs else ''
        id  = '#' + bsObj.attrs['id']              if 'id'    in bsObj.attrs else ''
        print('{indent}-{name}{cls}{id}'.format(indent=indent, name=bsObj.name, cls=cls, id=id))
    
    for c in bsObj.children:
        tree(c, level=level+1, filter=filter)


def __parser():
    PARSER_DESC0 = 'html tree view pprint'
    PARSER_HELP0 = 'stdin or .html filename'
    PARSER_HELP1 = 'filtered tag names'
    PARSER_HELP2 = 'HTML parser name'
    
    parser = argparse.ArgumentParser(description=PARSER_DESC0)
    parser.add_argument('html', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help=PARSER_HELP0)
    parser.add_argument('--filter', nargs='?', default=['p', 'br', 'span'],
                        help=PARSER_HELP1)
    parser.add_argument('--parser', default='html.parser',
                        help=PARSER_HELP2)
    
    return parser


parser = __parser()


def main():
    if sys.stdin.isatty():
        parser.print_help(); return
    
    args = parser.parse_args()
    html = args.html.read()
    bsObj = BeautifulSoup(html, features=args.parser)
    
    tree(bsObj, filter=lambda x: x in args.filter)
