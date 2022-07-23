import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Numeric,Float,DateTime
#from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from config.database import Base

class TransDet(Base):
	__tablename__ = "trans_det"
	trans_no = Column(String, primary_key=True)
	item_code = Column(String, primary_key=True)
    item_name = Column(String)
    item_desc = Column(String)
    item_price = Column(Numeric)
    item_qty = Column(Numeric)
    item_discount = Column(Numeric)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime,default=datetime.datetime.utcnow)

	# class Config:
	# 	orm_mode=True
	# 	arbitrary_types_allowed = True
	