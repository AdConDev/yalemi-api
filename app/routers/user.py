# pylint: disable=E1101
''' Router for Users '''

from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session, select
from app.models import User, UserCreate, UserRead, UserUpdate, UserData
from app import utils, oauth2, database as db


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
def post_one_user(
    *,
    new_user: UserCreate,
    session: Session = Depends(db.get_session)
):
    ''' Create a user '''
    user_in_db = session.exec(
            select(User).where(User.username == new_user.username)).first()
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    pwd_hash = utils.get_password_hash(new_user.password)
    new_user.password = pwd_hash
    created_user = User.from_orm(new_user)
    session.add(created_user)
    session.commit()
    session.refresh(created_user)
    return created_user


@router.get("/", response_model=list[UserRead])
def get_all_user(
    *,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Get all Users '''
    if not current_user:
        raise auth_exception
    all_users = session.exec(select(User)).all()
    if not all_users:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Users yet")
    return all_users


@router.get("/latest/", response_model=UserRead)
def get_latest_user(
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Get latest User '''
    if not current_user:
        raise auth_exception
    query = select(User).order_by(User.created_at.desc())  # type: ignore
    latest_user = session.exec(query).first()
    if not latest_user:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Users yet"
        )
    return latest_user


@router.get("/{user_id}/", response_model=UserRead)
def get_one_user(
    user_id: int,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Get specific User '''
    if not current_user:
        raise auth_exception
    one_user = session.get(User, user_id)
    if not one_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with ID {user_id} found"
        )
    return one_user


@router.put(
    "/{user_id}/", status_code=status.HTTP_202_ACCEPTED,
    response_model=UserData
)
def put_one_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Update specific User if logged in '''
    if current_user.id != user_id:
        raise auth_exception
    if user_update.username:
        username_exist = session.exec(
            select(User).where(User.username == user_update.username)
            ).first()
        if username_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
    if user_update.password:
        pwd_hash = utils.get_password_hash(user_update.password)
        user_update.password = pwd_hash
    edited_user = session.get(User, user_id)
    new_user = user_update.dict(exclude_unset=True)
    for key, value in new_user.items():
        setattr(edited_user, key, value)
    session.add(edited_user)
    session.commit()
    session.refresh(edited_user)
    return edited_user


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_user(
    user_id: int,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Delete specific User '''
    if current_user.id != user_id:
        raise auth_exception
    deleted_user = session.get(User, user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with this id {user_id}"
            )
    session.delete(deleted_user)
    session.commit()
