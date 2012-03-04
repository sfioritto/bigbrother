import webapp2
import webapp.model as model
import os
import json
import PIL.Image as Image
import StringIO


class Learn:
    
    def post(self):

        partial = self.request
        rawdata = model.build_raw_data(partial, self.request.environ, self.request.remote_addr)
        identity = model.create_user(partial["name"])
        whorls = model.create_get_whorls(rawdata)
        model.learn(whorls, identity)
        
        return ""
    

class Identify:

    def post(self):
        
        partial = self.request.items() # as in a partial fingerprint
        rawdata = model.build_raw_data(partial, self.request.environ, self.request.remote_addr)
        whorls = model.get_whorls(rawdata)
        identity = model.identify_from(whorls)
        self.response.headers['Content-Type'] = 'text/html'

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
            self.response.headers['Content-Type'] = 'image/png'
            self.response.headers['Last-Modified'] = 'Wed, 30 Jun 2010 21:36:48 GMT'
            self.response.headers['Expires'] = 'Tue, 31 Dec 2030 23:30:45 GMT'
            self.response.headers['Cache-Control'] = 'private, max-age=630720000'
            return self.cookies.get("evercookie_cache")
        #no cookie
        except:
            self.response.headers['Content-Type'] = 'image/png'
            self.abort(304)



class EvercookiePng:
    
    def get(self):
        """
        Port of evercookie php png code.
        """

        try:
            ec_png = self.cookies.get("evercookie_png")
            rgb = tuple([ord(x) for x in ec_png])
            i = Image.new("RGB", (200, 1))
            px = i.load()
            px[0, 0] = rgb
            sio = StringIO.StringIO()
            i.save(sio, "PNG")
            self.response.headers['Content-Type'] = 'image/png'
            self.response.headers['Last-Modified'] = 'Wed, 30 Jun 2010 21:36:48 GMT'
            self.response.headers['Expires'] = 'Tue, 31 Dec 2030 23:30:45 GMT'
            self.response.headers['Cache-Control'] = 'private, max-age=630720000'

            return sio.getvalue()

            
        except Exception as e:

            #no cookie found, force a read from the cache
            self.abort(304)


class EvercookieEtag:

    def get(self):
        
        """
        Port of evercookiee php etag code.
        """

        etag = ""
        self.response.headers['Content-Type'] = 'text/html'
        try:
            self.response.headers['Etag'] = self.cookies.get("evercookie_eta")
            return ""
        
        except:
            if self.request.environ.has_key("HTTP_IF_NONE_MATCH"):
                etag = self.request.environ["HTTP_IF_NONE_MATCH"]

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




