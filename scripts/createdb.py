#!./env/bin/python

import who.config as config
import who.models as models
from sqlalchemy import create_engine

engine = create_engine(config.dbconnection)
models.Base.metadata.create_all(engine)

