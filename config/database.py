import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL ="postgresql://yjelclgabkffud:a367ee1efaff3e536d338918b4814be7545f8f4ae554f3a53a276ea24efcd1cf@ec2-52-3-200-138.compute-1.amazonaws.com:5432/da5ol9s9k4q9h"

engine = create_engine(SQLALCHEMY_DATABASE_URL,max_identifier_length=128)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
