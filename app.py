import os
import tornado.ioloop
import tornado.web
import json
from models import Whorl, engine, Session
from hashlib import sha512
from sqlalchemy.orm.exc import NoResultFound



class Application(tornado.web.Application):

    def __init__(self):

        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static")
            }


        handlers = [
            (r"/identify", Identify),
            (r"/(tester\.html)", tornado.web.StaticFileHandler,
             dict(path=settings['static_path']))]


        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        self.session = Session()
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)


    def finish(self, *args, **kwargs):
        return tornado.web.RequestHandler.finish(self, *args, **kwargs)


def create_hashes(whorls):

    hashes = []
    test = {}
    for key, value in whorls.items():
        if key == "plugins":
            for blob in value:
                hashed = sha512("plugin" + str(blob)).hexdigest()
                hashes.append(hashed)
        else:
            hashed = sha512(key + str(value)).hexdigest()
            hashes.append(hashed)

    #todo: probably shouldn't assume these will all be unique.
    #don't assume the input is clean
    return hashes



    def get_create_whorls(self, whorls):
        pass

    
    def possible_identities(self, whorls):
        pass


    def ranked_identities(self, identities):
        pass





class Identify(BaseHandler):

    def post(self):

        whorls = []
        whorls.extend(json.loads(self.request.body).items())
        whorls.append(("supports http 1.1",self.request.supports_http_1_1()))
        whorls.extend(self.request.headers.items())

        for hashed in create_hashes(dict(whorls)):
            try:
                whorl = self.session.query(Whorl).filter_by(key=hashed).one()
                whorl.count = whorl.count + 1

            except NoResultFound:
                whorl = Whorl(key=hashed)
                self.session.add(whorl)
                self.write("new value")

        self.session.commit()



if __name__ == "__main__":
    application = Application()
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
