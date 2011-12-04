import os
import tornado.ioloop
import tornado.web
import json


class Identify(tornado.web.RequestHandler):
    def post(self):
        whorls = json.loads(self.request.body)
        
        self.write("")


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/identify", Identify),
    (r"/(tester\.html)", tornado.web.StaticFileHandler,
     dict(path=settings['static_path'])),
], **settings)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
