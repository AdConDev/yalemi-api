''' Table Model configuration with SQLModel '''

from datetime import datetime
from sqlmodel import Field, SQLModel, Column, Boolean, TIMESTAMP, text


class May(SQLModel, table=True):
    ''' Defining the May Model '''
    id_may: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=30)
    content: str = Field(max_length=120)
    published: bool | None = Field(
        sa_column=Column(
            Boolean(create_constraint=True), nullable=False,
            server_default='TRUE'),
        default=None)
    created_at: datetime | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False,
            server_default=text('NOW()')),
        default=None)
