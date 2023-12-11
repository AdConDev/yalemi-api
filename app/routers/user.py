# pylint: disable=E1101
''' Defines the routes for user-related operations in the application. '''

from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session, select
from app.models import User, UserCreate, UserRead, UserUpdate
from app import utils, oauth2, database as db


unauth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

forb_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You don't have enough permissions",
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
    ''' Route used to create a new user '''
    # Checks if a user with the same username or email already exists in the
    # database
    user_in_db = session.exec(
            select(User).where(
                User.username == new_user.username or
                User.email == new_user.email
                )).first()
    # If exists, it raises an exception
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username/email already exists"
        )
    # Hashes the password, creates a new user, and adds it to the database.
    pwd_hash = utils.get_password_hash(new_user.password)
    new_user.password = pwd_hash
    created_user = User.from_orm(new_user)
    session.add(created_user)
    session.commit()
    session.refresh(created_user)
    return created_user


@router.get("/", response_model=list[UserRead])
def get_all_users(
    *,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route used to get all users '''
    # It requires the current user to be authenticated
    if not current_user:
        raise unauth_exception
    # It fetches all users from the database and returns them
    all_users = session.exec(select(User)).all()
    # If there are no users, it raises an exception
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
    ''' Route used to get the latest user '''
    # It requires the current user to be authenticated
    if not current_user:
        raise unauth_exception
    # It fetches the latest user from the database and returns it
    latest_user = session.exec(
        select(User).order_by(User.created_at.desc())  # type: ignore
        ).first()
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
    ''' Route is used to get a specific user by their ID '''
    # It requires the current user to be authenticated
    if not current_user:
        raise unauth_exception
    # It fetches the user with the given ID from the database and returns it
    one_user = session.get(User, user_id)
    # If there is no user with the given ID, it raises an exception
    if not one_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with ID {user_id} found"
        )
    return one_user


@router.put(
    "/{user_id}/", status_code=status.HTTP_202_ACCEPTED,
    response_model=UserRead
)
def put_one_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route used to update a specific user by their ID '''
    # It requires the current user to be authenticated and to be the same as
    # the user being updated
    if current_user.id != user_id:
        raise forb_exception
    # Checks if a user with the same username or email already exists in the
    # database
    if user_update.username:
        username_exist = session.exec(
            select(User).where(User.username == user_update.username)
            ).first()
        # If exists, it raises an exception
        if username_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
                )
    if user_update.email:
        email_exist = session.exec(
            select(User).where(User.email == user_update.email)
            ).first()
        # If exists, it raises an exception
        if email_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
                )
    # If not, it hashes the new password (if provided), updates the user's
    # details, and saves the changes to the database
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
    ''' Route used to delete a specific user by their ID '''
    # It requires the current user to be authenticated and to be the same as
    # the user being deleted
    if current_user.id != user_id:
        raise forb_exception
    # It deletes the user with the given ID from the database
    deleted_user = session.get(User, user_id)
    # If there is no user with the given ID, it raises an exception
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with this id {user_id}"
            )
    session.delete(deleted_user)
    session.commit()
