from passlib.context import CryptContext
from util import load_setting
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from exception import AppException,Errorcode
oauth = OAuth2PasswordBearer(tokenUrl= '/auth/login')
pwd = CryptContext(schemes=['bcrypt'])

def hash_password(password: str):
    return pwd.hash(password)
def verify_password(password: str, hashpassword: str):
    return pwd.verify(password, hashpassword)
def encode_token(data: dict, expires: timedelta, type: str):
    exp = datetime.utcnow() + expires
    data.update({'type': type})
    data.update({'exp': exp})
    return jwt.encode(data, key=load_setting.SECRET_KEY)
def decode_token(token: str =Depends(oauth)):
    try:
        payload = jwt.decode(token, load_setting.SECRET_KEY)
        return payload
    except ExpiredSignatureError:
        raise AppException(Errorcode.TOKEN_EXPIRED)
    except JWTError:
        raise AppException(Errorcode.TOKEN_INVALID)
def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, load_setting.SECRET_KEY)
        if payload.get("type") != "refresh":
            raise AppException(Errorcode.TOKEN_INVALID)
        return payload
    except ExpiredSignatureError:
        raise AppException(Errorcode.TOKEN_EXPIRED)
    except JWTError:
        raise AppException(Errorcode.TOKEN_INVALID)
def require_role(Role: list):
    def check(user: dict = Depends(decode_token)):
        if user["role"] in Role:
            return user
        raise AppException(Errorcode.UNAUTHORIZED)
    return check