import pytest
from graphene.test import Client

from acondbs.schema.schema import schema

##__________________________________________________________________||
params = [
    pytest.param(
        '''
          mutation m {
            updateMapFilePath(mapFilePathId: 1, input: {
              path: "nersc:/go/to/my/new_map_v2",
              note: "- Note 1 updated",
              mapId: 1012
            }) { mapFilePath { path } }
          }
        ''',
        '''
          {
            map(mapId: 1012) {
              name datePosted mapper note
              beams { edges { node { name } } }
              mapFilePaths { edges { node { path note map { mapId } } } }
            }
          }
        ''',
        id='updateMapFilePath'
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
