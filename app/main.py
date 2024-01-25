''' Yet Another Learning Experience Made In Python.
It sets up the FastAPI instance, includes the routers,
and defines the main route.'''

# Import the async context manager
from contextlib import asynccontextmanager
# Import the FastAPI class from the fastapi package
from fastapi import FastAPI
# Import the routers
from app.routers import user, may, auth, vote
# Import the function to create the database
from app.database import create_db


# Create the async context manager
@asynccontextmanager
async def lifespan(api: FastAPI):
    ''' Async context manager is used for startup and shutdown events '''
    # Startup event
    print("Starting up...")
    print(api)
    create_db()
    yield
    # Shutdown event
    print("Shutting down...")

# Create the FastAPI instance
app = FastAPI(lifespan=lifespan)
# Include the routers
app.include_router(user.router)
app.include_router(may.router)
app.include_router(auth.router)
app.include_router(vote.router)


# FastAPI's decorators allow FastAPI to automatically generate interactive API
# documentation, handle requests and responses, and manage the application's
# lifecycle.
@app.get("/")
def get_hello_world():
    ''' Hello World! '''
    return {'FastAPI': 'Hello World!',
            'SQLModel': 'Hello World!',
            'OAuth2': 'Hello World!'
            }
