import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Numeric,Float,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from config.database import Base

class Item(Base):
	__tablename__ = "items"
	item_code = Column(String, primary_key=True)
	item_name = Column(String)
	item_desc = Column(String)
	item_price = Column(Numeric)
	item_stock = Column(Numeric,default=0)
	item_color = Column(String)
	item_images1 = Column(String)
	item_images2 = Column(String)
	item_images3 = Column(String)
	status = Column(Integer, default=0)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime,default=datetime.datetime.utcnow)

	# class Config:
	# 	orm_mode=True
	# 	arbitrary_types_allowed = True
