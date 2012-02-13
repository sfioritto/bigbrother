import webapp2
import webapp.model as model
import os
import json
import Pil.Image as Image
import StringIO


class Learn:
    
    def post(self):

        partial = json.loads(web.data())
        rawdata = model.build_raw_data(partial, web.ctx.environ, web.ctx.ip)
        identity = model.create_user(partial["name"])
        whorls = model.create_get_whorls(rawdata)
        model.learn(whorls, identity)
        
        return ""
    

class Identify:

    def post(self):
        
        partial = json.loads(web.data()).items() # as in a partial fingerprint
        rawdata = model.build_raw_data(partial, web.ctx.environ, web.ctx.ip)
        whorls = model.get_whorls(rawdata)
        identity = model.identify_from(whorls)
        web.header('Content-Type', 'text/html');

        if identity:
            return identity.name
        else:
            return "I dunno."


class EvercookieCache:

    def get(self):
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
    
    def get(self):
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

    def get(self):
        
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

urls = [
    ('/learn', Learn),
    ('/identify', Identify),
    ('/evercookie_cache', EvercookieCache),
    ('/evercookie_png', EvercookiePng),
    ('/evercookie_etag', EvercookieEtag),
]


app = webapp2.WSGIApplication(urls,
                              debug=True)




