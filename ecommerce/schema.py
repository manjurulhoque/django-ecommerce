import graphene
from graphene_django.debug import DjangoDebug

from core.graphql import queries as product_queries


class Query(
    product_queries.ProductQuery,
    product_queries.CategoryQuery,
    graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
