''' Database connection and setup using SQLModel '''

from sqlmodel import create_engine
from . import models


def new_engine():
    ''' Create database engine '''
    return create_engine(POSTGRES_URL, echo=True)


def create_db(sql_engine):
    ''' Create database and tables '''
    models.SQLModel.metadata.create_all(sql_engine)


POSTGRES_FILE = "yalemi-dev"
POSTGRES_URL = f"postgresql://adcon:231014@localhost/{POSTGRES_FILE}"
