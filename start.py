import tornado.ioloop
import tornado.web

PORT = 8888

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello')

if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/', MainHandler),
    ])
    print('GraphQL server starting on %s' % PORT)
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
