import bigbrother.config as config
from google.appengine.ext import db

    
class Stat(db.Model):
    name = db.StringProperty()
    value = db.IntegerProperty(default=0)


class Identity(db.Model):
    name = db.StringProperty()
    count = db.IntegerProperty(default=0)


class Whorl(db.Model):
    """
    The key will be a string, which will be hashed.
    """
    hashed = db.StringProperty()
    name = db.StringProperty()
    value = db.StringProperty(multiline=True)
    count = db.IntegerProperty(default=0)


class WhorlToId(db.Model):
    idkey = db.StringProperty()


