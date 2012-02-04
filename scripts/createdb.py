#!./env/bin/python

import bigbrother.config as config
import bigbrother.webapp.models as models
from sqlalchemy import create_engine

engine = create_engine(config.dbconnection)
models.Base.metadata.create_all(engine)

session = models.Session()
total_visits = models.Stat(key="total_visits")
session.add(total_visits)
session.commit()
