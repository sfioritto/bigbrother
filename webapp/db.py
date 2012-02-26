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
	The key will be a string, which will be hased.
	"""
	name = db.StringProperty()
	value = db.StringProperty(multiline=True)
	count = db.IntegerProperty(default=0)


class WhorlIdentity(db.Model):
    whorl_hashed = db.StringProperty() #whorl entity key
    identity_id = db.IntegerProperty() #identity entity key
    count = db.IntegerProperty(default=1)
