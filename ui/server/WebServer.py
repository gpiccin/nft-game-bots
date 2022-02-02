import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class WebServer:
    def __init__(self) -> None:
        pass

    def start(self):
        app = self.create_routes()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()

    def create_routes(self):
        return tornado.web.Application([
            (r"/", MainHandler),
        ])