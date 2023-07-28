''' CRUD Operations for database '''

from sqlmodel import Session, select, SQLModel, engine
try:
    from .schemas import BaseModel
except ImportError:
    from schemas import BaseModel


def insert_one(sql_engine: engine, model: SQLModel, schema: BaseModel):
    ''' Add May to table '''
    may = model(**schema.dict())
    with Session(sql_engine) as session:
        session.add(may)
        session.commit()
        session.refresh(may)
    return may


def select_all(sql_engine: engine, model: SQLModel):
    ''' Select all rows from database '''
    with Session(sql_engine) as session:
        query = session.exec(select(model)).all()
    return query


def select_id(sql_engine: engine, model: SQLModel, value: int):
    ''' Select one May from database '''
    with Session(sql_engine) as session:
        query = session.get(model, value)
    return query


def select_latest(sql_engine: engine, model: SQLModel):
    ''' Select all Mayz from database '''
    with Session(sql_engine) as session:
        query = session.exec(
            select(model).order_by(model.created_at.desc())).first()
    return query


def update_id(
    sql_engine: engine, model: SQLModel, value: int, schema: BaseModel
):
    ''' Select one May from database '''
    with Session(sql_engine) as session:
        query = session.get(model, value)
        if query:
            query.title = schema.title
            query.content = schema.content
            session.add(query)
            session.commit()
            session.refresh(query)
    return query


def delete_id(sql_engine: engine, model: SQLModel, value: int):
    ''' Select one May from database '''
    with Session(sql_engine) as session:
        query = session.get(model, value)
        if query:
            session.delete(query)
            session.commit()
            return True
    return False
