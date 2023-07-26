''' Database connection and setup using SQLModel '''

from sqlmodel import create_engine
from models import SQLModel


def create_db_and_tables():
    ''' Create database and tables '''
    engine = create_engine(POSTGRES_URL, echo=True)
    SQLModel.metadata.create_all(engine)


POSTGRES_FILE = "yalemi-dev"
POSTGRES_URL = f"postgresql://adcon:231014@localhost/{POSTGRES_FILE}"


if __name__ == "__main__":
    create_db_and_tables()
