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

from prompt_toolkit.layout.screen import Point
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window, ScrollOffsets
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import to_formatted_text

from twc.widgets.urls import OpenUrls
from twc.utils import event_to_controller
from twc.consts import NL


class TextView:
    def __init__(self, text, cfg):
        self.text = text
        self.cfg = cfg
        self._pos = 0

        self.control = FormattedTextControl(
            self._get_text_fragments,
            get_cursor_position=lambda: Point(0, self.pos),
            key_bindings=self.keys(),
            focusable=True,
            show_cursor=False)

        self.window = Window(
            content=self.control,
            scroll_offsets=ScrollOffsets(top=1, bottom=1),
            wrap_lines=True)

    def keys(self):
        kb = KeyBindings()

        @self.cfg.command_handler('quit', kb)
        @event_to_controller
        def _(controller):
            if controller.stack and controller.stack[-1] is self:
                controller.pop()

        @self.cfg.command_handler('scroll.down', kb)
        def _(event):
            info = self.window.render_info
            height = info.window_height
            vs = info.vertical_scroll

            # substract 1 due to scroll offsets
            self.pos = vs + height - 1

        @self.cfg.command_handler('scroll.up', kb)
        def _(event):
            info = self.window.render_info
            vs = info.vertical_scroll

            # don't add 1 due to scroll offsets
            self.pos = vs

        @self.cfg.command_handler('scroll.begin', kb)
        def _(event):
            self.pos = 0

        @self.cfg.command_handler('scroll.end', kb)
        def _(event):
            self.pos = len(self.text) - 1

        @self.cfg.command_handler('followurl', kb)
        @event_to_controller
        def _(controller):
            OpenUrls(self.text, self.cfg, controller)

        return kb

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, val):
        if 0 <= val < len(self.text):
            self._pos = val

    def _get_text_fragments(self):
        result = []
        for line in self.text:
            ft = to_formatted_text(line)
            result.extend(ft)
            result.append(NL)
        return result

    def __pt_container__(self):
        return self.window
