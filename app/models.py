''' Table Model configuration with SQLModel '''

from datetime import datetime
from sqlmodel import Field, SQLModel, DateTime, Column


class May(SQLModel, table=True):
    ''' Defining the May Model '''
    id_may: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=30)
    content: str = Field(max_length=120)
    published: bool = Field(default=True, nullable=False)
    created_at: datetime | None = Field(sa_column=Column(
        DateTime(timezone=True), nullable=False), default=datetime.utcnow())
