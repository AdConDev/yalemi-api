''' Router for authentication '''

from fastapi import APIRouter, HTTPException, status
from app.models import UserLogin, User
from app import utils, crud, database as db


ENGINE = db.new_engine()
router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
    )


@router.post(
    "/", status_code=status.HTTP_202_ACCEPTED)
def login(user: UserLogin):
    ''' Login a user '''
    one_user = crud.select_email(ENGINE, User, user.email)
    if one_user:
        pwd_match = utils.verify(
            user.hashed_password, one_user.hashed_password)
        if pwd_match:
            return {one_user.username: "Logged in", "token": "Example Token"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Invalid email or password"
    )
