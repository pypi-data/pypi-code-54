import pytest
from graphene.test import Client

from acondbs.schema.schema import schema

##__________________________________________________________________||
params = [
    pytest.param(
        '''
        mutation m {
          deleteMap(mapId: 1001) { ok }
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
        id='deleteMap'
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
params = [
    pytest.param(
        '''
        mutation m {
          deleteMap(mapId: 512) { ok }
        }
         ''',
        '''
          {
            allMaps {
              edges {
                node {
                  mapId
                  name
                }
              }
            }
          }
        ''',
        id='deleteMap-error'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_error(app, snapshot, mutation, query, mock_request_backup_db):
    client = Client(schema)
    with app.app_context():
        snapshot.assert_match(client.execute(mutation))
    with app.app_context():
        snapshot.assert_match(client.execute(query))
    assert 0 == mock_request_backup_db.call_count

##__________________________________________________________________||
