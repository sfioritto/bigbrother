import os
import tornado.ioloop
import tornado.web
import json
from models import Whorl, engine, Session
from sqlalchemy.orm import scoped_session
from hashlib import sha512
from sqlalchemy.orm.exc import NoResultFound



class Application(tornado.web.Application):

    def __init__(self):

        self.session = scoped_session(Session)

        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static")
            }


        handlers = [
            (r"/identify", Identify),
            (r"/(tester\.html)", tornado.web.StaticFileHandler,
             dict(path=settings['static_path']))]


        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):

    @property
    def session(self):
        return self.application.session



class Identify(BaseHandler):

    def post(self):
        whorls = json.loads(self.request.body)
        for key, value in whorls.items():
            hashed = sha512(key + str(value)).hexdigest()

            try:
                whorl = self.session.query(Whorl).filter_by(key=hashed).one()
                whorl.count = whorl.count + 1
                self.write("found old value")

            except NoResultFound:
                whorl = Whorl(key=hashed)
                self.session.add(whorl)
                self.write("new value")

        self.session.commit()



if __name__ == "__main__":
    application = Application()
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
