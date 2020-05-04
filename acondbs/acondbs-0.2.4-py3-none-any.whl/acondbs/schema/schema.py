import graphene

from .query import Query
from .mutation import Mutation

##__________________________________________________________________||
schema = graphene.Schema(query=Query, mutation=Mutation)

##__________________________________________________________________||
