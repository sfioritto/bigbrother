from sqlalchemy.ext.declarative import *
from sqlalchemy import Column, ForeignKey, Integer, String
Base = declarative_base()


class Identity(Base):
    __tablename__ = 'identities'
    id = Column(Integer, primary_key=True)


class Whorl(Base):
    __tablename__ = 'whorls'
    key = Column(String(128), primary_key=True)
    count = Column(Integer)

    
class WhorlGivenIdentity(Base):
    __tablename__ = 'whorl_given_identity'
    whorl_key = Column(String(128), ForeignKey('whorls.key'), primary_key=True)
    identity_id = Column(Integer, ForeignKey('identities.id'), primary_key=True)
    count = Column(Integer)


