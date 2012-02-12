#!./env/bin/python

import bigbrother.config as config
import bigbrother.webapp.orm as orm
from sqlalchemy import create_engine

def run():
    engine = create_engine(config.dbconnection)
    orm.Base.metadata.create_all(engine)

    session = orm.Session()
    total_visits = orm.Stat(key="total_visits")
    session.add(total_visits)
    session.commit()
    session.close()


if __name__ == "__main__":
    run()
