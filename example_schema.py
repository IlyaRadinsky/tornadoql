# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import graphene
from rx.subjects import Subject


class Message(graphene.ObjectType):
    id = graphene.ID()
    userId = graphene.ID()
    msg = graphene.String()


class Storage:
    stream = Subject()


class PostMutation(graphene.Mutation):
    class Arguments:
        userId = graphene.ID(required=True)
        msg = graphene.String(required=True)

    Output = Message

    def mutate(self, info, userId, msg):
        import uuid
        newMessage = Message(
            id=str(uuid.uuid4()),
            userId=userId,
            msg=msg
        )
        Storage.stream.on_next(newMessage)
        return newMessage


class Query(graphene.ObjectType):
    class Meta:
        description = 'Example query for TornadoQL'

    hello = graphene.String()

    def resolve_hello(self, info):
        return 'Hello from TornadoQL!'


class Mutation(graphene.ObjectType):
    class Meta:
        description = 'Example mutation for TornadoQL'

    post = PostMutation.Field()


class Subscription(graphene.ObjectType):
    class Meta:
        description = 'Example subscription for TornadoQL'

    onPost = graphene.Field(Message)

    def resolve_onPost(root, info):
        return Storage.stream


DEFAULT_SCHEMA = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
