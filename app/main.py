''' Crating a Social Media API with FastAPI '''

from contextlib import asynccontextmanager
import sys
from fastapi import FastAPI, status, HTTPException
from passlib.context import CryptContext
from . import database as db
from . import crud
from .models import May, MayCreate, MayRead, MayUpdate
from .models import User, UserCreate, UserRead, UserUpdate

ENGINE = db.new_engine()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@asynccontextmanager
async def lifespan(api: FastAPI):
    ''' Startup and shutdown event '''
    # Startup event
    print("Starting up...")
    print(sys.getsizeof(api))
    db.create_db(ENGINE)
    yield
    # Shutdown event
    print("Shutting down...")
    print(sys.getsizeof(api))


app = FastAPI(lifespan=lifespan)


@app.post("/may", status_code=status.HTTP_201_CREATED, response_model=MayRead)
def post_one_may(new_may: MayCreate):
    ''' Create a may '''
    created_may = crud.insert_one(ENGINE, May, new_may)
    return created_may


@app.get("/")
def get_hello_world():
    ''' Hello World! '''
    crud.select_all(ENGINE, May)
    return {'FastAPI': 'Hello World!', 'SQLModel': 'Hello World!'}


@app.get("/may", response_model=list[MayRead])
def get_all_may():
    ''' Get all Mayz '''
    all_mayz = crud.select_all(ENGINE, May)
    if all_mayz:
        return all_mayz
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Mayz yet"
    )


@app.get("/may/latest", response_model=MayRead)
def get_latest_may():
    ''' Get latest may '''
    latest_may = crud.select_latest(ENGINE, May)
    if latest_may:
        return latest_may
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Mayz yet"
    )


@app.get("/may/{id_may}", response_model=MayRead)
def get_one_may(id_may: int):
    ''' Get specific may '''
    one_may = crud.select_id(ENGINE, May, id_may)
    if one_may:
        return one_may
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No May with ID {id_may} found"
        )


@app.put(
    "/may/{id_may}", status_code=status.HTTP_202_ACCEPTED,
    response_model=MayRead)
def put_one_may(id_may: int, updated_may: MayUpdate):
    ''' Update specific may '''
    edited_may = crud.update_id(ENGINE, May, updated_may, id_may)
    if edited_may:
        return edited_may
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No May with ID {id_may} found"
        )


@app.delete("/may/{id_may}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_may(id_may: int):
    ''' Delete specific may '''
    deleted_may = crud.delete_id(ENGINE, May, id_may)
    if not deleted_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No mayz with this id {id_may}"
            )


@app.post(
    "/user", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def post_one_user(new_user: UserCreate):
    ''' Create a user '''
    created_user = crud.insert_one(ENGINE, User, new_user)
    return created_user


@app.get("/user", response_model=list[UserRead])
def get_all_user():
    ''' Get all Users '''
    all_users = crud.select_all(ENGINE, User)
    if all_users:
        return all_users
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Users yet"
    )


@app.get("/user/latest", response_model=UserRead)
def get_latest_user():
    ''' Get latest User '''
    latest_user = crud.select_latest(ENGINE, User)
    if latest_user:
        return latest_user
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Users yet"
    )


@app.get("/user/{id_user}", response_model=UserRead)
def get_one_user(id_user: int):
    ''' Get specific User '''
    one_user = crud.select_id(ENGINE, User, id_user)
    if one_user:
        return one_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No User with ID {id_user} found"
        )


@app.put(
    "/user/{id_user}", status_code=status.HTTP_202_ACCEPTED,
    response_model=UserRead)
def put_one_user(id_user: int, updated_user: UserUpdate):
    ''' Update specific User '''
    edited_user = crud.update_id(ENGINE, User, updated_user, id_user)
    if edited_user:
        return edited_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No User with ID {id_user} found"
        )


@app.delete("/user/{id_user}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_user(id_user: int):
    ''' Delete specific User '''
    deleted_user = crud.delete_id(ENGINE, User, id_user)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with this id {id_user}"
            )
