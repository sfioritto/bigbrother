import os
import tornado.ioloop
import tornado.web
import json
from tornado.web import url, RequestHandler, StaticFileHandler
from models import Whorl, engine, Session, Appearance
from hashlib import sha512
from sqlalchemy.orm.exc import NoResultFound



class Application(tornado.web.Application):

    def __init__(self):

        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static")
            }


        handlers = [
            (r"/identify", Identify),
            (r"/(tester\.html)", StaticFileHandler,
             dict(path=settings['static_path']))]


        tornado.web.Application.__init__(self, handlers, **settings)
        


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        self.session = Session()
        RequestHandler.__init__(self, *args, **kwargs)


    def finish(self, *args, **kwargs):
        return RequestHandler.finish(self, *args, **kwargs)


def create_hashes(whorls, prefix=None):
    
    hashes = []

    for key, value in whorls.items():

        if prefix:
            key = prefix + ":" + key
            
        if type(value) == dict:
            hashes.extend(create_hashes(value, prefix=key))
            
        elif type(value) == list:
            for item in value:
                hashes.extend(create_hashes(item, prefix=key))
                
        else:
            hashes.append((key,
                            value,
                            sha512(key + str(value)).hexdigest()))

    return hashes


def learn(whorls, id):
    pass



class Identify(BaseHandler):

    def post(self):

        rawdata = []
        rawdata.extend(json.loads(self.request.body).items())
        rawdata.append(("supports http 1.1",self.request.supports_http_1_1()))
        rawdata.extend(self.request.headers.items())

        whorls = self.create_get_whorls(rawdata)
        id = self.identify_from(whorls)

        if id:
            learn(whorls, id)
            
        self.session.commit()


    def identify_appearances(self, appearances, id):

        for appearance in appearances:
            appearance
            for whorl in appearance.whorls:
                try:
                    wgi = self.session.query(WhorlGivenIdentity)
                    .filter_by(whorl_hashed=whorl.hashed)
                    .filter_by(identity_id=id.id)
                    .one()
                    wgi.count = wgi.count + 1
                    
                except NoResultFound:
                    wgi = WhorlGivenIdentity(whorl_hashed = whorl.hashed,
                                             identity_id=id.id)
                    self.session.add(wgi)
                    self.session.flush()
        

    def create_get_whorls(self, rawdata):

        whorls = []

        for key, value, hashed in create_hashes(dict(rawdata)):
            try:
                whorl = self.session.query(Whorl).filter_by(hashed=hashed).one()

            except NoResultFound:
                whorl = Whorl(hashed=hashed, key=key, value=value)
                self.session.add(whorl)
                self.session.flush()

            whorls.append(whorl)

        return whorls

        

if __name__ == "__main__":
    application = Application()
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
