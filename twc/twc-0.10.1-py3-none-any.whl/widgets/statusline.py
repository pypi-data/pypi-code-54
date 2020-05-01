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

from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import (
    Window,
    WindowAlign,
    VSplit,
    ConditionalContainer,
)

import twc.markup as markup
from twc.widgets.formatters import Statuses


class StatusLine:
    def __init__(self, tw, cfg):
        self.tw = tw
        self.cfg = cfg
        self.enabled = bool(
            self.cfg.settings.statusleft
            and self.cfg.settings.statusright)
        self.infos = Statuses()

        self.infos.taskrc = self.tw.taskrc_location

        self.left = FormattedTextControl(
            lambda: self.items(self.cfg.settings.statusleft),
            focusable=False,
            show_cursor=False)

        self.right = FormattedTextControl(
            lambda: self.items(self.cfg.settings.statusright),
            focusable=False,
            show_cursor=False)

        self.window = ConditionalContainer(
            content=VSplit([
                Window(
                    content=self.left,
                    height=1,
                    style='class:statusline'),
                Window(
                    content=self.right,
                    align=WindowAlign.RIGHT,
                    height=1,
                    dont_extend_width=True,
                    style='class:statusline')]),
            filter=self.enabled)

    def connect_to_signals(self, controller):
        agendaview = controller.agendaview
        commandline = controller.commandline

        agendaview.scrolled.connect(
            self._agenda_scrolled,
            agendaview=agendaview)

        agendaview.agenda_changed.connect(
            self._agenda_changed,
            agendaview=agendaview)

        commandline.command_name_changed.connect(self._command_changed)

    def items(self, fmt):
        if not self.enabled:
            return []

        return markup.format_map(fmt, self.infos)

    def _agenda_changed(self, _, agendaview):
        self.infos.agenda = agendaview

    def _agenda_scrolled(self, pos, agendaview):
        self.infos.agenda.pos = pos
        self.infos.task = agendaview.current_task

    def _command_changed(self, name):
        self.infos.command = name

    def __pt_container__(self):
        return self.window
