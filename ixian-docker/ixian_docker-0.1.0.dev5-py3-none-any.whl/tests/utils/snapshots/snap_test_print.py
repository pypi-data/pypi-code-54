# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from pysnap import Snapshot


snapshots = Snapshot()

snapshots['test_print 1'] = '''

\x1b[2A\r\x1b[1B\r\x1b[1B\r\x1b[1A\r\x1b[1A\r\x1b[2B\r\x1b[2A\r\x1b[2B\r\x1b[2A\r\x1b[2B\r
\x1b[2A\r\x1b[2B\r
\x1b[4A\r1\x1b[K\r\x1b[1B\r2\x1b[K\r\x1b[1B\r3\x1b[K\r\x1b[1B\r4\x1b[K\r\x1b[1B\r5\x1b[K\r\x1b[4A\r11\x1b[K\r111\x1b[K\r1111\x1b[K\r\x1b[4B\r5555\x1b[K\r\x1b[3A\r2222\x1b[K\r\x1b[2B\r4444\x1b[K\r\x1b[1A\r3333\x1b[K\r\x1b[3B\r'''
