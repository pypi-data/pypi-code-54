# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from pysnap import Snapshot


snapshots = Snapshot()

snapshots['TestDjangoConfig.test_read[HOST] 1'] = {
    'field': '0.0.0.0'
}

snapshots['TestDjangoConfig.test_read[MODULE_DIR] 1'] = {
    'field': '/opt/ixian_docker/ixian_docker/modules/django'
}

snapshots['TestDjangoConfig.test_read[PORT] 1'] = {
    'field': '8000'
}

snapshots['TestDjangoConfig.test_read[SETTINGS_DIR] 1'] = {
    'field': 'unittests/settings'
}

snapshots['TestDjangoConfig.test_read[SETTINGS_MODULE] 1'] = {
    'field': 'unittests.settings'
}

snapshots['TestDjangoConfig.test_read[SETTINGS_FILE] 1'] = {
    'field': 'unittests.settings.base'
}

snapshots['TestDjangoConfig.test_read[SETTINGS_TEST] 1'] = {
    'field': 'unittests.settings.test'
}

snapshots['TestDjangoConfig.test_read[UWSGI_INI] 1'] = {
    'field': 'uwsgi.ini'
}
