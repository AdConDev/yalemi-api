''' Table Model configuration with SQLModel '''

from sqlmodel import Field, SQLModel


class May(SQLModel, table=True):
    ''' Defining the May Model '''
    id_may: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=30)
    content: str = Field(max_length=120)
    published: bool = Field(default=True)
    created_at: str = Field(max_length=25)
