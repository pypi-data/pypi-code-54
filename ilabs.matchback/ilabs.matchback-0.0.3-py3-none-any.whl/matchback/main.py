import argparse
import lxml.etree as et
import lxml.html as ht
import difflib
import re
import collections
import uuid
import logging
import json


NS = 'http://innodatalabs.com/innodom'
inno = lambda x: f'{{{NS}}}{x}'

IndexedItem = collections.namedtuple('IndexedItem', ['text', 'elt', 'level', 'type'])


def matchback(html_name, xml_name, output_html, output_meta, required_coverage=0.75):

    if required_coverage <= 0.:
        raise ValueError('Required coverage can not be zero or negative')

    html = ht.parse(html_name)

    with open(xml_name, 'rb') as f:
        xml = et.fromstring(f.read())

    if xml.tag != inno('dom'):
        raise RuntimeError('XML document is not an InnoDOM one (top level tag should be "dom")!')

    content = xml.find('.//' + inno('content'))
    if content is None:
        raise RuntimeError('XML document problem: "content" not found')

    meta = xml.find('.//' + inno('meta'))
    if meta is None:
        raise RuntimeError('XML document problem: "meta" not found')

    html_index = list(build_index(html.getroot()))
    xml_index = list(build_index(content))

    html_text = [x.text for x in html_index]
    xml_text = [x.text for x in xml_index]

    matcher = difflib.SequenceMatcher(isjunk=None, a=html_text, b=xml_text, autojunk=False)

    match_index = {}

    equals = 0
    deletes = 0
    inserts = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # print(' '.join(html_text[i1:i2]))
            equals += i2-i1
            for j in range(j1, j2):
                match_index[j] = ('exact', i1 + j - j1)
        elif tag == 'replace':
            # print('replace:', ' '.join(html_text[i1:i2]), '=>', ' '.join(xml_text[j1:j2]))
            deletes += i2-i1
            inserts += j2-j1
            for j in range(j1, j2):
                match_index[j] = ('fuzzy', i1, i2)
        elif tag == 'insert':
            # print('insert:', ' '.join(xml_text[j1:j2]))
            inserts += j2-j1
        elif tag == 'delete':
            # print('delete:', ' '.join(html_text[i1:i2]))
            deletes += i2-i1
        else:
            assert False, tag

    percent_inserts = inserts / (equals + deletes + 1.e-8)
    percent_deletes = deletes / (equals + inserts + 1.e-8)
    logging.debug('Mismatch: %s', percent_inserts + percent_deletes)

    meta_json = []
    for datapoint in meta:
        obj = {
            'key': datapoint.attrib['key'],
            'value': datapoint.text.strip(),
        }
        idref = datapoint.get('idref')
        if idref is not None:
            srcid = find_idref(match_index, html_index, xml_index, idref, required_coverage=required_coverage)
            obj['idref'] = srcid

        if datapoint.get('confidence'):
            obj['confidence'] = round(float(datapoint.get('confidence')), 3)

        meta_json.append(obj)

    html.write(output_html)
    logging.info('Saved HTML as %s', output_html)

    with open(output_meta, 'w') as f:
        json.dump(meta_json, f, indent='\t')
    logging.info('Saved META as %s', output_meta)


def build_index(xml):
    '''Given an XML tree, extracts text and builds an index from text offset back to the closest XML element'''

    def process(elt, level):
        if elt.text and elt.text.strip():
            for chunk in segment(elt.text.strip()):
                yield IndexedItem(chunk, elt, level, 'text')

        for c in elt:
            yield from process(c, level+1)

        if elt.tail and elt.tail.strip():
            for chunk in segment(elt.tail.strip()):
                yield IndexedItem(chunk, elt, level, 'tail')

    yield from process(xml, 0)


def segment(text):
    '''Simplest possible segmentation: words'''
    return text.split()


def find_idref(match_index, html_index, xml_index, id_, required_coverage=0.75):
    '''Given match index and id of an element in the InnoDom, finds matching element in the source HTML.

    Side effect: may create an "id" attribute on the HTML source element if needed.

    Returns the id of the source HTML that matched best to the id of the InnoDOM.
    '''
    offsets = list(xml_offsets(xml_index, id_))
    coverage = 0
    srcset = {}
    for off in offsets:
        x = match_index.get(off)
        if x is not None and x[0] == 'exact':
            coverage += 1
            _, i = x
            src = html_index[i]
            srcset[id(src.elt)] = (src.elt, src.level)

    logging.debug('Searching for %s: found %s text chunks, %s of which (%4.2lf) can be traced back to the HTML source',
        id_, len(offsets), coverage, coverage / (len(offsets) + 1.e-8))

    if coverage < required_coverage * len(offsets):
        raise RuntimeError(f'Failed to find a reliable match for idref "{id_}". Required coverage={required_coverage}.')

    # find lowest common elt that covers all srset
    while len(srcset) > 1:
        # pop elt with highest level
        topop, _ = max(srcset.items(), key=lambda x:x[1][1])
        elt, level = srcset.pop(topop)
        # move it to the parent
        elt = elt.getparent()
        level -= 1
        srcset[id(elt)] = elt, level

    assert len(srcset) == 1
    _, (elt, level) = srcset.popitem()

    srcid = elt.get('id')
    if srcid is None:
        srcid = str(uuid.uuid4())
        logging.debug('Created an id for element %s: %s', elt.tag, srcid)
        elt.set('id', srcid)

    logging.debug('Found a match %s => %s', id_, srcid)

    return srcid


def xml_offsets(xml_index, id_):
    '''Finds all offsets in the index array that are "covered" by an element with the given id'''
    for off, (_, elt, _, _) in enumerate(xml_index):
        while elt is not None:
            if elt.get('id') == id_:
                yield off
                break
            elt = elt.getparent()


def main():
    parser = argparse.ArgumentParser(description='match HTML and InnoDOM XML files, then translate idref from InnoDOM back to the source HTML, and writes HTML and META')

    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Increase verbosity level')
    parser.add_argument('-r', '--required', type=float, default=0.75, help='Required coverage threshold, default is %(default)s')
    parser.add_argument('input_html', help='HTML input file')
    parser.add_argument('input_innodom', help='InnoDOM XML input file')
    parser.add_argument('output_html', help='Output HTML - copy of the input HTML with ids added')
    parser.add_argument('output_meta', help='Output META in JSON format')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    matchback(args.input_html, args.input_innodom, args.output_html, args.output_meta, required_coverage=args.required)


if __name__ == '__main__':
    main()
