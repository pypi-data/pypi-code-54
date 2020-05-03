# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from pysnap import Snapshot


snapshots = Snapshot()

snapshots['TestJestConfig.test_read[BIN] 1'] = {'/srv/unittests/node_modules/.bin/jest'}

snapshots['TestJestConfig.test_read[CONFIG_FILE] 1'] = {'jest.config.json'}

snapshots['TestJestConfig.test_read[CONFIG_FILE_PATH] 1'] = {'/srv/unittests/project/jest.config.json'}
