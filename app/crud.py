''' CRUD Operations for database '''

from sqlmodel import Session, select, SQLModel, engine


def select_all(sql_engine: engine, model: SQLModel):
    ''' Select all rows from database '''
    with Session(sql_engine) as session:
        return session.exec(select(model)).all()


def select_one(sql_engine: engine, model: SQLModel, value: int):
    ''' Select all Mayz from database '''
    with Session(sql_engine) as session:
        return session.exec(
            select(model).where(model.id_may == value)).one_or_none()


def select_latest(sql_engine: engine, model: SQLModel):
    ''' Select all Mayz from database '''
    with Session(sql_engine) as session:
        return session.exec(
            select(model).order_by(model.created_at.desc())).first()
