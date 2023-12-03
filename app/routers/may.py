''' Router for Mayz '''

from fastapi import APIRouter, status, HTTPException
from app.models import May, MayCreate, MayRead, MayUpdate
from app import crud, database as db


ENGINE = db.new_engine()
router = APIRouter(
    prefix="/may",
    tags=["Mayz"]
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MayRead)
def post_one_may(new_may: MayCreate):
    ''' Create a may '''
    created_may = crud.insert_one(May, new_may)
    return created_may


@router.get("/", response_model=list[MayRead])
def get_all_may():
    ''' Get all Mayz '''
    all_mayz = crud.select_all(May)
    if all_mayz:
        return all_mayz
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Mayz yet"
    )


@router.get("/latest/", response_model=MayRead)
def get_latest_may():
    ''' Get latest may '''
    latest_may = crud.select_latest(May)
    if latest_may:
        return latest_may
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Mayz yet"
    )


@router.get("/{id_may}/", response_model=MayRead)
def get_one_may(id_may: int):
    ''' Get specific may '''
    one_may = crud.select_id(May, id_may)
    if one_may:
        return one_may
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No May with ID {id_may} found"
        )


@router.put(
    "/{id_may}/", status_code=status.HTTP_202_ACCEPTED,
    response_model=MayRead)
def put_one_may(id_may: int, updated_may: MayUpdate):
    ''' Update specific may '''
    edited_may = crud.update_id(May, updated_may, id_may)
    if edited_may:
        return edited_may
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No May with ID {id_may} found"
        )


@router.delete("/{id_may}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_may(id_may: int):
    ''' Delete specific may '''
    deleted_may = crud.delete_id(May, id_may)
    if not deleted_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No mayz with this id {id_may}"
            )
