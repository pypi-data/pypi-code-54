# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from pysnap import Snapshot


snapshots = Snapshot()

snapshots['TestBowerConfig.test_read[ARGS] 1'] = [
    '--config.interactive=false',
    '--allow-root'
]

snapshots['TestBowerConfig.test_read[BIN] 1'] = '/srv/unittests/node_modules/.bin/bower'

snapshots['TestBowerConfig.test_read[COMPONENTS_DIR] 1'] = '/srv/unittests/bower_components'

snapshots['TestBowerConfig.test_read[CONFIG_FILE] 1'] = 'bower.json'

snapshots['TestBowerConfig.test_read[CONFIG_FILE_PATH] 1'] = '/srv/unittests/project/bower.json'

snapshots['TestBowerConfig.test_read[DOCKERFILE] 1'] = 'Dockerfile.bower'

snapshots['TestBowerConfig.test_read[IMAGE] 1'] = 'docker.io/library/unittests:bower-27a022922e73344c316d657ad99710548617005cf8886fb16139237a21bf4d4f'

snapshots['TestBowerConfig.test_read[IMAGE_TAG] 1'] = 'bower-27a022922e73344c316d657ad99710548617005cf8886fb16139237a21bf4d4f'

snapshots['TestBowerConfig.test_read[MODULE_DIR] 1'] = '/opt/ixian_docker/ixian_docker/modules/bower'

snapshots['TestBowerConfig.test_read[REPOSITORY] 1'] = 'docker.io/library/unittests'
