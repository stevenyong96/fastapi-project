#!/usr/bin/env python

from typing import List
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status, Request, Path
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from sqlalchemy import text
from starlette.responses import FileResponse
import pathlib
import os
import json
from datetime import date, datetime, timedelta
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from passlib.context import CryptContext

###MODELS###
from models.auth.auth_models import *
from models.auth.auth_models import Base
from models.master.items_models import *
from models.master.items_models import Base

###SCHEMAS###
from schemas.auth.auth_schemas import *
from schemas.auth.auth_schemas import BaseModel

###CRUD###
from controllers.auth.auth_crud import *
from controllers.master.items_crud import *
# from controllers.transaction.test_crud import *


# CONFIG
from config.database import SessionLocal, engine, Base
from config.connection import *

app = FastAPI(
	title="Binar API Kelompok 3",
	description="Binar API Challenge Chapter 7",
	version="0.0.1",
)

# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

today = date.today()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
	allow_credentials=True,
)

#from multiprocessing import set_start_method
#from multiprocessing import Process, Manager
#try:
#    set_start_method('spawn')
#except RuntimeError:
#    pass


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	return JSONResponse(
		status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
		content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
	)


#######################################################################  DEFAULT  ###############################################################################

# Dependency
@app.get("/" ,include_in_schema=False)
def main(db: Session = Depends(Connection.get_db)):
	if db is None:
		raise HTTPException(status_code=404, detail="User not found")
	return RedirectResponse(url="/docs/")


# @app.post("/token", response_model=Token , include_in_schema=False)
# async def login_for_access_token(db: Session = Depends(Connection.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
# 	user = AuthCrud.authenticate_user(
# 		db, form_data.username, form_data.password)
# 	if not user:
# 		raise HTTPException(
# 			status_code=status.HTTP_401_UNAUTHORIZED,
# 			detail="Incorrect username or password",
# 			headers={"WWW-Authenticate": "Bearer"},
# 		)
# 	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# 	access_token = AuthCrud.create_access_token(
# 		data={"sub": user.NIK}, expires_delta=access_token_expires
# 	)
# 	return {"access_token": access_token, "token_type": "bearer", "apikey": "2l0aCrhbVmxX8393FU4tYrNzeWrncpgb"}


# async def read_users_me(current_user: User = Depends(AuthCrud.get_current_user)):
# 	return current_user


@app.get("/login/{p_username}/{p_password}", tags=["Auth"])
async def login(p_username:str, p_password:str,db: Session = Depends(Connection.get_db)):
	try:
		if db is None:
			raise HTTPException(status_code=404, detail="Connection Failed")
		cek_login = AuthCrud.cek_login(p_username,p_password,db)
		if (cek_login is not None):
			return {'status': 'SUCCESS', 'data': 'Login Successfull'}
		else:
			return {'status': 'ERROR', 'data': 'Wrong Username Or Password'}
	except:
		return {'status': 'ERROR', 'data': 'Something Went Wrong With Login'}

#######################################################################  MASTER  ###############################################################################
###################USERS###########################
@app.get("/users", tags=["Master_Users"])
async def get_all_users(db: Session = Depends(Connection.get_db)):
	
	try:
		if db is None:
			raise HTTPException(status_code=404, detail="Connection Failed")
		get_all_users = AuthCrud.get_all_users(db)
		if len(get_all_users) > 0:
			return {'status': 'SUCCESS', 'data': get_all_users}
		else:
			return {'status': 'ERROR', 'data': 'Get All Users Not Found'}
	except:
		return {'status': 'ERROR', 'data': 'Something Went Wrong With Get All Users'}


@app.post("/users/add/{p_username}/{p_password}/{p_nama}/{p_email}", tags=["Master_Users"])
async def ins_user(p_username:str,p_password:str,p_nama:str,p_email:str,db: Session = Depends(Connection.get_db)):

	try:
		if db is None:
			raise HTTPException(status_code=404, detail="Connection Failed")

		cek_user = AuthCrud.cek_user(p_username,db)
		if(cek_user is None):
			cek_email = AuthCrud.cek_email(p_email,db)
			if(cek_email is None):
				ins_user = AuthCrud.ins_user(p_username,p_password,p_nama,p_email,db)
				if (ins_user == 'SUCCESS'):
					return {'status': 'SUCCESS', 'data': 'Insert Success'}
				else:
					return {'status': 'ERROR', 'data': 'Failed to Insert Users'}
			else:
				return {'status': 'ERROR', 'data': 'Failed to Insert Users , Email Already Exist'}
		else:
			return {'status': 'ERROR', 'data': 'Failed To Insert , Username Already Exist'}
	except:
		return {'status': 'ERROR', 'data': 'Something Went Wrong With Insert Users'}


