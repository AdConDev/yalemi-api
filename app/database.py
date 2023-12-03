''' Database connection and setup using SQLModel '''

from sqlmodel import create_engine
from app import models


def new_engine():
    ''' Create database engine '''
    return create_engine(POSTGRES_URL, echo=True)


def create_db():
    ''' Create database and tables '''
    models.SQLModel.metadata.create_all(new_engine())


POSTGRES_FILE = "yalemi-dev"
POSTGRES_URL = f"postgresql://adcon:231014@localhost/{POSTGRES_FILE}"
