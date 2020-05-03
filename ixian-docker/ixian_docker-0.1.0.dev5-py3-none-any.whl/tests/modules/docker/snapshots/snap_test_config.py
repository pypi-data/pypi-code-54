# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from pysnap import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['TestDockerConfig.test_read[APP_BIN] 1'] = '/srv/unittests/bin'

snapshots['TestDockerConfig.test_read[APP_DIR] 1'] = '/srv/unittests'

snapshots['TestDockerConfig.test_read[BASE_IMAGE] 1'] = 'docker.io/library/unittests:base-44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'

snapshots['TestDockerConfig.test_read[BASE_IMAGE_FILES] 1'] = [
]

snapshots['TestDockerConfig.test_read[BASE_IMAGE_HASH] 1'] = '44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'

snapshots['TestDockerConfig.test_read[BASE_IMAGE_TAG] 1'] = 'base-44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'

snapshots['TestDockerConfig.test_read[COMPOSE_FLAGS] 1'] = [
    '--rm',
    '-u root'
]

snapshots['TestDockerConfig.test_read[DEFAULT_APP] 1'] = 'app'

snapshots['TestDockerConfig.test_read[DEV_VOLUMES] 1'] = [
    '{PWD}:{DOCKER.PROJECT_DIR}',
    '{BUILDER}/.bash_history:{DOCKER.HOME_DIR}/.bash_history',
    '{PWD}/bin/:{DOCKER.APP_DIR}/bin',
    '{PWD}/.env:{DOCKER.APP_DIR}/.env'
]

snapshots['TestDockerConfig.test_read[DEV_ENV] 1'] = {
}

snapshots['TestDockerConfig.test_read[DOCKERFILE] 1'] = 'Dockerfile'

snapshots['TestDockerConfig.test_read[DOCKERFILE_BASE] 1'] = 'Dockerfile.base'

snapshots['TestDockerConfig.test_read[DOCKERFILE_TEMPLATE] 1'] = '/opt/ixian_docker/ixian_docker/modules/docker/Dockerfile.template'

snapshots['TestDockerConfig.test_read[ENV] 1'] = {
}

snapshots['TestDockerConfig.test_read[ENV_DIR] 1'] = '/srv'

snapshots['TestDockerConfig.test_read[HOME_DIR] 1'] = '/root'

snapshots['TestDockerConfig.test_read[IMAGE_TAG] 1'] = 'runtime-f6872898d76287a682ed1db15cd0c3344202935a88d858ef51f54aca0ed8e8b2'

snapshots['TestDockerConfig.test_read[MODULE_CONTEXT] 1'] = '.builder/module_context'

snapshots['TestDockerConfig.test_read[MODULE_DIR] 1'] = '/opt/ixian_docker/ixian_docker/modules/docker'

snapshots['TestDockerConfig.test_read[PROJECT_DIR] 1'] = '/srv/unittests/project'

snapshots['TestDockerConfig.test_read[REGISTRY] 1'] = 'docker.io'

snapshots['TestDockerConfig.test_read[REGISTRY_PATH] 1'] = 'library'

snapshots['TestDockerConfig.test_read[REPOSITORY] 1'] = 'docker.io/library/unittests'

snapshots['TestDockerConfig.test_read[ROOT_MODULE_DIR] 1'] = '/opt/ixian_docker/ixian_docker'

snapshots['TestDockerConfig.test_read[VOLUMES] 1'] = [
]

snapshots['TestDockerConfig.test_read[IMAGE] 1'] = 'docker.io/library/unittests:runtime-8db14905ba6cef58ab7d6732db7f156a540647aba67998a752e17e8b12dbfc7d'

snapshots['TestDockerConfig.test_task_hash 1'] = GenericRepr('<ixian.config.TaskConfig object at 0x100000000>')

snapshots['TestDockerConfig.test_task_hash 2'] = GenericRepr('<ixian.config.TaskConfig object at 0x100000000>')
