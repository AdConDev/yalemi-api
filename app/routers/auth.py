''' Router for authentication '''

from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models import User, Token, UserRead
from app import database as db
from app import oauth2


ENGINE = db.new_engine()
router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
    )


@router.post(
    "/", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    ''' Login a user '''
    user = oauth2.authenticate_user(User, form_data)
    if user:
        access_token = oauth2.create_access_token(
                data={"sub": user.username}
            )
        return {'access_token': access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Invalid email or password"
    )


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
