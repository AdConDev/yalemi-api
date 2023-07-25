''' Crating a simple API with FastAPI '''

from random import randrange
import time
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg

app = FastAPI()
posts_db = []

while True:
    try:
        print("---- CONNECTION TRY ----")
        CONN = psycopg.connect(
            host="localhost",
            user="adcon",
            password="231014",
            dbname='Yalemi Dev'
        )
        cursor = CONN.cursor()
    except psycopg.Error as error:
        print("Error:", str(error))
        print("---- TRYING TO RECONNECT ----")
    else:
        print("---- CONNECTED TO DATABASE ----")
        break
    finally:
        time.sleep(1)


class Post(BaseModel):
    ''' Defining the New Post schema '''
    title: str
    content: str
    published: bool = True


def find_id_index(db_posts: list, id_post: int):
    ''' Find the index of the post with the id in URL '''
    for index, post in enumerate(db_posts):
        if post["id"] == id_post:
            return index
    return None


@app.get("/")
def read_hello_world():
    ''' Hello World! '''
    return {"detail": "Hello World!"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create(post: Post):
    ''' Create a post '''
    new_post = post.model_dump()
    new_post["id"] = randrange(10000)
    if post.published:
        posts_db.append(new_post)
        return {"posts": new_post, "detail": "Post published"}
    return {"posts": new_post, "detail": "Post not published"}


@app.get("/posts")
def read_all():
    ''' Get all posts '''
    if posts_db:
        return {"posts": posts_db}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No posts found"
        )


@app.get("/posts/latest")
def read_latest():
    ''' Get latest post '''
    if posts_db:
        return {"posts": posts_db[-1]}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No posts found"
        )


@app.get("/posts/{id_post}")
def read_one(id_post: int):
    ''' Get specific post '''
    index = find_id_index(posts_db, id_post)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts with this id {id_post}"
            )
    return {"posts": posts_db[index]}


@app.put("/posts/{id_post}", status_code=status.HTTP_202_ACCEPTED)
def update(id_post: int, post: Post):
    ''' Update specific post '''
    index = find_id_index(posts_db, id_post)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts with this id {id_post}"
            )
    edited_post = post.model_dump()
    edited_post["id"] = id_post
    posts_db[index] = edited_post
    return {"posts": posts_db[index]}


@app.delete("/posts/{id_post}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id_post: int):
    ''' Delete specific post '''
    index = find_id_index(posts_db, id_post)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts with this id {id_post}"
            )
    posts_db.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
