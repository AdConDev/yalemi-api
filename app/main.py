''' Crating a Social Media API with FastAPI '''

import time
from fastapi import FastAPI, status, HTTPException
import psycopg
from psycopg.rows import dict_row
from sqlmodel import create_engine
from . import database
from . import schemas

engine = create_engine(database.POSTGRES_URL, echo=True)
database.create_tables(engine)
app = FastAPI()
mayz_db = []


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
def read_hello_world():
    ''' Hello World! '''
    try:
        hello_pg = CONN.execute(""" SELECT version(); """).fetchone()
    except psycopg.OperationalError as hello_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Error"
        ) from hello_error
    if hello_pg is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=""
        )
    hello_pg['detail'] = 'Hello World!'
    return hello_pg


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
        mayz = CONN.execute(""" SELECT * FROM mayz; """).fetchall()
    except psycopg.OperationalError as read_all_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No mayz found"
        ) from read_all_error
    if mayz is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No mayz found"
        )
    return {'data': mayz}


@app.get("/mayz/latest")
def read_latest():
    ''' Get latest may '''
    try:
        latest_may = CONN.execute(
            """ SELECT * FROM mayz
                ORDER BY created_at
                DESC LIMIT 1; """).fetchone()
    except psycopg.OperationalError as read_latest_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No latest may found"
        ) from read_latest_error
    if latest_may is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No mayz found"
        )
    return {'data': latest_may}


@app.get("/mayz/{id_post}")
def read_one(id_post: int):
    ''' Get specific may '''
    try:
        chosen_may = CONN.execute(
            """ SELECT * FROM mayz
                WHERE id_may = %s; """,
            (id_post,)).fetchone()
    except psycopg.OperationalError as read_chosen_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Error"
        ) from read_chosen_error
    if chosen_may is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No mayz found"
        )
    return {'data': chosen_may}


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
