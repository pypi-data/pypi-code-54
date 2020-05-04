# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema_success[deleteMap] 1'] = {
    'data': {
        'deleteMap': {
            'ok': True
        }
    }
}

snapshots['test_schema_success[deleteMap] 2'] = {
    'data': {
        'map': None
    }
}

snapshots['test_schema_error[deleteMap-error] 1'] = {
    'data': {
        'deleteMap': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 11,
                    'line': 3
                }
            ],
            'message': "Class 'builtins.NoneType' is not mapped",
            'path': [
                'deleteMap'
            ]
        }
    ]
}

snapshots['test_schema_error[deleteMap-error] 2'] = {
    'data': {
        'allMaps': {
            'edges': [
                {
                    'node': {
                        'mapId': '1001',
                        'name': 'lat20190213'
                    }
                },
                {
                    'node': {
                        'mapId': '1012',
                        'name': 'lat20200120'
                    }
                },
                {
                    'node': {
                        'mapId': '1013',
                        'name': 'lat20200201'
                    }
                }
            ]
        }
    }
}
