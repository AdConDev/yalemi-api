''' Router for Users '''


from fastapi import APIRouter, status, HTTPException
from app.models import User, UserCreate, UserRead, UserUpdate
from app import utils, crud, database as db


ENGINE = db.new_engine()
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
def get_all_user():
    ''' Get all Users '''
    all_users = crud.select_all(User)
    if all_users:
        return all_users
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Users yet"
    )


@router.get("/latest/", response_model=UserRead)
def get_latest_user():
    ''' Get latest User '''
    latest_user = crud.select_latest(User)
    if latest_user:
        return latest_user
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Users yet"
    )


@router.get("/{id_user}/", response_model=UserRead)
def get_one_user(id_user: int):
    ''' Get specific User '''
    one_user = crud.select_id(User, id_user)
    if one_user:
        return one_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No User with ID {id_user} found"
        )


@router.put(
    "/{id_user}/", status_code=status.HTTP_202_ACCEPTED,
    response_model=UserRead
    )
def put_one_user(id_user: int, updated_user: UserUpdate):
    ''' Update specific User '''
    if updated_user.hashed_password:
        pwd_hash = utils.get_password_hash(updated_user.hashed_password)
        updated_user.hashed_password = pwd_hash
    edited_user = crud.update_id(User, updated_user, id_user)
    if edited_user:
        return edited_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No User with ID {id_user} found"
        )


@router.delete("/{id_user}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_user(id_user: int):
    ''' Delete specific User '''
    deleted_user = crud.delete_id(User, id_user)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with this id {id_user}"
            )
