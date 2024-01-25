# pylint: disable=E1101
''' Defines the routes for May-related operations in the application. '''

from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session, select, column
from app.models import May, MayCreate, MayRead, MayUpdate, User
from app import oauth2, database as db


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
    prefix="/may",
    tags=["Mayz"]
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MayRead)
def post_may(
    *,
    create_may: MayCreate,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route to create a May '''
    # Validate user
    if not current_user:
        raise unauth_exception
    # It creates a new May with the data from create_may and the user_id of
    # current_user
    new_may = May.model_validate(create_may, from_attributes=True)
    new_may.user_id = current_user.id
    session.add(new_may)
    session.commit()
    session.refresh(new_may)
    return new_may


@router.get("/all/", response_model=list[MayRead])
def get_all_mayz(
    *,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session),
    limit: int = 100,
    skip: int = 0,
    search: str = ''
):
    ''' Route to get all Mays '''
    # Validate user
    if not current_user:
        raise unauth_exception
    # It gets all Mays that match the search string, skips the first skip Mays,
    # limits the result to limit Mays, and returns them.
    all_mayz = session.exec(
        select(May).where(
            column('title').regexp_match(search, 'i')
            ).offset(skip).limit(limit)
        ).all()
    # If there are no Mays, it raises an exception
    if not all_mayz:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Mayz yet"
            )
    return all_mayz


@router.get("/me/", response_model=list[MayRead])
def get_my_mayz(
    *,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route to get all Mays of the current user '''
    # Validate user
    if not current_user:
        raise unauth_exception
    # It gets all Mays where the user_id is the id of current_user and returns
    # them.
    all_mayz = session.exec(
        select(May).where(May.user_id == current_user.id)
        ).all()
    if not all_mayz:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Mayz yet"
            )
    return all_mayz


@router.get("/latest/", response_model=MayRead)
def get_latest_may(
    *,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route to get the latest May '''
    # Validate user
    if not current_user:
        raise unauth_exception
    # It gets the latest May by created_at and returns it.
    latest_may = session.exec(
        select(May).order_by(May.created_at.desc())  # type: ignore
        ).first()
    # If there are no Mays, it raises an exception
    if not latest_may:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Mayz yet"
            )
    return latest_may


@router.get("/{may_id}/", response_model=MayRead)
def get_may(
    may_id: int,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route to get a specific May '''
    # Validate user
    if not current_user:
        raise unauth_exception
    # It gets the May with the id may_id and returns it.
    one_may = session.get(May, may_id)
    # If there is no May with that id, it raises an exception
    if not one_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No May with ID {may_id} found"
            )
    return one_may


@router.put(
    "/{may_id}/", status_code=status.HTTP_202_ACCEPTED,
    response_model=MayRead)
def put_may(
    may_id: int,
    may_update: MayUpdate,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route to update a specific May '''
    # Validate user
    if not current_user:
        raise unauth_exception
    # It gets the May with the id may_id
    edited_may = session.get(May, may_id)
    # If there is no May with that id, it raises an exception
    if not edited_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No May with ID {may_id} found"
            )
    # If the user is not the owner of the May, it raises an exception
    if edited_may.user_id != current_user.id:
        raise forb_exception
    # It updates the May with the data from may_update and returns it.
    new_may = may_update.model_dump(exclude_unset=True)
    for key, value in new_may.items():
        setattr(edited_may, key, value)
    session.add(edited_may)
    session.commit()
    session.refresh(edited_may)
    return edited_may


@router.delete("/{may_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_may(
    may_id: int,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route to delete a specific May '''
    # Validate user
    if not current_user:
        raise unauth_exception
    # It gets the May with the id may_id
    deleted_may = session.get(May, may_id)
    # If there is no May with that id, it raises an exception
    if not deleted_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No mayz with this id {may_id}"
            )
    # If the user is not the owner of the May, it raises an exception
    if deleted_may.user_id != current_user.id:
        raise forb_exception
    # It deletes the May and returns nothing.
    session.delete(deleted_may)
    session.commit()
