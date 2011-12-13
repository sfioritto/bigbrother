import who.config as config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, ForeignKey, Integer, String, Text


Base = declarative_base()

engine = create_engine(config.dbconnection)
Session = scoped_session(sessionmaker(bind=engine, 
                                      autocommit=False, 
                                      autoflush=False))

class Identity(Base):
    __tablename__ = 'identities'
    id = Column(Integer, primary_key=True)


class Whorl(Base):
    __tablename__ = 'whorls'
    hashed = Column(String(128), primary_key=True)
    key = Column(String(500))
    value = Column(Text)
    count = Column(Integer, default=1)

    
class WhorlGivenIdentity(Base):
    __tablename__ = 'whorl_given_identity'
    whorl_hashed = Column(String(128), ForeignKey('whorls.hashed'), primary_key=True)
    identity_id = Column(Integer, ForeignKey('identities.id'), primary_key=True)
    count = Column(Integer, default=0)


