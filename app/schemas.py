''' Data Schema using Pydantic. Not needed anymore, SLQModel is enough. '''

from pydantic import BaseModel


class May(BaseModel):
    ''' Defining the May schema '''
    id: int | None
    title: str
    content: str
    published: bool = True
    created_at: str | None
