# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os

import tornado.web

from tornadoql.graphql_handler import GQLHandler
from tornadoql.subscription_handler import GQLSubscriptionHandler

PORT = 8888
PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(PATH, 'static')
SETTINGS = {
    'static_path': STATIC_PATH,
    'sockets': [],
    'subscriptions': {}
}


class GraphQLHandler(GQLHandler):
    @property
    def schema(self):
        return TornadoQL.schema


class GraphQLSubscriptionHandler(GQLSubscriptionHandler):

    def initialize(self, opts):
        super(GraphQLSubscriptionHandler, self).initialize()
        self.opts = opts

    @property
    def schema(self):
        return TornadoQL.schema

    @property
    def sockets(self):
        return self.opts['sockets']

    @property
    def subscriptions(self):
        return self.opts['subscriptions'].get(self, {})

    @subscriptions.setter
    def subscriptions(self, subscriptions):
        self.opts['subscriptions'][self] = subscriptions


class GraphiQLHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(STATIC_PATH, 'graphiql.html'))


class TornadoQL(object):
    schema = None
    endpoints = [
        (r'/subscriptions', GraphQLSubscriptionHandler, dict(opts=SETTINGS)),
        (r'/graphql', GraphQLHandler),
        (r'/graphiql', GraphiQLHandler)
    ]

    @staticmethod
    def start(schema, app_endpoints=None, port=PORT, settings=SETTINGS):
        if app_endpoints is None:
            app_endpoints = TornadoQL.endpoints

        TornadoQL.schema = schema
        app = tornado.web.Application(app_endpoints, **settings)

        print('Starting GraphQL server on %s' % port)
        print()
        print('  GraphiQL:              http://localhost:%s/graphiql' % port)
        print('  Queries and Mutations: http://localhost:%s/graphql' % port)
        print('  Subscriptions:         ws://localhost:%s/subscriptions' % port)
        print()
        app.listen(port)
        tornado.ioloop.IOLoop.current().start()
