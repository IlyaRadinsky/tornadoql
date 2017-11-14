# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import graphene
from rx.subjects import Subject


class RandomType(graphene.ObjectType):
    seconds = graphene.Int()
    random_int = graphene.Int()


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
    hello = graphene.String()

    def resolve_hello(self, info):
        return 'Hello from GraphQL!'


class Mutation(graphene.ObjectType):
    post = PostMutation.Field()


class Subscription(graphene.ObjectType):
    randomInt = graphene.Field(RandomType)
    onPost = graphene.Field(Message)

    def resolve_randomInt(root, info):
        import random
        return Observable.interval(1000)\
                         .map(lambda i: RandomType(seconds=i, random_int=random.randint(0, 500)))

    def resolve_onPost(root, info):
        return Storage.stream


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