@app.put("/users/edit/{p_username}/{p_password}/{p_nama}/{p_email}", tags=["Master_Users"])
async def edit_user(p_username:str,p_password:str,p_nama:str,p_email:str,db: Session = Depends(Connection.get_db)):

	try:
		if db is None:
			raise HTTPException(status_code=404, detail="Connection Failed")

		cek_user = AuthCrud.cek_user(p_username,db)
		if(cek_user is not None):
			edit_user = AuthCrud.edit_user(p_username,p_password,p_nama,p_email,db)
			if (edit_user == 'SUCCESS'):
				return {'status': 'SUCCESS', 'data': 'Update User Success'}
			else:
				return {'status': 'ERROR', 'data': 'Failed to Update User'}
		else:
			return {'status': 'ERROR', 'data': 'Failed To Update , Username Not Exist'}
	except:
		return {'status': 'ERROR', 'data': 'Something Went Wrong With Edit Users'}

@app.patch("/users/update/pass/{p_username}/{p_password}", tags=["Master_Users"])
async def update_pass(p_username:str,p_password:str,db: Session = Depends(Connection.get_db)):

	try:
		if db is None:
			raise HTTPException(status_code=404, detail="Connection Failed")

		cek_user = AuthCrud.cek_user(p_username,db)
		if(cek_user is not None):
			update_password = AuthCrud.update_password(p_username,p_password,db)
			if (update_password == 'SUCCESS'):
				return {'status': 'SUCCESS', 'data': 'Update Password Success'}
			else:
				return {'status': 'ERROR', 'data': 'Failed to Update User Password'}
		else:
			return {'status': 'ERROR', 'data': 'Failed To Update , Username Not Exist'}
	except:
		return {'status': 'ERROR', 'data': 'Something Went Wrong With Update Users Password'}

@app.delete("/users/delete/{p_username}", tags=["Master_Users"])
async def delete_user(p_username:str,db: Session = Depends(Connection.get_db)):

	try:
		if db is None:
			raise HTTPException(status_code=404, detail="Connection Failed")

		cek_user = AuthCrud.cek_user(p_username,db)
		if(cek_user is not None):
			delete_user = AuthCrud.delete_user(p_username,db)
			if (delete_user == 'SUCCESS'):
				return {'status': 'SUCCESS', 'data': 'Delete User Success'}
			else:
				return {'status': 'ERROR', 'data': 'Failed to Delete User'}
		else:
			return {'status': 'ERROR', 'data': 'Failed To Delete , Username Not Exist'}
	except:
		return {'status': 'ERROR', 'data': 'Something Went Wrong With Delete User'}

@app.get("/list_items", tags=["Master_Items"])
async def list_items(db: Session = Depends(Connection.get_db)):

	try:
		if db is None:
			raise HTTPException(status_code=404, detail="Connection Failed")
		get_list_items = ItemsCrud.get_list_items(db)
		if len(get_list_items) > 0 :
			return {'status': 'SUCCESS', 'data': get_list_items}
		else:
			return {'status': 'ERROR', 'data': 'Get List Items Not Found'}	
	except:
		return {'status': 'ERROR', 'data': 'Something Went Wrong'}

@app.get("/items/{p_item_code}", tags=["Master_Items"])
async def item_detail(p_item_code:str,db: Session = Depends(Connection.get_db)):

	try:
		if db is None:
			raise HTTPException(status_code=404, detail="Connection Failed")
		get_item_detail = ItemsCrud.get_item_detail(p_item_code,db)
		if (get_item_detail is not None):
			return {'status': 'SUCCESS', 'data': get_item_detail}
		else:
			return {'status': 'ERROR', 'data': 'Get Items Not Found'}	
	except:
		return {'status': 'ERROR', 'data': 'Something Went Wrong'}

