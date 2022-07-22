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

from models.auth.auth_models import *
from models.auth.auth_models import Base
from schemas.auth.auth_schemas import *
from schemas.auth.auth_schemas import BaseModel

SECRET_KEY = "bfcaa24859af5279d4ec6c1de8f9d2624f6d819b020eba2bcd9fe0483af45ed3"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

Base.metadata.create_all(bind=engine)

class AuthCrud():

	def verify_password(plain_password, hashed_password):
		return pwd_context.verify(plain_password, hashed_password)

	def get_password_hash(password):
		return pwd_context.hash(password)

	def get_user(db, username: str):
		return db.query(User).filter(User.NIK == username).first()

	def authenticate_user(db, username: str, password: str):
		user = AuthCrud.get_user(db, username)
		if not user:
			return False
		if not AuthCrud.verify_password(password, user.PASSWORD):
			return False
		return user

	def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
		to_encode = data.copy()
		if expires_delta:
			expire = datetime.datetime.utcnow() + expires_delta
		else:
			expire = datetime.datetime.utcnow() + timedelta(minutes=15)
		to_encode.update({"exp": expire})
		encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
		return encoded_jwt

	async def get_current_user(db: Session = Depends(Connection.get_db),token: str = Depends(oauth2_scheme)):
		credentials_exception = HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Could not validate credentials",
			headers={"WWW-Authenticate": "Bearer"},
		)
		try:
			payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
			username: str = payload.get("sub")
			if username is None:
				raise credentials_exception
			token_data = TokenData(username=username)
		except JWTError:
			raise credentials_exception
		user = AuthCrud.get_user(db, username=token_data.username)
		if user is None:
			raise credentials_exception
		return user

	def validate_token(db: Session = Depends(Connection.get_db),token: str = Depends(oauth2_scheme)):
		credentials_exception = HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Could not validate credentials",
			headers={"WWW-Authenticate": "Bearer"},
		)
		try:
			payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
			username: str = payload.get("sub")
			if username is None:
				raise credentials_exception
			token_data = TokenData(username=username)
		except JWTError:
			raise credentials_exception
		user = AuthCrud.get_user(db, username=token_data.username)
		if user is None:
			raise credentials_exception
		return user

	def get_all_users(db: Session):

		query = """
		SELECT
		username,
		nama,
		email
		FROM users
		ORDER BY username
		"""
		sql = text(query)
		result = db.execute(sql)

		return result.fetchall()
	
	def cek_user(p_username:str,db: Session):

		query = """
		SELECT 
		username,
		email
		from users
		WHERE username = '{0}'
		LIMIT 1
		""".format(p_username)
		sql = text(query)
		result = db.execute(sql)

		return result.fetchone()
		
	
	def ins_user(p_username:str,p_password:str,p_nama:str,p_email:str,db: Session):
		query = """
		INSERT INTO users(username,password,nama,email)
		VALUES('{0}','{1}','{2}','{3}')
		""".format(p_username,p_password,p_nama,p_email)
		sql = text(query)
		result = db.execute(sql)
		res = db.commit()

		return 'SUCCESS'

	def edit_user(p_username:str,p_password:str,p_nama:str,p_email:str,db: Session):
		query = """
		UPDATE users 
		SET password = '{0}',
		nama= '{1}',
		email = '{2}'
		WHERE username = '{3}'
		""".format(p_password,p_nama,p_email,p_username)
		sql = text(query)
		result = db.execute(sql)
		res = db.commit()

		return 'SUCCESS'
	
	def update_password(p_username:str,p_password:str,db: Session):
		query = """
		UPDATE users 
		SET password = '{0}'
		WHERE username = '{1}'
		""".format(p_password,p_username)
		sql = text(query)
		result = db.execute(sql)
		res = db.commit()

		return 'SUCCESS'

	def delete_user(p_username:str, db: Session):
		query = """
		DELETE FROM users 
		WHERE username = '{0}'
		""".format(p_username)
		sql = text(query)
		result = db.execute(sql)
		res = db.commit()

		return 'SUCCESS'
	

	def cek_login(p_username:str,p_password:str,db: Session):

		query = """
		SELECT 
		username,
		password,
		email
		from users
		WHERE username = '{0}'
		and password = '{1}'
		LIMIT 1
		""".format(p_username,p_password)
		sql = text(query)
		result = db.execute(sql)

		return result.fetchone()