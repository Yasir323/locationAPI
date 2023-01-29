import time
from typing import Union, Dict

from passlib.context import CryptContext
from jose import jwt

from conf import SECRET_KEY, REFRESH_SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class TooManyVehiclesException(Exception):
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(users_db, username: str) -> Union[Dict, None]:
    if username in users_db:
        return users_db[username]


def authenticate_user(users_db, username: str, password: str) -> Union[Dict, bool]:
    user = get_user(users_db, username)
    if not user:
        return False
    hashed_password = get_password_hash(user['password'])
    if not verify_password(password, hashed_password):
        return False
    return user


def create_access_token(data: str, expiry_seconds: Union[int, None] = 1):
    expire = int(time.time()) + expiry_seconds
    to_encode = {'exp': expire, 'sub': data}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: str, expiry_seconds: Union[int, None] = 24):
    expire = int(time.time()) + expiry_seconds
    to_encode = {'exp': expire, 'sub': data}
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
