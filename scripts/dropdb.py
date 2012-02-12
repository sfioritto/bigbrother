#!./env/bin/python

import bigbrother.config as config
import bigbrother.webapp.orm as orm
from sqlalchemy import create_engine

def run():
    engine = create_engine(config.dbconnection)
    orm.Base.metadata.drop_all(engine)
    session = orm.Session()
    session.close()

if __name__ == "__main__":
    run()
