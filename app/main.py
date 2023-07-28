''' Crating a Social Media API with FastAPI '''

from fastapi import FastAPI, status, HTTPException
try:
    from . import database as db
    from . import schemas
    from . import crud
    from . import models
except ImportError:
    import database as db
    import schemas
    import crud
    import models

db.create_db(ENGINE := db.new_engine())
app = FastAPI()


@app.post("/mayz", status_code=status.HTTP_201_CREATED)
def post_new_may(may: schemas.May):
    ''' Create a may '''
    try:
        new_may = crud.insert_one(ENGINE, models.May, may)
    except Exception as create_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid data schema"
        ) from create_error
    return {"data": new_may}


@app.get("/")
def get_hello_http():
    ''' Hello World, HTTP! '''
    try:
        crud.select_all(ENGINE, models.May)
    except Exception as hello_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="HTTP/SQLModel Error"
        ) from hello_error
    return {'http': 'Hello World!', 'SQLModel': 'Hello World!'}


@app.get("/mayz", status_code=status.HTTP_200_OK)
def get_all_may():
    ''' Get all mayz '''
    try:
        mayz = crud.select_all(ENGINE, models.May)
    except Exception as read_all_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Read all error"
        ) from read_all_error
    if mayz:
        return {'data': mayz}
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Mayz yet"
    )


@app.get("/mayz/latest")
def get_latest_may():
    ''' Get latest may '''
    try:
        latest_may = crud.select_latest(ENGINE, models.May)
    except Exception as read_latest_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Read all error"
        ) from read_latest_error
    if latest_may:
        return {'data': latest_may}
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No Mayz yet"
    )


@app.get("/mayz/{id_post}")
def get_one_may(id_post: int):
    ''' Get specific may '''
    try:
        may = crud.select_id(ENGINE, models.May, id_post)
    except Exception as read_one_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Read all error"
        ) from read_one_error
    if may:
        return {'data': may}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No Mayz found"
        )


@app.put("/mayz/{id_post}", status_code=status.HTTP_202_ACCEPTED)
def put_one_may(id_post: int, may: schemas.May):
    ''' Update specific may '''
    try:
        updated_may = crud.update_id(ENGINE, models.May, id_post, may)
    except Exception as update_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Update Error"
        ) from update_error
    if updated_may is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No mayz with this id {id_post}"
            )
    return {"data": updated_may}


@app.delete("/mayz/{id_post}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_may(id_post: int):
    ''' Delete specific may '''
    try:
        deleted_may = crud.delete_id(ENGINE, models.May, id_post)
        if not deleted_may:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No mayz with this id {id_post}"
                )
    except Exception as delete_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Error"
        ) from delete_error


if __name__ == "__main__":
    db.create_mockup_mayz(ENGINE)
