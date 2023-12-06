''' OAuth2 scheme for authentication '''

from typing import Annotated
from datetime import datetime as dt, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from jose import jwt, JWTError
from app import utils, database as db
from app.models import User, TokenData


SECRET_KEY = "c20429beb3a9aee9430444de3a4535e674a05eaa1101707e56644fb293590a54"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(db.get_session)]
):
    ''' Get current user from token '''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        email = payload.get("email")
        if not username or not email:
            raise credentials_exception
        token_data = TokenData(username=username, email=email)
    except JWTError as exc:
        raise credentials_exception from exc
    user_in_db = session.exec(
            select(User).where(User.username == token_data.username)).first()
    if not user_in_db:
        raise credentials_exception
    return user_in_db


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    ''' Get current user if active '''
    if not current_user.enabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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


def authenticate_user(
    user_in_db: User | None,
    credentials: OAuth2PasswordRequestForm
):
    ''' User authentication '''
    if not user_in_db:
        return False
    pwd_match = utils.verify_password(
        credentials.password, user_in_db.password)
    if not pwd_match:
        return False
    return user_in_db
