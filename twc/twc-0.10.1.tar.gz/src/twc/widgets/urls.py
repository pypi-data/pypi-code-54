# Copyright (C) 2020 Michał Góral.
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

import re
import webbrowser

from prompt_toolkit.layout.screen import Point
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window, ScrollOffsets
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import to_formatted_text

from twc.consts import NL
from twc.utils import pprint, eprint, event_to_controller
from twc.locale import tr
from twc.task import Task


class OpenUrls:
    def __init__(self, element, cfg, controller):
        self.cfg = cfg
        self._pos = 0
        self.choices = _extract_urls(element)

        if not self.choices:
            eprint(tr('No URL found.'))
            return

        if len(self.choices) == 1:
            self.open(self.choices[0])
            return

        self.control = FormattedTextControl(
            self._get_text_fragments,
            get_cursor_position=lambda: Point(0, self.pos),
            key_bindings=self.keys(),
            focusable=True,
            show_cursor=False)

        self.window = Window(
            content=self.control,
            scroll_offsets=ScrollOffsets(top=1, bottom=1))

        controller.push(self)

    @classmethod
    def open(cls, url):
        pprint('Opening URL.')
        webbrowser.open(url, new=2)

    def keys(self):
        kb = KeyBindings()

        @self.cfg.command_handler('quit', kb)
        @event_to_controller
        def _(controller):
            if controller.stack and controller.stack[-1] is self:
                controller.pop()

        @self.cfg.command_handler('scroll.begin', kb)
        def _(event):
            self.pos = 0

        @self.cfg.command_handler('scroll.end', kb)
        def _(event):
            self.pos = len(self.choices) - 1

        @self.cfg.command_handler('scroll.down', kb)
        def _(event):
            self.pos += 1

        @self.cfg.command_handler('scroll.up', kb)
        def _(event):
            self.pos -= 1

        @self.cfg.command_handler('activate', kb)
        def _(event):
            url = self.choices[self.pos]
            self.open(url)

        return kb

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, val):
        if 0 <= val < len(self.choices):
            self._pos = val

    def _get_text_fragments(self):
        result = []
        for i, url in enumerate(self.choices):
            style = ''
            if i == self.pos:
                style = 'class:highlight'

            ft = to_formatted_text(url, style=style)
            result.extend(ft)
            result.append(NL)
        return result

    def __pt_container__(self):
        return self.window


def _extract_urls(lhs):
    expr = re.compile(r'(https?://[^\s]+)')
    if isinstance(lhs, Task):
        urls = expr.findall(lhs['description'])
        for ann in lhs.t['annotations']:
            urls.extend(expr.findall(ann['description']))
    elif isinstance(lhs, list):
        urls = []
        for elem in lhs:
            urls.extend(expr.findall(elem))
    elif isinstance(lhs, str):
        urls = expr.findall(lhs)
    else:
        urls = []
    return urls
