# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema_success[deleteMapFilePath] 1'] = {
    'data': {
        'deleteMapFilePath': {
            'ok': True
        }
    }
}

snapshots['test_schema_success[deleteMapFilePath] 2'] = {
    'data': {
        'map': {
            'beams': {
                'edges': [
                ]
            },
            'datePosted': '2019-02-13',
            'mapFilePaths': {
                'edges': [
                ]
            },
            'mapper': 'pwg-pmn',
            'name': 'lat20190213',
            'note': '''- This is a dummy test with a lat map
- This should not depend on any beam'''
        }
    }
}
