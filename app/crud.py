''' CRUD Operations for database '''

from sqlmodel import Session, select, SQLModel, engine


def insert_one(sql_eng: engine, table: SQLModel(table=True), model: SQLModel):
    ''' Add one entry to table '''
    with Session(sql_eng) as session:
        new_row = table.from_orm(model)
        session.add(new_row)
        session.commit()
        session.refresh(new_row)
        return new_row


def select_all(sql_eng: engine, table: SQLModel(table=True)):
    ''' Select all rows from table '''
    with Session(sql_eng) as session:
        all_rows = session.exec(select(table)).all()
        return all_rows


def select_latest(sql_eng: engine, table: SQLModel(table=True)):
    ''' Select all Mayz from database '''
    with Session(sql_eng) as session:
        query = select(table).order_by(table.created_at.desc())
        latest_row = session.exec(query).first()
        return latest_row


def select_id(sql_eng: engine, table: SQLModel(table=True), value: int):
    ''' Select one May from database '''
    with Session(sql_eng) as session:
        query = session.get(table, value)
        return query


def update_id(
    sql_eng: engine, table: SQLModel(table=True), model: SQLModel, index: int
):
    ''' Select one May from database '''
    with Session(sql_eng) as session:
        edited_row = session.get(table, index)
        if edited_row:
            new_row = model.dict(exclude_unset=True)
            for key, value in new_row.items():
                setattr(edited_row, key, value)
            session.add(edited_row)
            session.commit()
            session.refresh(edited_row)
        return edited_row


def delete_id(sql_engine: engine, table: SQLModel(table=True), value: int):
    ''' Select one May from database '''
    with Session(sql_engine) as session:
        deleted_row = session.get(table, value)
        if deleted_row:
            session.delete(deleted_row)
            session.commit()
            return True
        return False
