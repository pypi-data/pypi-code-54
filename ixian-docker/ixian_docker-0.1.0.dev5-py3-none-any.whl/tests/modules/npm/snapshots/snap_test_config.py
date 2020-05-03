# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from pysnap import Snapshot


snapshots = Snapshot()

snapshots['TestNPMConfig.test_read[DOCKERFILE] 1'] = 'Dockerfile.npm'

snapshots['TestNPMConfig.test_read[DOCKERFILE_TEMPLATE] 1'] = '/opt/ixian_docker/ixian_docker/modules/npm/Dockerfile.template'

snapshots['TestNPMConfig.test_read[IMAGE] 1'] = 'docker.io/library/unittests:npm-27a022922e73344c316d657ad99710548617005cf8886fb16139237a21bf4d4f'

snapshots['TestNPMConfig.test_read[IMAGE_TAG] 1'] = 'npm-27a022922e73344c316d657ad99710548617005cf8886fb16139237a21bf4d4f'

snapshots['TestNPMConfig.test_read[MODULE_DIR] 1'] = '/opt/ixian_docker/ixian_docker/modules/npm'

snapshots['TestNPMConfig.test_read[NODE_MODULES_DIR] 1'] = '/srv/unittests/node_modules'

snapshots['TestNPMConfig.test_read[PACKAGE_JSON] 1'] = 'package.json'

snapshots['TestNPMConfig.test_read[REPOSITORY] 1'] = 'docker.io/library/unittests'
