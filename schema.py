# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import graphene
from rx import Observable


class RandomType(graphene.ObjectType):
    seconds = graphene.Int()
    random_int = graphene.Int()


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
        import uuid
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


class Subscription(graphene.ObjectType):
    random_int = graphene.Field(RandomType)

    def resolve_random_int(root, info):
        import random
        return Observable.interval(1000)\
                         .map(lambda i: RandomType(seconds=i, random_int=random.randint(0, 500)))



schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
