''' OAuth2 scheme for authentication '''

from typing import Annotated
from datetime import datetime as dt, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from app import utils
from app.models import User, TokenData
from app import crud, database as db


ENGINE = db.new_engine()


SECRET_KEY = "c20429beb3a9aee9430444de3a4535e674a05eaa1101707e56644fb293590a54"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 5


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    ''' Get current user from token '''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as exc:
        raise credentials_exception from exc
    user_db = crud.select_username(User, token_data.username)
    if user_db:
        return user_db
    raise credentials_exception


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    ''' Get current user if active '''
    if current_user.enabled:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive user")


def create_access_token(data: dict, expire_delta: timedelta | None = None):
    ''' Create access token with expiration time '''
    to_encode = data.copy()
    if expire_delta:
        expire = dt.timestamp(dt.utcnow() + expire_delta)
    else:
        expire = dt.timestamp(
            dt.now() + timedelta(minutes=EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def authenticate_user(table, credentials: OAuth2PasswordRequestForm):
    ''' User authentication '''
    one_user = crud.select_username(table, credentials.username)
    if one_user:
        pwd_match = utils.verify_password(
            credentials.password, one_user.hashed_password)
        if pwd_match:
            return one_user
    return False
