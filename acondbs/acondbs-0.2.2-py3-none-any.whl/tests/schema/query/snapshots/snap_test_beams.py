# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema[beamByBeamID] 1'] = {
    'data': {
        'beam': {
            'name': '20180101'
        }
    }
}

snapshots['test_schema[beamByBeamID-nonexistent] 1'] = {
    'data': {
        'beam': None
    }
}

snapshots['test_schema[beamByName] 1'] = {
    'data': {
        'beam': {
            'beamId': '1010'
        }
    }
}
