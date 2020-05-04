import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import BeamFilePath as BeamFilePathModel

from ..db.sa import sa

##__________________________________________________________________||
class BeamFilePath(SQLAlchemyObjectType):
    class Meta:
        model = BeamFilePathModel
        interfaces = (relay.Node, )

##__________________________________________________________________||
