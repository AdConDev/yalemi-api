''' Router for Users '''

from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from app.models import User, UserCreate, UserRead, UserUpdate, UserData
from app import utils, crud, oauth2


auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


router = APIRouter(
    prefix="/user",
    tags=["Users"]
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def post_one_user(new_user: UserCreate):
    ''' Create a user '''
    pwd_hash = utils.get_password_hash(new_user.hashed_password)
    new_user.hashed_password = pwd_hash
    created_user = crud.insert_one(User, new_user)
    return created_user


@router.get("/", response_model=list[UserRead])
def get_all_user(
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Get all Users '''
    if not current_user:
        raise auth_exception
    all_users = crud.select_all(User)
    if not all_users:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Users yet")
    return all_users


@router.get("/latest/", response_model=UserRead)
def get_latest_user(
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Get latest User '''
    if not current_user:
        raise auth_exception
    latest_user = crud.select_latest(User)
    if not latest_user:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Users yet"
        )
    return latest_user


@router.get("/{id_user}/", response_model=UserRead)
def get_one_user(
    id_user: int,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Get specific User '''
    if not current_user:
        raise auth_exception
    one_user = crud.select_id(User, id_user)
    if not one_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with ID {id_user} found"
            )
    return one_user


@router.put(
    "/{id_user}/", status_code=status.HTTP_202_ACCEPTED,
    response_model=UserData
    )
def put_one_user(
    id_user: int,
    updated_user: UserUpdate,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Update specific User if logged in '''
    if current_user.id != id_user:
        raise auth_exception
    if updated_user.username:
        username = crud.select_username(User, updated_user.username)
        if username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
    if updated_user.nickname:
        nickname = crud.select_nickname(User, updated_user.nickname)
        if nickname:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nickname already exists"
            )
    if updated_user.hashed_password:
        pwd_hash = utils.get_password_hash(updated_user.hashed_password)
        updated_user.hashed_password = pwd_hash
    edited_user = crud.update_id(User, updated_user, id_user)
    return edited_user


@router.delete("/{id_user}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_user(
    id_user: int,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Delete specific User '''
    if current_user.id != id_user:
        raise auth_exception
    deleted_user = crud.delete_id(User, id_user)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with this id {id_user}"
            )
