import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Numeric,Float,DateTime
#from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from config.database import Base

class TransHdr(Base):
	__tablename__ = "trans_hdr"
	trans_no = Column(String, primary_key=True)
	customer_name = Column(String)
	total_payment = Column(Numeric)
	total_item = Column(Numeric)
    payment_type = Column(String)
    total_discount = Column(Numeric)
    tax = Column(Numeric, default=0)
    tax_percent = Column(String)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime,default=datetime.datetime.utcnow)

	# class Config:
	# 	orm_mode=True
	# 	arbitrary_types_allowed = True
	