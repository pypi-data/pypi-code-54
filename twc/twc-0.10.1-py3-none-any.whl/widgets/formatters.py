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

import attr

from twc.utils import eprint
from twc.locale import tr


@attr.s
class TaskFlags:
    @attr.s
    class _FlagInfo:
        attrname = attr.ib()
        char = attr.ib()

    _task = attr.ib()

    _FLAGMAP = {
        '%a': _FlagInfo('annotations', 'A'),
        '%d': _FlagInfo('due', 'D'),
        '%s': _FlagInfo('scheduled', 'S'),
        '%t': _FlagInfo('tags', 'T'),
    }

    def __getitem__(self, name):
        # A hack to avoid passing flags wrapped in a one element dict
        if name != 'flags':
            raise KeyError(name)
        return self

    def __format__(self, spec):
        if not self._task:
            return ''
        if not spec:
            spec = '%s%d%a'

        return re.sub(r'(%[a-z])', self._flag, spec)

    def _flag(self, matchobj):
        flag = matchobj.group(1)
        info = self._FLAGMAP.get(flag)
        if info is None:
            eprint(tr('Invalid flag format: {}'.format(flag)))
            return ''

        if self._task[info.attrname]:
            return info.char
        return ''


class _TaskAttrGetter:
    def __init__(self, task, default=''):
        self._t = task
        self._default = ''

    def __getattr__(self, name):
        if name.startswith('_'):
            return self.__dict__[name]
        if not self._t:
            return self._default
        return self._t[name]


@attr.s
class AgendaStatus:
    _pos = attr.ib(0)  # highlighted item's position
    size = attr.ib(0)   # size of current agenda

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new):
        self._pos = new + 1

    @property
    def ppos(self):
        if self.size < 1:
            return 0
        return 100 * self.pos // self.size


@attr.s
class Statuses:
    taskrc = attr.ib('')  # path to used taskrc
    command = attr.ib('')  # current command

    _task = attr.ib(None)  # highlighted task
    _agenda = attr.ib(factory=AgendaStatus)  # current agenda status

    @property
    def task(self):
        return _TaskAttrGetter(self._task)

    @task.setter
    def task(self, task):
        self._task = task

    @property
    def agenda(self):
        return self._agenda

    @agenda.setter
    def agenda(self, new):
        self._agenda.pos = new.pos
        self._agenda.size = new.size

    # TODO: Maybe this should be available via task.flags?
    # (in _TaskAttrGetter?) (mg, 2020-03-27)
    @property
    def flags(self):
        if self._task:
            return TaskFlags(self._task.t)
        return TaskFlags(None)

    @property
    def COMMAND(self):
        return self.command.upper()

    def __getitem__(self, name):
        return getattr(self, name)
