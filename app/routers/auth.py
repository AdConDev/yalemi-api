''' Responsible for handling the authentication routes of application '''

from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.models import User, Token, UserRead
from app import oauth2, database as db

# API router
router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
    )


# Login
@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(db.get_session)
):
    ''' Login route '''
    # It checks if the username and password from form_data are not None,
    # gets the user from the database, authenticates the user,
    # and creates an access token.
    if form_data.username is None or form_data.password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password"
            )
    # Get user
    user = session.exec(
        select(User).where(User.username == form_data.username)
        ).first()
    # Authenticate user
    user_auth = oauth2.authenticate_user(user, form_data)
    if not user_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
            )
    # Create access token
    access_token = oauth2.create_access_token(
        data={'username': user_auth.username, 'email': user_auth.email}
        )
    # It returns a dictionary with the access token and the token type.
    return {'access_token': access_token, "token_type": "bearer"}


# Get current user
@router.get("/me/", response_model=UserRead)
def read_users_me(
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Get current user '''
    # Returns data of the current user
    return current_user
