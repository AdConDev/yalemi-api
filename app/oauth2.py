''' Responsible for handling OAuth2 authentication '''


from typing import Annotated, Optional
from datetime import datetime as dt, timedelta
from datetime import timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from jose import jwt, JWTError
from app import utils, database as db
from app.models import User, TokenData
from app.config import EnvSettings

env = EnvSettings()

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
    ''' Get current user from token and validates credentials '''
    try:
        # It decodes the token to get the username and email. If the username
        # or email is not found in the token, it raises an exception.
        payload = jwt.decode(token, env.secret_key, algorithms=[env.algorithm])
        username = payload.get("username")
        email = payload.get("email")
        token_data = TokenData(username=username, email=email)
    except JWTError as exc:
        raise credentials_exception from exc
    # If the user is not found, it raises an exception. If the user is found,
    # it returns the user.
    if user_in_db := session.exec(
            select(User).where(User.username == token_data.username)
    ).first():
        return user_in_db
    raise credentials_exception


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    ''' Get current user if active '''
    # It checks if the user is active.
    if not current_user.enabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_access_token(data: dict, expire_delta: timedelta | None = None):
    ''' Create access token with expiration time '''
    # It creates a JWT token with the given data and expiration time.
    to_encode = data.copy()
    if expire_delta:
        expire = dt.timestamp(dt.now(timezone.utc) + expire_delta)
    else:
        expire = dt.timestamp(
            dt.now() + timedelta(minutes=env.expire_minutes))
    to_encode['exp'] = expire
    # The token is encoded with the secret key and algorithm from the
    # environment variables.

    return jwt.encode(to_encode, env.secret_key, env.algorithm)


def authenticate_user(
    user_in_db: Optional[User],
    credentials: OAuth2PasswordRequestForm
) -> bool | User:
    ''' User authentication '''
    # It checks if the user exists and if the password from the credentials
    # matches the password of the user.
    if not user_in_db:
        return False
    pwd_match = utils.verify_password(
        credentials.password, user_in_db.password)
    # If the user exists and the passwords match, it returns the user.
    return user_in_db if pwd_match else False
