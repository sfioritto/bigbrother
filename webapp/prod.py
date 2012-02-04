#!/usr/bin/env python

from bigbrother.webapp.app import *


if __name__ == "__main__":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
