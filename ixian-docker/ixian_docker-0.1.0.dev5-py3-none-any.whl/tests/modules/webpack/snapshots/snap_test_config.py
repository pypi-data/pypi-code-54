# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from pysnap import Snapshot


snapshots = Snapshot()

snapshots['TestConfig.test_read[ARGS] 1'] = [
    '--progress',
    '--colors',
    '--config {WEBPACK.CONFIG_FILE_PATH}',
    '--output-path {WEBPACK.COMPILED_STATIC_DIR}'
]

snapshots['TestConfig.test_read[COMPILED_STATIC_DIR] 1'] = '/srv/unittests/compiled_static'

snapshots['TestConfig.test_read[CONFIG_FILE] 1'] = 'webpack.config.js'

snapshots['TestConfig.test_read[CONFIG_FILE_PATH] 1'] = '/srv/unittests/project/webpack.config.js'

snapshots['TestConfig.test_read[DOCKERFILE] 1'] = 'Dockerfile.webpack'

snapshots['TestConfig.test_read[IMAGE] 1'] = 'docker.io/library/unittests:webpack-a48d3cf9e533b626854b657b88eaf0cdb2ff01e78947640e68f3558d4037c7d7'

snapshots['TestConfig.test_read[IMAGE_TAG] 1'] = 'webpack-a48d3cf9e533b626854b657b88eaf0cdb2ff01e78947640e68f3558d4037c7d7'

snapshots['TestConfig.test_read[MODULE_DIR] 1'] = '/opt/ixian_docker/ixian_docker/modules/webpack'

snapshots['TestConfig.test_read[REPOSITORY] 1'] = 'docker.io/library/unittests'

snapshots['TestConfig.test_read[SOURCE_DIRS] 1'] = [
    'static'
]
