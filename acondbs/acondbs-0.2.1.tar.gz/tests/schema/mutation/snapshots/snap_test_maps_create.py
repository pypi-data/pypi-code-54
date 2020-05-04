# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema_success[createMap-all-options] 1'] = {
    'data': {
        'createMap': {
            'map': {
                'name': 'map1'
            }
        }
    }
}

snapshots['test_schema_success[createMap-all-options] 2'] = {
    'data': {
        'map': {
            'beams': {
                'edges': [
                ]
            },
            'datePosted': '2020-02-20',
            'mapFilePaths': {
                'edges': [
                ]
            },
            'mapper': 'pwg-pmn',
            'name': 'map1',
            'note': '- Item 1'
        }
    }
}

snapshots['test_schema_success[createMap-selective-options] 1'] = {
    'data': {
        'createMap': {
            'map': {
                'name': 'map1'
            }
        }
    }
}

snapshots['test_schema_success[createMap-selective-options] 2'] = {
    'data': {
        'map': {
            'beams': {
                'edges': [
                ]
            },
            'datePosted': None,
            'mapFilePaths': {
                'edges': [
                ]
            },
            'mapper': 'pwg-pmn',
            'name': 'map1',
            'note': None
        }
    }
}

snapshots['test_schema_error[createMap-error-no-name] 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 30,
                    'line': 3
                }
            ],
            'message': '''Argument "input" has invalid value {mapper: "pwg-pmn"}.
In field "name": Expected "String!", found null.'''
        }
    ]
}

snapshots['test_schema_error[createMap-error-no-name] 2'] = {
    'data': {
        'map': None
    }
}
