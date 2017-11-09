import os
import tornado.ioloop
import tornado.web
from GQLHandler import GQLHandler
from schema import schema

PORT = 8888

class GraphQLHandler(GQLHandler):
    @property
    def schema(self):
        return schema

if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/graphql', GraphQLHandler),
    ])
    print('GraphQL server starting on %s' % PORT)
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
