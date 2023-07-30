''' Table Model configuration with SQLModel '''

from datetime import datetime
from sqlmodel import Field, SQLModel, Column, Boolean, TIMESTAMP, text


class MayBase(SQLModel):
    ''' Defining the May Base Model '''
    title: str = Field(max_length=30, index=True)
    content: str = Field(max_length=120, index=True)
    published: bool | None = Field(
        sa_column=Column(
            Boolean(create_constraint=True), nullable=False,
            server_default='TRUE'
        ),
        default=None
    )


class May(MayBase, table=True):
    ''' Defining the May Model '''
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False,
            server_default=text('NOW()')),
        default=None, index=True)


class MayCreate(MayBase):
    ''' Defining the May Crate Model '''


class MayRead(MayBase):
    ''' Defining the May Model '''
    id: int
    created_at: datetime


class MayUpdate(SQLModel):
    ''' Defining the May Update Model '''
    title: str | None = None
    content: str | None = None
    published: bool | None = None
