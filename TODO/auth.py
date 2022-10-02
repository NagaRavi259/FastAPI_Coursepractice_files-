from base64 import encode
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import models

from sqlalchemy.orm import Session
from DataBase import sessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError



SECRET_KEY = "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
algorithem = "HS256"



class CreateUser(BaseModel):
    username:str
    email:Optional[str]
    first_name:str
    last_name:str
    password:str

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.base.metadata.create_all(bind=engine)

OAuth2Barrer = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_passowrd(plain_password,hash_password):
    return bcrypt_context.verify(plain_password,hash_password)

def authenticate_user(username:str,password:str,db):
    user = db.query(models.Users).filter(models.Users.username==username).first()
    if not user:
        return False
    if not verify_passowrd(password,user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id:int, expires_delta:Optional[timedelta] = None):
    encode = {"sub":username,"id":user_id}
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=15)
    encode.update({"exp":expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=algorithem) 

async def get_current_user(token:str = Depends(OAuth2Barrer)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[algorithem])
        username:str = payload.get("sub")
        user_id:int= payload.get("id")
        if username is None or user_id is None:
            raise get_user_execption()
        return {"username":username, "id":user_id}

    except JWTError:
        raise get_user_execption()


@app.post("/create/user")
async def create_new_user(create_user :CreateUser, db : Session = Depends(get_db) ):
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name

    hash_password = get_password_hash(create_user.password)

    create_user_model.hashed_password = hash_password
    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()
    return create_user_model

@app.post("/token")
async def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends(),db=Depends(get_db)):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise token_execption()
    token_epires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_epires)

    return {"token":token}

## Execptions
def get_user_execption():
    credentials_execption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate Credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    return credentials_execption

def token_execption():
    token_execption_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="incorrect username or password",
        headers= {"WWW-Authenticate":"Bearer"}
    )
    return token_execption_response