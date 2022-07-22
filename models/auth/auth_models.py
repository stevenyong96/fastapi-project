import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Numeric,Float,DateTime
#from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from config.database import Base

class User(Base):
	__tablename__ = "users"
	username = Column(String, primary_key=True)
	password = Column(String)
	nama = Column(String)
	email = Column(String, unique=True)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime,default=datetime.datetime.utcnow)

	# class Config:
	# 	orm_mode=True
	# 	arbitrary_types_allowed = True
	
# class UserData(Base):
#      __tablename__ = "YG_TEST_USER_DATA"
#      USER_NIK = Column(String, primary_key=True)
#      USER_ADDRESS = Column(String)
#      CITY = Column(String)
#      PHONE_NO = Column(String)
#      CREATED_AT = Column(DateTime, default=datetime.datetime.utcnow)
#      UPDATED_AT = Column(DateTime,default=datetime.datetime.utcnow)
	 