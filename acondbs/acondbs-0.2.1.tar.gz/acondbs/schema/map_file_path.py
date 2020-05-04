import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import MapFilePath as MapFilePathModel

from ..db.sa import sa
from ..db.backup import request_backup_db

##__________________________________________________________________||
class MapFilePath(SQLAlchemyObjectType):
    class Meta:
        model = MapFilePathModel
        interfaces = (relay.Node, )

##__________________________________________________________________||
class MapFilePathAttribute:
    path = graphene.String()
    note = graphene.String()
    map_id = graphene.Int()

class CreateMapFilePathInput(graphene.InputObjectType, MapFilePathAttribute):
    pass

class UpdateMapFilePathInput(graphene.InputObjectType, MapFilePathAttribute):
    pass

class CreateMapFilePath(graphene.Mutation):
    class Arguments:
        input = CreateMapFilePathInput(required=True)

    ok = graphene.Boolean()
    mapFilePath = graphene.Field(lambda: MapFilePath)

    def mutate(root, info, input):
        mapFilePath = MapFilePathModel(**input)
        sa.session.add(mapFilePath)
        sa.session.commit()
        ok = True
        request_backup_db()
        return CreateMapFilePath(mapFilePath=mapFilePath, ok=ok)

class UpdateMapFilePath(graphene.Mutation):
    class Arguments:
        map_file_path_id = graphene.Int()
        input = UpdateMapFilePathInput(required=True)

    ok = graphene.Boolean()
    mapFilePath = graphene.Field(lambda: MapFilePath)

    def mutate(root, info, map_file_path_id, input):
        mapFilePath = MapFilePathModel.query.filter_by(map_file_path_id=map_file_path_id).first()
        for k, v in input.items():
            setattr(mapFilePath, k, v)
        sa.session.commit()
        ok = True
        request_backup_db()
        return UpdateMapFilePath(mapFilePath=mapFilePath, ok=ok)

class DeleteMapFilePath(graphene.Mutation):
    class Arguments:
        map_file_path_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(root, info, map_file_path_id):
        mapFilePath = MapFilePathModel.query.filter_by(map_file_path_id=map_file_path_id).first()
        sa.session.delete(mapFilePath)
        sa.session.commit()
        ok = True
        request_backup_db()
        return DeleteMapFilePath(ok=ok)

##__________________________________________________________________||
