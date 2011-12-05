#!./env/bin/python

import models
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:password@localhost/who')
models.Base.metadata.create_all(engine)