@app.post("/item/ins/{p_item_code}/{p_item_name}/{p_item_desc}/{p_item_price}/{p_item_stock}/{p_item_images1}/{p_item_images2}/{p_item_images3}/{status}", tags=["Master_Items"])
async def ins_item_detail(p_item_code:str,p_item_name:str,p_item_desc:str,p_item_price:int,p_item_stock:int,p_item_images1:str,p_item_images2:str,p_item_images3:str,p_status:int,db: Session = Depends(Connection.get_db)):

	try:
		if db is None:
			raise HTTPException(status_code=404, detail="Connection Failed")
		ins_item_detail = ItemsCrud.ins_item_detail(p_item_code,p_item_name,p_item_desc,p_item_price,p_item_stock,p_item_images1,p_item_images2,p_item_images3,status,db)
		if (ins_item_detail == 'SUCCESS'):
			return {'status': 'SUCCESS', 'data': 'Insert Item Detail Success'}
		else:
			return {'status': 'ERROR', 'data': 'Insert Items Detail Not Found'}	
	except:
		return {'status': 'ERROR', 'data': 'Something Went Wrong'}

ins_item_detail

#######################################################################  TRANSACTION  ###############################################################################


########### PO ############################

# @app.post("/po/post_supplier_order/", tags=["Transaction_PO"])
# async def post_supplier_order(item: S_PO_DATA, db: Session = Depends(Connection.get_db), current_user: User = Depends(read_users_me)):
	
# 	if db is None:
# 		raise HTTPException(status_code=404, detail="Connection Failed")
	
# 	try:
# 		p_modul = 'po'
# 		p_task_name = 'post_supplier_order'
# 		getConfRabbitMQ = AuthCrud.get_conf_rabbitmq(p_modul, p_task_name, db)

# 		if len(getConfRabbitMQ) == 0:
# 			return {'status': 'MAINTENANCE', 'data': 'API UNDER MAINTENANCE'}

# 		privileges = AuthCrud.get_user_privileges(
# 			current_user.NIK, 'post', p_modul, p_task_name, db)
# 		if len(privileges) == 0:
# 			return {'status': 'ERROR', 'data': 'USER DID NOT HAVE PRIVILEGES'}

