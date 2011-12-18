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
            (r"/tag", Tag),
            (r"/(tester\.html)", StaticFileHandler,
             dict(path=settings['static_path']))]


        tornado.web.Application.__init__(self, handlers, **settings)
        


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        self.session = Session()
        RequestHandler.__init__(self, *args, **kwargs)


    def get_whorls(self, rawdata):

        whorls = []

        for key, value, hashed in create_hashes(dict(rawdata)):
            try:
                whorl = self.session.query(Whorl).filter_by(hashed=hashed).one()
                whorls.append(whorls)
                
            except NoResultFound:
                pass
            
        return whorls
        
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


def learn(whorls, identity, session):
    
    """
    increment the count for whorlGivenId probability and whorl
    """
    
    for whorl in whorls:
        whorl.count = whorl.count + 1
        try:
            wgi = session.query(WhorlGivenIdentity)
            .filter(whorl_hashed=whorl.hashed)
            .filter(identity_id=identity.id)
            .one()
            wgi.count = wgi.count + 1
            
        except NoResultFound:
            wgi = WhorlGivenIdentity(whorl_hashed=whorl.hashed,
                                     identity_id = identity.id)
            session.add(wgi)
                

def build_raw_data(request):

        rawdata = []
        rawdata.extend(json.loads(request.body).items())
        rawdata.append(("supports http 1.1", request.supports_http_1_1()))
        rawdata.extend(request.headers.items())

        return rawdata


def get_user(username, session):

    try:
        return session.query(Identity).filter(username=username).one()
    except NoResultFound:
        session.add(Identity(username=username))
        session.flush()

class Tag(BaseHandler):

    def post(self):
        username = self.request.body["username"]
        identity = get_user(username, session)
        rawdata = build_raw_data(self.request)
        whorls = self.create_get_whorls(rawdata)
        learn(whorls, identity, self.session)
        self.session.commit()


class Identify(BaseHandler):

    def post(self):
        rawdata = build_raw_data(self.request)
        whorls = self.get_whorls(rawdata)
        identity = self.identify_from(whorls)
        self.write(identity)
        self.session.commit()


    def identify_from(self, whorls):
        return None
        # identities = {}
        # for whorl in whorls:
            # wgi = self.session.query(WhorlGivenIdentity).filter(whorl_hashed=whorl.hashed).all()
            

        

if __name__ == "__main__":
    application = Application()
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
