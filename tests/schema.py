import graphene

from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

import graphql_jwt


class UserNode(DjangoObjectType):

    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    user = graphene.Field(UserNode)


class Mutations(graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
