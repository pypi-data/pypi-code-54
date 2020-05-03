# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from pysnap import Snapshot


snapshots = Snapshot()

snapshots['TestPythonConfig.test_read[BIN] 1'] = 'python3'

snapshots['TestPythonConfig.test_read[DOCKERFILE] 1'] = 'Dockerfile.python'

snapshots['TestPythonConfig.test_read[HOST_ROOT_MODULE_PATH] 1'] = '/opt/ixian_docker/unittests'

snapshots['TestPythonConfig.test_read[IMAGE] 1'] = 'docker.io/library/unittests:python-bce5ccc9ee5195735bc4ed1308361650fd3d7e44cf931ac9860b5a73bfc11735'

snapshots['TestPythonConfig.test_read[IMAGE_TAG] 1'] = 'python-bce5ccc9ee5195735bc4ed1308361650fd3d7e44cf931ac9860b5a73bfc11735'

snapshots['TestPythonConfig.test_read[REPOSITORY] 1'] = 'docker.io/library/unittests'

snapshots['TestPythonConfig.test_read[REQUIREMENTS] 1'] = 'requirements*.txt'

snapshots['TestPythonConfig.test_read[ROOT_MODULE] 1'] = 'unittests'

snapshots['TestPythonConfig.test_read[ROOT_MODULE_PATH] 1'] = '/srv/unittests/project/unittests'

snapshots['TestPythonConfig.test_read[VIRTUAL_ENV] 1'] = '.venv'

snapshots['TestPythonConfig.test_read[VIRTUAL_ENV_DIR] 1'] = '/srv/unittests/.venv'

snapshots['TestPythonConfig.test_read[VIRTUAL_ENV_RUN] 1'] = 'python3'

snapshots['TestPythonConfig.test_read[MODULE_DIR] 1'] = '/opt/ixian_docker/ixian_docker/modules/python'
