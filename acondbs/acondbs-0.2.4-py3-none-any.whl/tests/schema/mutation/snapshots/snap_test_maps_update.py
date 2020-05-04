# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema_success[updateMap-all-options] 1'] = {
    'data': {
        'updateMap': {
            'map': {
                'mapId': '1001',
                'name': 'new-name'
            }
        }
    }
}

snapshots['test_schema_success[updateMap-all-options] 2'] = {
    'data': {
        'map': {
            'beams': {
                'edges': [
                ]
            },
            'datePosted': '2020-02-18',
            'mapFilePaths': {
                'edges': [
                    {
                        'node': {
                            'path': 'nersc:/go/to/my/maps'
                        }
                    }
                ]
            },
            'mapper': 'pwg-xyz',
            'name': 'new-name',
            'note': '- Note 123'
        }
    }
}

snapshots['test_schema_success[updateMap-selective-options] 1'] = {
    'data': {
        'updateMap': {
            'map': {
                'mapId': '1001',
                'name': 'new-name'
            }
        }
    }
}

snapshots['test_schema_success[updateMap-selective-options] 2'] = {
    'data': {
        'map': {
            'beams': {
                'edges': [
                ]
            },
            'datePosted': '2019-02-13',
            'mapFilePaths': {
                'edges': [
                    {
                        'node': {
                            'path': 'nersc:/go/to/my/maps'
                        }
                    }
                ]
            },
            'mapper': 'pwg-xyz',
            'name': 'new-name',
            'note': '''- This is a dummy test with a lat map
- This should not depend on any beam'''
        }
    }
}
