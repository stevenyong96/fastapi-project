from datetime import date
from pydantic import BaseModel , Field
from dataclasses import dataclass
from typing import List,Optional, Set

from pydantic import BaseModel , Field

class Items(BaseModel):
	item_code: str
	item_name: str
	item_desc: str
	item_price: int
	item_stock: int
	item_color: str
	item_images1 : Optional[str] = 'https://raw.githubusercontent.com/stevenyong96/fastapi-project/master/images/no_images_available.png'
	item_images2 : Optional[str] = 'https://raw.githubusercontent.com/stevenyong96/fastapi-project/master/images/no_images_available.png' 
	item_images3 : Optional[str] = 'https://raw.githubusercontent.com/stevenyong96/fastapi-project/master/images/no_images_available.png'
	status : Optional[int] = 0
	
	# class Config:
	# 	orm_mode=True

# class User(BaseModel):
# 	NIK: Optional[str] = None
# 	USERNAME: Optional[str] = None
# 	NAMA: Optional[str] = None
# 	EMAIL:	Optional[str] = None
# 	PASSWORD : Optional[str] = None
# 	UTIL:	Optional[str] = None
# 	TOKEN: 	Optional[str] = None 
# 	REMEMBER_TOKEN: Optional[int] = None
# 	STATUS : Optional[int] = None

	# class Config:
	# 	orm_mode=True
	# 	arbitrary_types_allowed = True

# class InsertUsers(BaseModel):
# 	nik: str
# 	username: str
# 	email:	str
# 	password: str



# class S_ART_ATTRIB(BaseModel):
# 	art_code = str
# 	class_code = str
# 	class_short_desc = str
# 	class_long_desc = str
# 	attrib_code = str
# 	attrib_short_desc = str	
# 	attrib_long_desc = str
# 	alphanum_value = str
# 	num_value = int
# 	start_date = str
# 	end_date = str
# 	create_date = date
# 	update_date = date
	
# 	class Config:
# 		orm_mode = True
# 		arbitrary_types_allowed = True
	

# class S_ART_ATTRIB_HDR(BaseModel):
# 	item_code = str
# 	attributes = List[S_ART_ATTRIB]
	
# 	class Config:
# 		orm_mode = True
# 		arbitrary_types_allowed = True

# class S_ART_ATTRIB_RES(BaseModel):
# 	status : str
# 	data : S_ART_ATTRIB_HDR
	
# 	class Config:
# 		orm_mode = True
# 		arbitrary_types_allowed = True