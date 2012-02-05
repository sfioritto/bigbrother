import web
import os
import json
import Image
import StringIO
from models import Whorl, Session, WhorlIdentity, engine, Identity, Stat
from hashlib import sha512
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import asc
from operator import mul
from collections import defaultdict


urls = (
    '/learn', 'Learn',
    '/identify', 'Identify',
    '/evercookie_cache', 'EvercookieCache',
    '/evercookie_png', 'EvercookiePng',
    '/evercookie_etag', 'EvercookieEtag'
)

app = web.application(urls, globals())

curdir = os.path.dirname(__file__)

application = app.wsgifunc()


def sa_load_hook():
    web.ctx.db = Session()

def sa_unload_hook():
    Session.remove()
    
app.add_processor(web.loadhook(sa_load_hook))
app.add_processor(web.unloadhook(sa_unload_hook))


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
            
            if type(value) != unicode:
                value = unicode(value)

            hashes.append((key,
                            value,
                            sha512((key + value).encode("utf-8")).hexdigest()))
            
    return hashes


def learn(whorls, identity):
    
    """
    increment the count for whorlID probability, whorl, total_visits
    and identity.
    """

    db = web.ctx.db
    identity.count = identity.count + 1
    total_visits = db.query(Stat).filter_by(key="total_visits").one()
    total_visits.value = total_visits.value + 1

    for whorl in whorls:
        whorl.count = whorl.count + 1
        try:
            wgi = db.query(WhorlIdentity).\
                filter_by(whorl_hashed=whorl.hashed).\
                filter_by(identity_id=identity.id).\
                one()
            wgi.count = wgi.count + 1
            
        except NoResultFound:
            wgi = WhorlIdentity(whorl_hashed=whorl.hashed,
                                     identity_id = identity.id)
            db.add(wgi)
            db.flush()
                

def build_raw_data(partial):

        rawdata = []
        rawdata.extend(partial.items())

        httpheaders = []
        for key, value in web.ctx.environ.items():
            if key.startswith("HTTP_"):
                httpheaders.append((key, value))
        rawdata.extend(httpheaders)
        rawdata.append(("IP_ADDR", web.ctx.ip))

        return rawdata


def get_user(username):
    db = web.ctx.db
    try:
        return db.query(Identity).filter_by(username=username).one()
    except NoResultFound:
        identity = Identity(username=username)
        db.add(identity)
        db.flush()
        return identity


def get_whorls(rawdata):

    db = web.ctx.db
    whorls = []
    hashes = [hashed for key, value, hashed in create_hashes(dict(rawdata))]
    whorls = db.query(Whorl).\
        filter(Whorl.hashed.in_(hashes)).\
        all()

    #TODO: if the number of users grows large, we need to limit
    # the whorls we consider, because otherwise the set of users we need
    # to consider gets too large, and the memory and computing requirements
    # will grow too quickly. So we could do something like this:
    #
    #order_by(asc(Whorl.count)).\
    #limit(top)
    #
    # this only looks at rare whorls. This may not be the best solution. When the data
    # is sparse, if a player switches browsers there is very little or no overlap with
    # the whorls generated by the previous browser with this method.

    return whorls



def create_get_whorls(rawdata):
        
    whorls = []
    db = web.ctx.db

    for key, value, hashed in create_hashes(dict(rawdata)):
        try:
            whorl = db.query(Whorl).filter_by(hashed=hashed).one()

        except NoResultFound:
            whorl = Whorl(hashed=hashed, key=key, value=value)
            db.add(whorl)
            db.flush()
            
        whorls.append(whorl)

    return whorls

    

def stats_obj(db):
    return dict([(s.key, s.value) for s in db.query(Stat).all()])


