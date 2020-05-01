# Copyright (C) 2020 Michał Góral.
#
# This file is part of TWC
#
# TWC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.  TWC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TWC. If not, see <http://www.gnu.org/licenses/>.

# Keep this text width <80 characters
_HELP_TEXT = '''
TWC is an interactive interface for TaskWarrior: a task/todo management
application.

This is a built-in short reference. It is not a comprehensive documentation
(see manual under link below or docs directory if source tree).

Full documentation:  https://mgoral.gitlab.io/twc
Source code:         https://gitlab.com/mgoral/twc

Configured keys
---------------

{keys}

Configuration
-------------

TWC follows XDG Base Directory Specification for finding configuration files.
Typically it means that you should create ~/.config/twc/config.py configuration
file.

Configuration files are ordinary Python scripts which are loaded with exposed
variable "c", which should be used to configure all aspects of TWC.

config.py example:

    # set some settings via c.set()
    c.set('incsearch', False)
    c.set('taskrc', '~/other_taskrc')

    # change appearence of twc
    c.set_style('comment', 'fg:lightblue bold')

    # change default bindings
    c.bind('r', 'refresh')
    c.bind('d d', 'task.delete')

    # Set up a single agenda with two blocks (TaskWarrior queries/filters).
    # Agendas are created automatically when a block is assigned to any
    # unexisting agenda with c.add_block(agenda='<name>').

    displayed_items = 'priority:warning:,description,id:comment:,tags:info:'

    c.add_block(
        agenda='My Tasks',
        title='Tasks with tag1 or tag2',
        filter='-WAITING -BLOCKING -BLOCKED +PENDING (+tag1 or +tag2)',
        items=displayed_items,
        sort='urgency-,priority')

    c.add_block(
        agenda='My Tasks',
        title='Inbox',
        filter='( status:pending tags.is: )',
        items=displayed_items)
'''


def _revert_alt(keys):
    '''TWC automatically changes a-key to a sequence of esc + key, because
    that's how shells work. We have to revert this, because it's internal
    implementation detail.'''
    if len(keys) > 1 and keys[0] == 'escape':
        return 'a-{}'.format(''.join(keys[1:]))
    return keys


def _formatted_keylist(commands):
    listing = []
    for cmd in sorted(commands):
        bindings = ', '.join(''.join(_revert_alt(seq)) for seq in commands[cmd])
        listing.append('  {:.<27} {}'.format(cmd + ' ', bindings))
    return listing


def helptext(commands):
    listing = _formatted_keylist(commands)
    return _HELP_TEXT.format(keys='\n'.join(listing))
