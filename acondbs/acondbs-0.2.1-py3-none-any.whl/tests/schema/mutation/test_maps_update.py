import pytest
from graphene.test import Client

from acondbs.schema.schema import schema

##__________________________________________________________________||
params = [
    pytest.param(
        '''
        mutation m {
          updateMap(mapId: 1001, input: {
              name: "new-name"
              datePosted: "2020-02-18",
              mapper: "pwg-xyz",
              note: "- Note 123"
          }) {
            map { mapId name } }
        }
         ''',
        '''
          {
            map(mapId: 1001) {
              name datePosted mapper note
              beams { edges { node { name } } }
              mapFilePaths { edges { node { path } } }
            }
          }
        ''',
        id='updateMap-all-options'
    ),
    pytest.param(
        '''
        mutation m {
          updateMap(mapId: 1001, input: {
              name: "new-name"
              mapper: "pwg-xyz",
          }) {
            map { mapId name } }
        }
         ''',
        '''
          {
            map(mapId: 1001) {
              name datePosted mapper note
              beams { edges { node { name } } }
              mapFilePaths { edges { node { path } } }
            }
          }
        ''',
        id='updateMap-selective-options'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_success(app, snapshot, mutation, query, mock_request_backup_db):
    client = Client(schema)
    with app.app_context():
        snapshot.assert_match(client.execute(mutation))
    with app.app_context():
        snapshot.assert_match(client.execute(query))
    assert 1 == mock_request_backup_db.call_count

##__________________________________________________________________||
