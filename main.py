import time
from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi import (
    FastAPI,
    status,
    HTTPException,
    Depends
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from conf import SECRET_KEY, ALGORITHM, USERS_DB, ACCESS_TOKEN_EXPIRE_SECONDS, REFRESH_ACCESS_TOKEN_EXPIRE_SECONDS
import crud
import database
import schemas
import utils

database.Base.metadata.create_all(bind=database.engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="generateToken")
app = FastAPI()


def get_db():
    """Dependency"""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def token_validation(token: str = Depends(oauth2_scheme)) -> Union[schemas.User, None]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': "Bearer"}
    )
    token_expired_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
        headers={'WWW-Authenticate': "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
        username: str = token_data.sub
        if username is None:
            raise credentials_exception
        if token_data.exp < int(time.time()):
            raise token_expired_exception
        # token_data = schemas.TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = utils.get_user(USERS_DB, username=token_data.sub)
    if user is None:
        raise credentials_exception
    return schemas.User(username=user['username'])


@app.post("/token/", response_model=schemas.Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = utils.authenticate_user(USERS_DB, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Check credentials"
        )
    return {
        'access_token': utils.create_access_token(
            data=user['username'],
            expiry_seconds=ACCESS_TOKEN_EXPIRE_SECONDS),
        'refresh_token': utils.create_refresh_token(
            data=user['username'],
            expiry_seconds=REFRESH_ACCESS_TOKEN_EXPIRE_SECONDS)
    }


@app.post("/location/", response_model=schemas.Data, status_code=status.HTTP_201_CREATED)
async def store_location_data(payload: schemas.InData,
                              # auth_key: str = Query(default=..., alias="authKey", min_length=3),
                              # location: Union[HttpUrl, None] = Header(default=None, convert_underscores=False)):
                              # location: Union[str, None] = Header(default=None, convert_underscores=False),
                              user: schemas.User = Depends(token_validation),
                              db: Session = Depends(get_db)):
    """
    Store data in db with the information provided:

    :param payload: The data to be stored (Raw Data)
    :param user: schemas.User
    :param db: Database connection
    :return: The data stored
    """
    if user:
        # out_data = await store_data_in_db(payload)
        try:
            out_data = crud.store_location_data(db, payload)
        except utils.TooManyVehiclesException as err:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=str(err)
            )
        return jsonable_encoder(out_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong Authentication Key"
        )
