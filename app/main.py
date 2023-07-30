''' Crating a Social Media API with FastAPI '''

from fastapi import FastAPI, status, HTTPException
from . import database as db
from . import crud
from .models import MayRead, MayCreate, MayUpdate, May

ENGINE = db.new_engine()
app = FastAPI()


@app.on_event("startup")
def startup_event():
    ''' Startup event '''
    db.create_db(ENGINE)


@app.post("/mayz", status_code=status.HTTP_201_CREATED, response_model=MayRead)
def post_one_may(new_may: MayCreate):
    ''' Create a may '''
    created_may = crud.insert_one(ENGINE, May, new_may)
    return created_may


@app.get("/")
def get_hello_world():
    ''' Hello World! '''
    crud.select_all(ENGINE, May)
    return {'FastAPI': 'Hello World!', 'SQLModel': 'Hello World!'}


@app.get("/mayz", response_model=list[MayRead])
def get_all_may():
    ''' Get all Mayz '''
    all_mayz = crud.select_all(ENGINE, May)
    if all_mayz:
        return all_mayz
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Mayz yet"
    )


@app.get("/mayz/latest", response_model=MayRead)
def get_latest_may():
    ''' Get latest may '''
    latest_may = crud.select_latest(ENGINE, May)
    if latest_may:
        return latest_may
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Mayz yet"
    )


@app.get("/mayz/{id_post}", response_model=MayRead)
def get_one_may(id_post: int):
    ''' Get specific may '''
    may_id = crud.select_id(ENGINE, May, id_post)
    if may_id:
        return may_id
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No May with ID {id_post} found"
        )


@app.put(
    "/mayz/{id_post}", status_code=status.HTTP_202_ACCEPTED,
    response_model=MayRead)
def put_one_may(id_post: int, updated_may: MayUpdate):
    ''' Update specific may '''
    edited_may = crud.update_id(ENGINE, May, updated_may, id_post)
    if edited_may:
        return edited_may
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No May with ID {id_post} found"
        )


@app.delete("/mayz/{id_post}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_may(id_post: int):
    ''' Delete specific may '''
    deleted_may = crud.delete_id(ENGINE, May, id_post)
    if not deleted_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No mayz with this id {id_post}"
            )
