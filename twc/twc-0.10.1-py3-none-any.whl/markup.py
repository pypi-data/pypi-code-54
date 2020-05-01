# Copyright (C) 2019 Michał Góral.
#
# This file is part of TWC
#
# TWC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TWC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TWC. If not, see <http://www.gnu.org/licenses/>.

'''Custom markup processor.'''

import re
import attr


_SEPS = re.compile(r'(,|\+)')


@attr.s
class _Item:
    before = attr.ib('')
    after = attr.ib('')
    attribute = attr.ib('')
    style = attr.ib('')
    fmt = attr.ib('')

    @property
    def fmtspec(self):
        if not self.attribute:
            return ''
        if self.fmt:
            return '{{{}:{}}}'.format(self.attribute, self.fmt)
        return '{{{}}}'.format(self.attribute)


@attr.s
class _State:
    _start = attr.ib(None)
    _end = attr.ib(None)
    _next = attr.ib(None)

    def consume(self, item, text, pos):
        if self._start is None:
            self._start = pos
        self._end = pos

        return self._consume(item, text, pos)

    def finalize(self, item, text):
        if self._end is not None:
            self._end += 1
        self._finalize(item, text)

    def spanned(self, text):
        if self._start is None or self._end is None:
            return ''
        return text[self._start:self._end]

    def next(self):
        return self._next

    @property
    def span(self):
        return (self._start, self._end)

    def _consume(self, item, text, pos):
        return True

    def _finalize(self, item, text):
        '''Default implementation does nothing.'''
        return


@attr.s
class _Start(_State):
    def _consume(self, item, text, pos):
        ch = text[pos]
        if ch.isalnum():
            item.before = self.spanned(text)
            self._next = _Attr()
            return False
        return True


@attr.s
class _End(_State):
    def _consume(self, item, text, pos):
        return True

    def _finalize(self, item, text):
        item.after = self.spanned(text)


@attr.s
class _Attr(_State):
    def _consume(self, item, text, pos):
        attr_preds = (
            lambda lhs: lhs.isalnum(),
            lambda lhs: lhs in '_.',
        )

        def _part_of_attr(lhs):
            return any(pred(lhs) for pred in attr_preds)

        ch = text[pos]
        if ch == ':':
            item.attribute = self.spanned(text)
            self._next = _Style()
            return True
        if not _part_of_attr(ch):
            item.attribute = self.spanned(text)
            self._next = _End()
            return False

        return True

    def _finalize(self, item, text):
        item.attribute = self.spanned(text)


@attr.s
class _Style(_State):
    def _consume(self, item, text, pos):
        style_preds = (
            lambda lhs: lhs.isalnum(),
            lambda lhs: lhs in '-_ .',
        )

        def _part_of_style(lhs):
            return any(pred(lhs) for pred in style_preds)

        ch = text[pos]
        if ch == ':':
            self._finalize(item, text)
            self._next = _Fmt()
            return True
        if not _part_of_style(ch):
            self._finalize(item, text)
            self._next = _End()
            return False

        return True

    def _finalize(self, item, text):
        item.style = self.spanned(text)


@attr.s
class _Fmt(_State):
    last_colon = attr.ib(None)
    first_end = attr.ib(None)

    def _consume(self, item, text, pos):
        style_preds = (
            lambda lhs: lhs.isalnum(),
            lambda lhs: lhs in '-_ ',
        )

        possible_ends = ' ]});|/\\'

        def _part_of_style(lhs):
            return any(pred(lhs) for pred in style_preds)

        ch = text[pos]
        if ch == ':':
            self.last_colon = pos
        elif self.first_end is None and ch in possible_ends:
            self.first_end = pos
        return True

    def _finalize(self, item, text):
        start, end = self.span

        if self.last_colon is not None:
            item.fmt = text[start:self.last_colon]
            item.after = text[self.last_colon + 1:end]  # exclude colon
        elif self.first_end is not None:
            item.fmt = text[start:self.first_end]
            item.after = text[self.first_end:end]  # include space
        else:
            item.fmt = self.spanned(text)


@attr.s
class Parser:
    '''Parser of task format markup'''
    _substs = attr.ib()
    _markup = attr.ib(factory=list)
    _nextsep = attr.ib(None)

    @property
    def markup(self):
        return self._markup

    def parse(self, text):
        if not text:
            return

        tokens = _SEPS.split(text)
        for token in tokens:
            if token == ',':
                self._nextsep = ' '
            elif token == '+':
                self._nextsep = None
            else:
                self._process_entry(token)

    def _add(self, text, style=''):
        if not text:
            return

        if style:
            style = 'class:{}'.format(style)

        if self._nextsep and self._markup:
            self._markup.append(('', self._nextsep))

        self._markup.append((style, text))

    def _process_entry(self, text):
        item = _Item()
        state = _Start()

        pos = 0
        while pos < len(text):
            if state.consume(item, text, pos):
                pos += 1
            if state.next():
                state = state.next()
        state.finalize(item, text)

        try:
            formatted = item.fmtspec.format_map(self._substs)
        except KeyError:
            return

        if formatted:
            processed = '{}{}{}'.format(item.before, formatted, item.after)
            self._add(processed, item.style)


def format_map(text, substitutions):
    parser = Parser(substitutions)
    parser.parse(text)
    return parser.markup


def format_(text, **kw):
    return format_map(text, kw)
