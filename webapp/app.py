import web
import os
import json
import Image
import StringIO


urls = (
    '/learn', 'Learn',
    '/identify', 'Identify',
    '/evercookie_cache', 'EvercookieCache',
    '/evercookie_png', 'EvercookiePng',
    '/evercookie_etag', 'EvercookieEtag'
)

app = web.application(urls, globals())

application = app.wsgifunc()

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
