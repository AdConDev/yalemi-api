''' Router for authentication '''

from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.models import User, Token, UserRead
from app import oauth2, database as db


router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
    )


@router.post(
    "/", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(db.get_session)
):
    ''' Login a user '''
    user = session.exec(
            select(User).where(User.username == form_data.username)).first()
    user_auth = oauth2.authenticate_user(user, form_data)
    if not user_auth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password"
        )
    access_token = oauth2.create_access_token(
            data={'sub': user_auth.username}
        )
    return {'access_token': access_token, "token_type": "bearer"}


@router.get("/me/", response_model=UserRead)
def read_users_me(
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Get authenticated current user '''
    return current_user


@router.get("/me/mayz/")
def read_own_items(
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Get authenticated current user mayz '''
    return [{"may_id": 100, "owner": current_user.nickname}]
