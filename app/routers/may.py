# pylint: disable=E1101
''' Router for Mayz '''

from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session, select
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
def post_one_may(
    *,
    create_may: MayCreate,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Create a may '''
    if not current_user:
        raise unauth_exception
    new_may = May(user_id=current_user.id, **create_may.dict())
    created_may = May.from_orm(new_may)
    session.add(created_may)
    session.commit()
    session.refresh(created_may)
    return created_may


@router.get("/all/", response_model=list[MayRead])
def get_all_mayz(
    *,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Get all Mayz '''
    if not current_user:
        raise unauth_exception
    all_mayz = session.exec(select(May)).all()
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
    ''' Get all Mayz '''
    if not current_user:
        raise unauth_exception
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
    ''' Get latest may '''
    if not current_user:
        raise unauth_exception
    latest_may = session.exec(
        select(May).order_by(May.created_at.desc())  # type: ignore
        ).first()
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
    ''' Get specific may '''
    if not current_user:
        raise unauth_exception
    one_may = session.get(May, may_id)
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
    ''' Update specific may '''
    if not current_user:
        raise unauth_exception
    edited_may = session.get(May, may_id)
    if not edited_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No May with ID {may_id} found"
            )
    if edited_may.user_id != current_user.id:
        raise forb_exception
    new_may = may_update.dict(exclude_unset=True)
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
    ''' Delete specific may '''
    if not current_user:
        raise unauth_exception
    deleted_may = session.get(May, may_id)
    if not deleted_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No mayz with this id {may_id}"
            )
    if deleted_may.user_id != current_user.id:
        raise forb_exception
    session.delete(deleted_may)
    session.commit()
