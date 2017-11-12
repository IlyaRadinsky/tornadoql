# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os
import tornado.ioloop
import tornado.web
from graphql_handler import GQLHandler
from subscription_handler import GQLSubscriptionHandler
from schema import schema


PORT = 8888
PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(PATH, 'static')

SETTINGS = {
    'static_path': STATIC_PATH,
    'sockets': []
}


class GraphQLHandler(GQLHandler):
    @property
    def schema(self):
        return schema


class GraphQLSubscriptionHandler(GQLSubscriptionHandler):

    def initialize(self, opts):
        super(GraphQLSubscriptionHandler, self).initialize()
        self.opts = opts

    @property
    def schema(self):
        return schema

    @property
    def sockets(self):
        return self.opts['sockets']


class GraphiQLHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(STATIC_PATH, 'graphiql.html'))


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/subscriptions', GraphQLSubscriptionHandler, dict(opts=SETTINGS)),
        (r'/graphql', GraphQLHandler),
        (r'/graphiql', GraphiQLHandler)
    ], **SETTINGS)
    print('GraphQL server starting on %s' % PORT)
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
