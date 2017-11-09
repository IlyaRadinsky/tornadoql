# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import graphene
import uuid


class Message(graphene.ObjectType):
    id = graphene.ID()
    userId = graphene.ID()
    msg = graphene.String()


class PostMutation(graphene.Mutation):
    class Arguments:
        userId = graphene.ID(required=True)
        msg = graphene.String(required=True)

    Output = Message

    def mutate(self, info, userId, msg):
        msg = Message(
            id=str(uuid.uuid4()),
            userId=userId,
            msg=msg
        )
        return msg


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return 'Hello from GraphQL!'


class Mutation(graphene.ObjectType):
    post = PostMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
