import pytest
from graphene.test import Client

from acondbs.schema.schema import schema

##__________________________________________________________________||
params = [
    pytest.param(
        '''
        { beam(beamId: 1010) { name } }
         ''',
        id='beamByBeamID'
    ),
    pytest.param(
        '''
        { beam(beamId: 2001) { name } }
         ''',
        id='beamByBeamID-nonexistent'
    ),
    pytest.param(
        '''
        { beam(name: "20180101") { beamId } }
         ''',
        id='beamByName'
    ),
]

@pytest.mark.parametrize('query', params)
def test_schema(app, snapshot, query):
    client = Client(schema)
    with app.app_context():
        snapshot.assert_match(client.execute(query))

##__________________________________________________________________||