def identify_from(whorls):

    db = web.ctx.db
    stats = stats_obj(db)
    minprob = float(1) / stats["total_visits"]
    whorl_hashes = list(set([whorl.hashed for whorl in whorls]))

    # this is a dictionary of dictionaries. The inner dictionaries
    # contain probabilities of the whorl given the user.
    whorlids = defaultdict(lambda : defaultdict(lambda : minprob))
    for wid in db.query(WhorlIdentity).\
        filter(WhorlIdentity.whorl_hashed.in_(whorl_hashes)).\
        all():

        whorlids[wid.identity][wid.whorl_hashed] =\
            min(1, float(wid.count) / wid.identity.count)

    # The probabilities above are then used to create a list
    # of probabilities per user for every whorl passed in.
    # The inner dictionary above defaults to a reasonable
    # minimum if we've never seen a whorl for a given user
    givenid = defaultdict(list)
    for identity, idprobs in whorlids.items():
        for whorl in whorls:
            givenid[identity].append(idprobs[whorl.hashed])

    # These are all the probabilities put into a list of tuples so
    # it can be sorted by probability.
    probs = [(\
               # calculate the posterior probability p(whorl|identity)p(identity)
               reduce(mul, idprobs) * (float(identity.count) / stats["total_visits"]),\

               # identity id as a tie breaker in sorting. this is arbitrary. If there
               # is a tie, we just guess. could put a random number here I suppose.
               identity.id,\

               # the identity tied to this probability.
               identity) \
               
               for identity, idprobs in givenid.items()]

    probs.sort()
    return probs[-1][2] # the most likely identity (third element is the identity)


class Learn:
    
    def POST(self):

        partial = json.loads(web.data())
        rawdata = build_raw_data(partial)
        identity = get_user(partial["username"])
        whorls = create_get_whorls(rawdata)
        learn(whorls, identity)
        web.ctx.db.commit()
        
        return ""
    

class Identify:

    def POST(self):
        
        partial = json.loads(web.data()) # as in a partial fingerprint
        rawdata = build_raw_data(partial)
        whorls = get_whorls(rawdata)
        identity = identify_from(whorls)
        web.header('Content-Type', 'text/html');

        if identity:
            return identity.username
        else:
            return "I dunno."


class EvercookieCache:

    def GET(self):
        """
        Port of evercookie php simple cache code.
        """
        
        try:
            web.header('Content-Type', 'image/png');
            web.header('Last-Modified', 'Wed, 30 Jun 2010 21:36:48 GMT');
            web.header('Expires', 'Tue, 31 Dec 2030 23:30:45 GMT');
            web.header('Cache-Control', 'private, max-age=630720000');
            return web.cookies().evercookie_cache
        #no cookie
        except:
            web.header('Content-Type', 'image/png');
            raise web.notmodified()



class EvercookiePng:
    
    def GET(self):
        """
        Port of evercookie php png code.
        """

        try:
            ec_png = web.cookies().evercookie_png
            rgb = tuple([ord(x) for x in ec_png])
            i = Image.new("RGB", (200, 1))
            px = i.load()
            px[0, 0] = rgb
            sio = StringIO.StringIO()
            i.save(sio, "PNG")
            web.header('Content-Type', 'image/png');
            web.header('Last-Modified', 'Wed, 30 Jun 2010 21:36:48 GMT');
            web.header('Expires', 'Tue, 31 Dec 2030 23:30:45 GMT');
            web.header('Cache-Control', 'private, max-age=630720000');

            return sio.getvalue()

            
        except Exception as e:

            #no cookie found, force a read from the cache
            raise web.notmodified()


class EvercookieEtag:

    def GET(self):
        
        """
        Port of evercookiee php etag code.
        """

        etag = ""
        web.header('Content-Type', 'text/html');
        try:
            web.header('Etag', web.cookies().evercookie_etag)
            return ""
        
        except:
            if web.ctx.environ.has_key("HTTP_IF_NONE_MATCH"):
                etag = web.ctx.environ["HTTP_IF_NONE_MATCH"]

        return etag
    


if __name__ == '__main__':
    app.run()
