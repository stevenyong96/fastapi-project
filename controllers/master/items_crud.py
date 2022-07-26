from sqlalchemy.orm import Session

from typing import List , Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse,FileResponse
from sqlalchemy import Sequence, exc, text
from datetime import date, datetime, timedelta, timezone
import pathlib
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from config.database import engine, SessionLocal,Base
from config.connection import *

from models.master.items_models import *
from models.master.items_models import Base
# from schemas.master.items_schemas import *
# from schemas.master.items_schemas import BaseModel

Base.metadata.create_all(bind=engine)

class ItemsCrud():

	def get_list_items(db: Session):

		query = """
		SELECT 
		item_code,
		item_name,
		item_desc,
		item_price,
		item_stock,
		item_images1,
		item_images2,
		item_images3,
		status
		from master_items
		LIMIT 100
		"""
		sql = text(query)
		result = db.execute(sql)
		return result.fetchall()

	def get_item_detail(p_item_code: str, db: Session):
		query = """
		SELECT 
		item_code,
		item_name,
		item_desc,
		item_price,
		item_stock,
		item_images1,
		item_images2,
		item_images3,
		status
		from master_items
		WHERE item_code = '{0}'
		and status = 1
		LIMIT 1
		""".format(p_item_code)
		sql = text(query)
		result = db.execute(sql)
		return result.fetchone()

	def ins_item_detail(p_item_code: str,p_item_name:str,p_item_desc:str,p_item_price:int,p_item_stock:int,p_item_color:str,p_item_images1:str,p_item_images2:str,p_item_images3:str,status:int, db: Session):
		query = """
		INSERT INTO master_items(item_code,item_name,item_desc,item_price,item_stock,item_color,item_images,item_images2,item_images3,status)
        VALUES('{0}','{1}','{2}',{3},{4},'{5}','{6}','{7}','{8}',{9})
		""".format(p_item_code,p_item_name,p_item_desc,p_item_price,p_item_stock,p_item_color,p_item_images1,p_item_images2,p_item_images3,status)
		sql = text(query)
		result = db.execute(sql)
		db.commit()
		return 'SUCCESS'

	
	
