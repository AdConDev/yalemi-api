''' Router for Mayz '''

from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from app.models import May, MayCreate, MayRead, MayUpdate, User
from app import crud, oauth2


auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

router = APIRouter(
    prefix="/may",
    tags=["Mayz"]
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MayRead)
def post_one_may(
    new_may: MayCreate,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Create a may '''
    if not current_user:
        raise auth_exception
    created_may = crud.insert_one(May, new_may)
    return created_may


@router.get("/", response_model=list[MayRead])
def get_all_may(
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Get all Mayz '''
    if not current_user:
        raise auth_exception
    all_mayz = crud.select_all(May)
    if not all_mayz:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Mayz yet"
            )
    return all_mayz


@router.get("/latest/", response_model=MayRead)
def get_latest_may(
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Get latest may '''
    if not current_user:
        raise auth_exception
    latest_may = crud.select_latest(May)
    if not latest_may:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Mayz yet"
            )
    return latest_may


@router.get("/{id_may}/", response_model=MayRead)
def get_one_may(
    id_may: int,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Get specific may '''
    if not current_user:
        raise auth_exception
    one_may = crud.select_id(May, id_may)
    if not one_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No May with ID {id_may} found"
            )
    return one_may


@router.put(
    "/{id_may}/", status_code=status.HTTP_202_ACCEPTED,
    response_model=MayRead)
def put_one_may(
    id_may: int,
    updated_may: MayUpdate,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Update specific may '''
    if not current_user:
        raise auth_exception
    edited_may = crud.update_id(May, updated_may, id_may)
    if not edited_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No May with ID {id_may} found"
            )
    return edited_may


@router.delete("/{id_may}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_may(
    id_may: int,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)]
):
    ''' Delete specific may '''
    if not current_user:
        raise auth_exception
    deleted_may = crud.delete_id(May, id_may)
    if not deleted_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No mayz with this id {id_may}"
            )
