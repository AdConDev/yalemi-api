''' Crating a Social Media API with FastAPI '''

import time
from fastapi import FastAPI, status, HTTPException
import psycopg
from psycopg.rows import dict_row
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

ENGINE = db.new_engine()
db.create_db(ENGINE)
app = FastAPI()


while True:
    print("---- CONNECTION TRY ----")
    try:
        CONN = psycopg.connect(
            host="localhost",
            user="adcon",
            password="231014",
            dbname='Yalemi Dev',
            row_factory=dict_row
        )
    except psycopg.Error as error:
        print("Error:", str(error))
        print("---- TRYING TO RECONNECT ----")
    else:
        print("---- CONNECTED TO DATABASE ----")
        break
    finally:
        time.sleep(1)


@app.get("/")
def read_hello_http():
    ''' Hello World, HTTP! '''
    try:
        crud.select_all(ENGINE, models.May)
    except Exception as hello_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="HTTP/SQLModel Error"
        ) from hello_error
    return {'http': 'Hello World!', 'SQLModel': 'Hello World!'}


@app.post("/mayz", status_code=status.HTTP_201_CREATED)
def create(may: schemas.May):
    ''' Create a may '''
    try:
        new_post = CONN.execute(
            """ INSERT INTO mayz (title, content, published)
                VALUES (%s, %s, %s)
                RETURNING *; """,
            (may.title, may.content, may.published)).fetchone()
    except psycopg.OperationalError as create_error:
        CONN.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid data schema"
        ) from create_error
    CONN.commit()
    return {"data": new_post}


@app.get("/mayz", status_code=status.HTTP_200_OK)
def read_all():
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
def read_latest():
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
def read_one(id_post: int):
    ''' Get specific may '''
    try:
        may = crud.select_one(ENGINE, models.May, id_post)
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
def update(id_post: int, may: schemas.May):
    ''' Update specific may '''
    try:
        updated_may = CONN.execute(
            """ UPDATE mayz SET title = %s, content = %s, published = %s
            WHERE id_may = %s
            RETURNING *; """,
            (may.title, may.content, may.published, id_post)).fetchone()
    except psycopg.OperationalError as update_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Error"
        ) from update_error
    if updated_may is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No mayz with this id {id_post}"
            )
    return {"data": updated_may}


@app.delete("/mayz/{id_post}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id_post: int):
    ''' Delete specific may '''
    try:
        deleted_may = CONN.execute(
            """ DELETE FROM mayz WHERE id_may = %s RETURNING *; """,
            (id_post,)).fetchone()
        CONN.commit()
        if deleted_may is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No mayz with this id {id_post}"
                )
    except psycopg.OperationalError as delete_error:
        CONN.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Error"
        ) from delete_error


if __name__ == "__main__":
    db.create_mayz(ENGINE)
