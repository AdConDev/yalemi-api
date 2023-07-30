''' Database connection and setup using SQLModel '''

from sqlmodel import create_engine, Session, engine
try:
    from . import models
except ImportError:
    import models


def new_engine():
    ''' Create database engine '''
    return create_engine(POSTGRES_URL, echo=True)


def create_db(sql_engine: engine):
    ''' Create database and tables '''
    models.SQLModel.metadata.create_all(sql_engine)


def create_mockup_mayz(sql_engine: engine):
    ''' Add mockup rows to Mayz table '''
    may_1 = models.May(
        title="May 1st",
        content="May the 1st be with you"
        )
    may_2 = models.May(
        title="May 2nd",
        content="May the 2nd be with you",
        published=False
        )
    may_3 = models.May(
        title="May 3rd",
        content="May the 3rd be with you"
        )
    with Session(sql_engine) as session:
        session.add(may_1)
        session.add(may_2)
        session.add(may_3)
        session.commit()


POSTGRES_FILE = "yalemi-dev"
POSTGRES_URL = f"postgresql://adcon:231014@localhost/{POSTGRES_FILE}"
