from fastapi import Fastapi, Path
from typing import Optional
from pydantic import BaseModel

app = FastApi()

users = {
    1: {
        "id": 1,
        "username": "steven",
        "password": "steven",
        "nama": "steven",
        "email": "steven.yong@outlook.com",
    }
}

class Users(BaseModel):
    id: int
    username: str
    password: str
    nama: str
    email: str

class UpdateUsers(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    nama: Optional[str] = None
    email: Optional[str] = None

@app.get("/")
def index():
    return {"message": "Hello Binar"}

@app.get("/users")
def get_users():
    try:
        return users
    except:
        return {"status": "ERROR" , "message" : "Something Went Wrong"}

@app.get("/users/{p_username}")
def get_one_user(p_username: str):
    try:
        for i in users:
            if users[i]["username"] == p_username:
                return {"status": "SUCCESS"  , "message": users[i]}
        return {"status": "ERROR" , "message" : "Username Not Found"}
    except:
        return {"status": "ERROR" , "message" : "Something Went Wrong"}

@app.post("/create_users_1/{p_username}")
def create_users(p_username: str, user: Users):
    try:
        if p_username in users:
            return {"status": "ERROR" , "message" : "Failed To Create Username Exists"}
        size = len(user)
        user[size+1]= user
        return {"status": "SUCCESS" , "message" : user[size+1]}
    except:
        return {"status": "ERROR" , "message" : "Something Went Wrong"}

@app.post("/create_users_2/{p_user_id}")
def create_users(p_user_id: int, user: Users):
    try:
        if p_user_id in users:
            return {"status": "ERROR" , "message" : "Failed To Create Username Exists"}
        users[p_user_id] = user
        return {"status": "SUCCESS" , "message" : user[p_user_id]}
    except:
        return {"status": "ERROR" , "message" : "Something Went Wrong"}

@app.put("/update_users/{p_user_id}")
def update_users(p_user_id: int , user: UpdateUsers):
    try:
        if p_user_id not in users:
            return {"status": "ERROR" , "message" : "Username Does Not Exists"}
        
        if user.username != None:
            users[p_user_id].username = user.username
        else:
            return {"status": "ERROR" , "message" : "Username Is Blank"}
        
        if user.password != None:
            users[p_user_id].password = user.password
        else:
            return {"status": "ERROR" , "message" : "Password Is Blank"}
        
        if user.nama != None:
            users[p_user_id].nama = user.nama
        else:
            return {"status": "ERROR" , "message" : "Nama Is Blank"}
        
        if user.email != None:
            users[p_user_id].email = user.email
        else:
            return {"status": "ERROR" , "message" : "Email Is Blank"}
        
        return {"status": "SUCCESS" , "message" : users[p_user_id]}

    except:
        return {"status": "ERROR" , "message" : "Something Went Wrong"}


@app.delete("/delete-users/{p_user_id}")
def delete_user(p_user_id: int):
    try:
        if p_user_id not in users:
            return {"status": "ERROR" , "message" : "User Does Not Exists"}
        del users[p_user_id]
        return {"status": "SUCCESS" , "message" : "User Deleted Successfully"}
    except:
        return {"status": "ERROR" , "message" : "Something Went Wrong"}
