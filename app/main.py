''' Crating a Social Media API with FastAPI '''

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import user, may, auth
from app.database import create_db


@asynccontextmanager
async def lifespan(api: FastAPI):
    ''' Startup and shutdown event '''
    # Startup event
    print("Starting up...")
    print(api)
    create_db()
    yield
    # Shutdown event
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
app.include_router(may.router)
app.include_router(auth.router)


@app.get("/")
def get_hello_world():
    ''' Hello World! '''
    return {'FastAPI': 'Hello World!',
            'SQLModel': 'Hello World!',
            'OAuth2': 'Hello World!'
            }
