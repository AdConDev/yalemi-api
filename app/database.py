''' Responsible for setting up the database connection and providing a session
for database operations '''

from sqlmodel import create_engine, Session
from app import models
from app.config import env


# Database connection
DATABASE_CONN = env.database_url()
engine = create_engine(DATABASE_CONN, echo=True)


def get_session():
    ''' Dependency in FastAPI routes to provide a session for database
    operations '''
    # The session is automatically committed and closed when the request is
    # finished.
    with Session(engine) as session:
        yield session


def create_db():
    ''' Creates the database and tables '''
    # It's called during application startup to ensure that the database and
    # tables exist before the application starts serving requests.
    models.SQLModel.metadata.create_all(engine)
