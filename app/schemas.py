''' Data Schema configuration using Pydantic '''

from pydantic import BaseModel


class May(BaseModel):
    ''' Defining the May schema '''
    title: str
    content: str
    published: bool = True
