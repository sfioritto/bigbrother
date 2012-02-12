import webapp2
import os
import json
import PIL.Image as Image
import StringIO


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')
		

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