# 		item_dict = item.dict()
# 		temp_transaction_id = item_dict['data']['header']['transaction_id']
# 		temp_source_name = item_dict['data']['header']['source_name']
# 		temp_site_code = item_dict['data']['header']['store_site_code']
# 		temp_dc_supplier_code = item_dict['data']['header']['dc_supplier_code']
# 		temp_ad_chain = item_dict['data']['header']['address_chain']
# 		temp_comm_cont = item_dict['data']['header']['commercial_contract']
# 		temp_order_date = item_dict['data']['header']['order_date']
# 		temp_delv_date = item_dict['data']['header']['delivery_date']
# 		temp_unique_code = item_dict['data']['header']['unique_deliv_code']
# 		temp_cust_lat = item_dict['data']['header']['cust_lat']
# 		temp_cust_long = item_dict['data']['header']['cust_long']
# 		count_detail = len(item_dict['data']['detail'])
# 		count_slash_order_date = temp_order_date.count('/')
# 		count_div_order_date = temp_order_date.count(':')
# 		count_slash_delv_date = temp_delv_date.count('/')
# 		count_div_delv_date = temp_delv_date.count(':')
# 		#temp_special_char_deliv_note_num1 = temp_deliv_note_num.replace(
# 		#    '!#34#!', '"')
# 		#temp_special_char_deliv_note_num2 = temp_special_char_deliv_note_num1.replace(
# 		#    '!#39#!', '\'')
# 		#temp_special_char_deliv_note_num3 = temp_special_char_deliv_note_num2.replace(
# 		#   '!#47#!', '/')
# 		#temp_special_char_deliv_note_num4 = temp_special_char_deliv_note_num3.replace(
# 		#    '!#92#!', '\\')
# 		#temp_special_char_deliv_note_count = len(
# 		#    temp_special_char_deliv_note_num4)
# 		# print(temp_special_char_deliv_note_count)
# 		if temp_transaction_id == "" or temp_transaction_id == None:
# 			return {'status': 'ERROR', 'data': 'TRANSACTION ID TIDAK BOLEH KOSONG'}
# 		if temp_site_code == "" or temp_site_code == None:
# 			return {'status': 'ERROR', 'data': 'SITE CODE TIDAK BOLEH KOSONG ATAU BUKAN LENGTH(5)'}
# 		if temp_dc_supplier_code == "" or temp_dc_supplier_code == None:
# 			return {'status': 'ERROR', 'data': 'SUPP CODE TIDAK BOLEH KOSONG'}
# 		if temp_ad_chain == "" or temp_ad_chain == None:
# 			return {'status': 'ERROR', 'data': 'ADD CHAIN TIDAK BOLEH KOSONG'}
# 		if temp_comm_cont == "" or temp_comm_cont == None:
# 			return {'status': 'ERROR', 'data': 'COMM CONT TIDAK BOLEH KOSONG'}
# 		if temp_order_date == "" or temp_order_date == None:
# 			return {'status': 'ERROR', 'data': 'ORDER DATE TIDAK BOLEH KOSONG'}
# 		if temp_delv_date == "" or temp_delv_date == None:
# 			return {'status': 'ERROR', 'data': 'DELV DATE TIDAK BOLEH KOSONG'}
# 		if temp_transaction_id == "" or temp_transaction_id == None:
# 			return {'status': 'ERROR', 'data': 'TRANSACTION ID TIDAK BOLEH KOSONG'}
# 		if temp_source_name == "" or temp_source_name == None:
# 			return {'status': 'ERROR', 'data': 'SOURCE NAME TIDAK BOLEH KOSONG'}
# 		if temp_cust_lat == "" or temp_cust_lat == None:
# 			return {'status': 'ERROR', 'data': 'CUST LATITUDE TIDAK BOLEH KOSONG'}
# 		if temp_cust_long == "" or temp_cust_long == None:
# 			return {'status': 'ERROR', 'data': 'CUST LONGITUDE TIDAK BOLEH KOSONG'}
# 		if temp_unique_code == "" or temp_unique_code == None:
# 			return {'status': 'ERROR', 'data': 'UNIQUE DELIV CODE TIDAK BOLEH KOSONG'}
# 		if(int(str(temp_order_date)[3:5]) > 12):
# 			return {'status': 'ERROR', 'data': 'HARAP MENGGUNAKAN FORMAT TANGGAL ORDER DATE DD/MM/YYYY HH24:MI:SS'}
# 		if(int(str(temp_delv_date)[3:5]) > 12):
# 			return {'status': 'ERROR', 'data': 'HARAP MENGGUNAKAN FORMAT TANGGAL DELIVERY DATE DD/MM/YYYY HH24:MI:SS'}
# 		if(int(str(temp_order_date)[0:2]) > 32):
# 			return {'status': 'ERROR', 'data': 'HARAP MENGGUNAKAN FORMAT TANGGAL ORDER DATE DD/MM/YYYY HH24:MI:SS'}
# 		if(int(str(temp_delv_date)[0:2]) > 32):
# 			return {'status': 'ERROR', 'data': 'HARAP MENGGUNAKAN FORMAT TANGGAL DELIVERY DATE DD/MM/YYYY HH24:MI:SS'}

# 		cekValidAppSource = ValidationCrud.check_valid_application_source(temp_source_name, db)
# 		if(cekValidAppSource.valid_application_source is None):
# 			return {'status': 'ERROR', 'data': 'SOURCE NAME BELUM TERDAFTAR'}

# 		if count_detail > 1000:
# 			return {'status': 'ERROR', 'data': 'DETAIL TIDAK BOLEH LEBIH DARI 1000'}

# 		item_json = json.dumps(item_dict)
# 		TRANSACTION_ID = item.data.header.transaction_id
# 		STORE_CODE = item.data.header.store_site_code
# 		data = {'TRANSACTION_ID': TRANSACTION_ID, 'STORE_CODE': STORE_CODE,
# 				'message': 'STORE {1} With TRANSACTION ID {0} send'.format(TRANSACTION_ID, STORE_CODE)}
# 		command = "/home/goldapi/rabbitmq/python/publisher/emitPostPoVal.py {0} {1} {2} '{3}'".format(
# 			getConfRabbitMQ[0][2], getConfRabbitMQ[0][3], getConfRabbitMQ[0][4], item_json)
# 		os.system(command)
# 		outputData = {'status': 'SUCCESS', 'data': data}
# 		return outputData

# 	except:
# 		return {'status': 'ERROR', 'data': 'Something Went Wrong POST Supplier Order'}

#################################################################################################################################################################


if __name__ == "__main__":
	# app.run()
	serve(app, host='0.0.0.0', port=80)
		#uvicorn.run(app, host="0.0.0.0", port=8008)
