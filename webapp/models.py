import bigbrother.config as config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Table


Base = declarative_base()

engine = create_engine(config.dbconnection)
Session = scoped_session(sessionmaker(bind=engine, 
                                      autocommit=False, 
                                      autoflush=False))

class Stat(Base):
    __tablename__ = 'stats'
    key = Column(String(100), primary_key=True)
    value = Column(Integer, default=0)


class Identity(Base):
    __tablename__ = 'identities'
    id = Column(Integer, primary_key=True)
    username = Column(String(500), unique=True)
    whorl_identities = relationship("WhorlIdentity", backref="identity")
    count = Column(Integer, default=0)


class Whorl(Base):
    __tablename__ = 'whorls'
    hashed = Column(String(128), primary_key=True)
    key = Column(String(500))
    value = Column(Text)
    count = Column(Integer, default=0)


class WhorlIdentity(Base):
    __tablename__ = 'whorl_identity'
    whorl_hashed = Column(String(128), ForeignKey('whorls.hashed'), primary_key=True)
    identity_id = Column(Integer, ForeignKey('identities.id'), primary_key=True)
    count = Column(Integer, default=1)
