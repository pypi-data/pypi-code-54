# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema[allSimulations] 1'] = {
    'data': {
        'allSimulations': {
            'edges': [
                {
                    'node': {
                        'name': 'xyz-s1234-20200101'
                    }
                }
            ]
        }
    }
}

snapshots['test_schema[simulationBySimulationID] 1'] = {
    'data': {
        'simulation': {
            'name': 'xyz-s1234-20200101'
        }
    }
}

snapshots['test_schema[simulationBySimulationID-nonexistent] 1'] = {
    'data': {
        'simulation': None
    }
}
