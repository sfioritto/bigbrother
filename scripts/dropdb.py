#!./env/bin/python

import bigbrother.config as config
import bigbrother.webapp.models as models
from sqlalchemy import create_engine

engine = create_engine(config.dbconnection)
models.Base.metadata.drop_all(engine)
