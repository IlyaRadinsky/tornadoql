# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os
import tornado.ioloop
import tornado.web
from graphql_handler import GQLHandler
from schema import schema


PORT = 8888
PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(PATH, 'static')

SETTINGS = {
    'static_path': STATIC_PATH,
}


class GraphQLHandler(GQLHandler):
    @property
    def schema(self):
        return schema


class GraphiQLHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(STATIC_PATH, 'graphiql.html'))


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/graphql', GraphQLHandler),
        (r'/graphiql', GraphiQLHandler)
    ], **SETTINGS)
    print('GraphQL server starting on %s' % PORT)
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
