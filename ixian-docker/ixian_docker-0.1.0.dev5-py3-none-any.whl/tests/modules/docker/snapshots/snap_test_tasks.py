# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from pysnap import Snapshot


snapshots = Snapshot()

snapshots['TestCleanDocker.test_help 1'] = '''
\x1b[90m[exec] help(clean_docker) force=False clean=False\x1b[0m
\x1b[1mNAME
\x1b[0m    clean_docker -- 
\x1b[1m
DESCRIPTION
\x1b[0m
    Clean Docker:
        - kill and remove all containers
    \x1b[1m

STATUS
\x1b[0m\x1b[90m○\x1b[0m clean_docker

\x1b[90m[fini] help\x1b[0m
'''

snapshots['TestCleanDocker.test_help 2'] = '''
'''

snapshots['TestBuildBaseImage.test_help 1'] = '''
\x1b[90m[exec] help(build_base_image) force=False clean=False\x1b[0m
\x1b[1mNAME
\x1b[0m    build_base_image -- Build app image
\x1b[1m
DESCRIPTION
\x1b[0mBuilds the docker app image using CONFIG.DOCKER_FILE\x1b[1m

STATUS
\x1b[0m\x1b[90m○\x1b[0m build_base_image

\x1b[90m[fini] help\x1b[0m
'''

snapshots['TestBuildBaseImage.test_help 2'] = '''
'''

snapshots['TestBuildBaseImage.test_execute[image_exists] 1'] = '''
\x1b[90m[exec] build_base_image() force=False clean=False\x1b[0m
\x1b[90mAttempting to build docker.io/library/unittests:base-44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a\x1b[0m
\x1b[90mImage exists, skipping build.\x1b[0m
\x1b[90m[fini] build_base_image\x1b[0m
'''

snapshots['TestBuildBaseImage.test_execute[image_exists] 2'] = '''
'''

snapshots['TestBuildBaseImage.test_execute[image_exists] 3'] = [
    (
        (
            'docker.io/library/unittests:base-44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'
        ,),
        {
        }
    ,)
]

snapshots['TestBuildBaseImage.test_execute[image_exists] 4'] = [
]

snapshots['TestBuildBaseImage.test_execute[image_exists] 5'] = [
]

snapshots['TestBuildBaseImage.test_execute[image_exists_local] 1'] = '''
\x1b[90m[exec] build_base_image() force=False clean=False\x1b[0m
\x1b[90mAttempting to build docker.io/library/unittests:base-44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a\x1b[0m
\x1b[90mImage exists, skipping build.\x1b[0m
\x1b[90m[fini] build_base_image\x1b[0m
'''

snapshots['TestBuildBaseImage.test_execute[image_exists_local] 2'] = '''
'''

snapshots['TestBuildBaseImage.test_execute[image_exists_local] 3'] = [
    (
        (
            'docker.io/library/unittests:base-44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'
        ,),
        {
        }
    ,)
]

snapshots['TestBuildBaseImage.test_execute[image_exists_local] 4'] = [
]

snapshots['TestBuildBaseImage.test_execute[image_exists_local] 5'] = [
]

snapshots['TestBuildBaseImage.test_execute[pull_image] 1'] = '''
\x1b[90m[exec] build_base_image() force=False clean=False\x1b[0m
\x1b[90mAttempting to build docker.io/library/unittests:base-44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a\x1b[0m
\x1b[90mImage does not exist.\x1b[0m
\x1b[90mImage exists on registry. Pulling image.\x1b[0m
\x1b[90mImage pulled.\x1b[0m
\x1b[90mCheck passed, skipping build.\x1b[0m
\x1b[90m[fini] build_base_image\x1b[0m
'''

snapshots['TestBuildBaseImage.test_execute[pull_image] 2'] = '''
'''

snapshots['TestBuildBaseImage.test_execute[pull_image] 3'] = [
    (
        (
            'docker.io/library/unittests:base-44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'
        ,),
        {
        }
    ,)
]

snapshots['TestBuildBaseImage.test_execute[pull_image] 4'] = [
    (
        (
            'docker.io/library/unittests',
            'base-44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'
        ,),
        {
        }
    ,)
]

snapshots['TestBuildBaseImage.test_execute[pull_image] 5'] = [
    (
        (
            'docker.io/library/unittests',
            'base-44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'
        ,),
        {
        }
    ,)
]
